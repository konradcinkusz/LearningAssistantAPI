import time
from abc import ABC, abstractmethod
from api.openai_client import OpenAIClient
from utils.pretty_print import pretty_print_thread_messages_colored_desc
from contextlib import redirect_stdout
import io
import sys

class BaseService(ABC):
    def __init__(self, service_name):
        self.client = OpenAIClient()
        self.service_name = service_name
        self.thread_id = None  # Initialize thread_id as None
        
    def create_thread(self):
        """
        Creates a new thread and stores its ID in the instance variable.
        """
        thread = self.client.create_thread()
        self.thread_id = thread.id

    def post_message(self, content, role="user"):
        """
        Posts a message to the current thread, identified by self.thread_id.
        """
        if self.thread_id is None:
            raise ValueError("Thread has not been created yet.")
        self.client.create_message(thread_id=self.thread_id, role=role, content=content)

    def run_assistant(self, assistant_id, instructions):
        """
        Initiates a run with the assistant for the current thread.
        """
        if self.thread_id is None:
            raise ValueError("Thread has not been created yet.")
        run = self.client.create_run(thread_id=self.thread_id, assistant_id=assistant_id, instructions=instructions)
        run_id = run.id
        return self.client.retrieve_run(thread_id=self.thread_id, run_id=run_id).status

    def run_assistant_and_wait(self, assistant_id, instructions):
        """
        Initiates a run with the assistant and waits for it to complete, checking the status periodically.
        """
        if self.thread_id is None:
            raise ValueError("Thread has not been created yet.")
        run = self.client.create_run(thread_id=self.thread_id, assistant_id=assistant_id, instructions=instructions)
        run_id = run.id
        end_statuses = ['completed', 'cancelled', 'failed', 'expired']
        start_time = time.time()
        while True:
            run_status = self.client.retrieve_run(thread_id=self.thread_id, run_id=run_id).status
            elapsed_time = time.time() - start_time
            print(f"Current status: {run_status}, Total time: {elapsed_time:.2f} seconds")
            
            if run_status in end_statuses:
                print(f"Process ended with status: {run_status}, Total time: {elapsed_time:.2f} seconds")
                break
            time.sleep(10)  # Wait before checking again

        self.fetch_and_print_messages()

    def fetch_and_print_messages(self):
        """
        Fetches and prints all messages from the current thread to both the console and a file.
        The file is named with the current date-time as its name.
        """
        if self.thread_id is None:
            raise ValueError("Thread has not been created yet.")
        messages = self.client.list_messages(self.thread_id)
        
        # Capture the output in an in-memory buffer
        buffer = io.StringIO()
        sys.stdout = buffer  # Temporarily redirect stdout to the buffer
        
        pretty_print_thread_messages_colored_desc(messages.data)
        
        # Restore stdout to its original state
        sys.stdout = sys.__stdout__
        
        # Get the buffer content and print it to the console
        output = buffer.getvalue()
        print(output)  # This prints to the console
        
        # Also save the output to a file
        filename = time.strftime("%Y-%m-%d_%H-%M-%S") + "_output.log"
        with open(filename, "w") as file:
            file.write(output)
        
        print(f"Output saved to {filename}")
        
        # Don't forget to close the buffer!
        buffer.close()

    @abstractmethod
    def create_or_retrieve_assistant(self):
        pass

    def _find_first_asistant_by_name(self):
        assistants_data = self.client.list_assistants().data
        for assistant in assistants_data:
            name = assistant.name.lower()
            description = (assistant.description or '').lower()
            if self.service_name.lower() in name or self.service_name.lower() in description:
                return assistant.id
        return None
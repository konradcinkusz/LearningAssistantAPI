import time
from abc import ABC, abstractmethod
from api.openai_client import OpenAIClient
from utils.pretty_print import pretty_print_thread_messages_colored_desc
import io
import sys

class BaseService(ABC):
    def __init__(self, service_name, period=10):
        self.client = OpenAIClient()
        self.service_name = service_name
        self.thread_id = None  # Initialize thread_id as None
        self.period = period  # Initialize period as 10 seconds

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
            retrieved_run = self.client.retrieve_run(thread_id=self.thread_id, run_id=run_id)
            run_status = retrieved_run.status
            elapsed_time = time.time() - start_time
            print(f"Current status: {run_status}, Total time: {elapsed_time:.2f} seconds")
            
            if run_status in end_statuses:
                print(f"Process ended with status: {run_status}, Total time: {elapsed_time:.2f} seconds")
                break
            elif run_status == 'requires_action':
                print("Run requires action to proceed.")
                if retrieved_run.required_action.type == 'submit_tool_outputs':
                    tool_calls = retrieved_run.required_action.submit_tool_outputs.tool_calls
                    tool_outputs = []
                    for tool_call in tool_calls:
                        tool_call_id = tool_call.id
                        # For simplicity, we're just using the function name and arguments in the prompt.
                        # In a real application, you'd likely want to provide more context or use a more user-friendly format.
                        function_name = tool_call.function.name
                        arguments = tool_call.function.arguments
                        print(f"Required output for tool call {tool_call_id}: {function_name} with arguments {arguments}")
                        user_output = input("Please enter the required output: ")
                        tool_outputs.append({
                            "tool_call_id": tool_call_id,
                            "output": user_output,
                        })

                    # Submit the tool outputs provided by the user
                    self.client.submit_tool_outputs(
                        thread_id=self.thread_id,
                        run_id=run_id,
                        tool_outputs=tool_outputs
                    )
                    print("Submitted required tool outputs.")
                else:
                    print("Unknown required action, unable to proceed.")
                    break
                # After handling requires_action, it might be a good idea to continue the loop to check the new status.
                # However, consider adding a short delay before continuing to avoid rapid-fire API calls.
                time.sleep(1)
                continue
            time.sleep(self.period)  # Wait before checking again

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
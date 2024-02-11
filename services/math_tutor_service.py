import time
from api.openai_client import OpenAIClient
from utils.pretty_print import pretty_print_thread_messages_colored_desc

class MathTutorService:
    def __init__(self):
        self.client = OpenAIClient()
        self.math_tutor = "Math Tutor"
        self.thread_id = None  # Initialize thread_id as None

    def __find_first_math_tutor_id(self):
        assistants_data = self.client.list_assistants().data
        for assistant in assistants_data:
            name = assistant.name.lower()
            description = (assistant.description or '').lower()
            if self.math_tutor.lower() in name or self.math_tutor.lower() in description:
                return assistant.id
        return None

    def create_or_retrieve_math_tutor(self):
        math_tutor_id = self.__find_first_math_tutor_id()
        if math_tutor_id is None:
            python_math_file = self.client.upload_file("data/code_interpreter_files/math_basic_functions.py", "assistants")
            math_file = self.client.upload_file("data/retrieval_knowledge_files/knowledge.pdf", "assistants")
            assistant = self.client.create_assistant(
                name=self.math_tutor,
                instructions="You are a personal math tutor. Write and run code to answer math questions. Find the right definition in the PDF Fundamentals of Mathematics I. Always return example python code.",
                tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
                model="gpt-4-turbo-preview",
                file_ids=[python_math_file.id, math_file.id]
            )
            print('Math tutor created!')
            return assistant
        else:
            return self.client.retrieve_assistant(math_tutor_id)

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

        # Simplified status retrieval; consider implementing more robust handling
        run_status = self.client.retrieve_run(thread_id=self.thread_id, run_id=run_id).status
        return run_status

    def run_assistant_and_wait(self, assistant_id, instructions):
        """
        Initiates a run with the assistant and waits for it to complete, checking the status periodically.
        """
        if self.thread_id is None:
            raise ValueError("Thread has not been created yet.")

        # Start the assistant run
        run = self.client.create_run(thread_id=self.thread_id, assistant_id=assistant_id, instructions=instructions)
        run_id = run.id

        end_statuses = ['completed', 'cancelled', 'failed', 'expired']
        start_time = time.time()

        # Periodically check the run status
        while True:
            run_status = self.client.retrieve_run(thread_id=self.thread_id, run_id=run_id).status
            print(f"Current status: {run_status}")

            # Calculate elapsed time in seconds
            elapsed_time = time.time() - start_time

            if run_status in end_statuses:
                print(f"Process ended with status: {run_status}")
                print(f"Total time: {elapsed_time:.2f} seconds")
                break

            time.sleep(10)  # Wait before checking again

        # Optionally, fetch and print messages here or handle elsewhere
        self.fetch_and_print_messages()

    def fetch_and_print_messages(self):
        """
        Fetches and prints all messages from the current thread.
        """
        if self.thread_id is None:
            raise ValueError("Thread has not been created yet.")
        messages = self.client.list_messages(self.thread_id)
        pretty_print_thread_messages_colored_desc(messages.data)
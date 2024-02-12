from services.base_service import BaseService
from utils.pretty_print import pretty_print_thread_messages_colored_desc

class MathTutorService(BaseService):
    def __init__(self):
        super().__init__(service_name="Math Tutor")

    def create_or_retrieve_assistant(self):
        math_tutor_id = self._find_first_asistant_by_name()
        if math_tutor_id is None:
            python_math_file = self.client.upload_file("data/code_interpreter_files/math_basic_functions.py", "assistants")
            math_file = self.client.upload_file("data/retrieval_knowledge_files/knowledge.pdf", "assistants")
            assistant = self.client.create_assistant(
                name=self.service_name,
                instructions="You are a personal math tutor. Write and run code to answer math questions. Find the right definition in the PDF Fundamentals of Mathematics I. Always return example python code.",
                tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
                model="gpt-4-turbo-preview",
                file_ids=[python_math_file.id, math_file.id]
            )
            print('Math tutor created!')
            return assistant
        else:
            return self.client.retrieve_assistant(math_tutor_id)

from application.application_base import Application
from services.book_writer_service import BookWriterService

class BookWriterApplication(Application):
    def __init__(self):
        super().__init__(BookWriterService())

    def _execute(self, assistant):
        print("Book Writer Assistant is ready to help you.")
        self.service.create_thread()
        self.service.post_message("I have an idea of creating a book about Neuralink usage by the 100 years from today. Write a conspectus and show me the example chapters.")
        instructions = "Please make it realistic, although it still should be sci-fi."
        self.service.run_assistant_and_wait(assistant.id, instructions)

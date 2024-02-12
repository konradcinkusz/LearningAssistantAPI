from application.application_base import Application
from services.book_writer_service import BookWriterService

class BookWriterApplication(Application):
    def __init__(self):
        super().__init__(BookWriterService())

    def run(self):
        assistant = self.service.create_or_retrieve_assistant()
        if assistant is None:
            print("Failed to create or retrieve the Book Writer assistant.")
            return
        
        print("Book Writer Assistant is ready to help you.")
        
        self.service.create_thread()

        #I have modified this
        self.service.post_message("I have an idea of creating book about neuralink usage by the 100 years from today. Write conspectus and show me the example chapters.")
        
        # Assuming you have the assistant ID from the assistant object
        assistant_id = assistant.id  # Example; replace with actual retrieval
        
        #I have modified this
        instructions = "Please make it realistic, although it still should be sci-fci."

        
        self.service.run_assistant_and_wait(assistant_id, instructions)
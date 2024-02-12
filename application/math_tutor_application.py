from application.application_base import Application
from services.math_tutor_service import MathTutorService

class MathTutorApplication(Application):
    def __init__(self): 
        # Initialize the parent class with the service instance
        super().__init__(MathTutorService())
    
    def run(self):
        assistant = self.service.create_or_retrieve_assistant()
        if assistant is None:
            print("Failed to create or retrieve the Math Tutor assistant.")
            return
        
        print("Math Tutor Assistant is ready to help you.")
        
        self.service.create_thread()
        self.service.post_message("I need to solve the equation `x^2 + 3x + 11 - 14 = 0`. Can you help?")
        
        # Assuming you have the assistant ID from the assistant object
        assistant_id = assistant.id  # Example; replace with actual retrieval
        
        instructions = "Please solve the given equation."
        self.service.run_assistant_and_wait(assistant_id, instructions)

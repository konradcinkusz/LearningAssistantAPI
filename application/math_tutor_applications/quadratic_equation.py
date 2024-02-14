from application.application_base import Application
from services.math_tutor_service import MathTutorService

class MathTutorApplication(Application):
    def __init__(self): 
        super().__init__(MathTutorService())
    
    def _execute(self, assistant):
        self.service.create_thread()
        self.service.post_message("I need to solve the equation `x^2 + 3x + 11 - 14 = 0`. Can you help?")
        instructions = "Please solve the given equation."
        self.service.run_assistant_and_wait(assistant.id, instructions)

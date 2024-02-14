from application.application_base import Application
from services.math_tutor_service import MathTutorService

class MathTutorSorting(Application):
    def __init__(self): 
        super().__init__(MathTutorService())
    
    def _execute(self, assistant):
        self.service.create_thread()
        self.service.post_message("I have a list of numbers `[12, 3, 5, 7, 2, 8, 1]` and I need to sort them in ascending order. Can you guide me through the process? Perform different types of algorithms to sort the list. I want insertion_sort and buble_sort to be performed.")
        instructions = "Please help me sort the given list of numbers in ascending order."
        self.service.run_assistant_and_wait(assistant.id, instructions)

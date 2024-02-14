from abc import ABC, abstractmethod
from dotenv import load_dotenv, find_dotenv
from services.base_service import BaseService

class Application(ABC):
    def __init__(self, service: BaseService):
        load_dotenv(find_dotenv())
        self.service = service

    def run(self):
        # Default behavior or setup steps
        assistant = self.__create_or_retrieve_assistant()
        if assistant is None:
            return
        # Call an abstract method that subclasses must implement
        self._execute(assistant)

    def __create_or_retrieve_assistant(self):
        assistant = self.service.create_or_retrieve_assistant()
        if assistant is None:
            print("Failed to create or retrieve the assistant.")
            return None
        print("Assistant is ready to help you.")
        return assistant

    @abstractmethod
    def _execute(self, assistant):
        """
        Subclasses must implement this method to define specific behavior.
        """
        pass

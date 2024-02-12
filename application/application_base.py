from abc import ABC, abstractmethod
from dotenv import load_dotenv, find_dotenv

from services.base_service import BaseService

class Application(ABC):
    def __init__(self, service: BaseService):
        load_dotenv(find_dotenv())
        self.service = service
    
    @abstractmethod
    def run(self):
        pass
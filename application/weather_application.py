from application.application_base import Application
from services.weather_bot import WeatherBotService

class WeatherApplication(Application):
    def __init__(self):
        super().__init__(WeatherBotService())

    def _execute(self, assistant):
        print("Weather Assistant is ready to help you.")
        self.service.create_thread()
        instructions = "Help with weather checking."
        self.service.run_assistant_and_wait(assistant.id, instructions)

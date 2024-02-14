from services.base_service import BaseService

class WeatherBotService(BaseService):
    def __init__(self):
        super().__init__(service_name="Weather bot")

    def create_or_retrieve_assistant(self):
        assistant_id = self._find_first_asistant_by_name()
        if assistant_id is None:
            assistant = self.client.create_assistant(
                name=self.service_name, 
                instructions="You are a weather bot. Use the provided functions to answer questions.",
                model="gpt-4-turbo-preview",
                tools=[{
                    "type": "function",
                    "function": {
                        "name": "getCurrentWeather",
                        "description": "Get the weather in location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
                                "unit": {"type": "string", "enum": ["c", "f"]}
                            },
                            "required": ["location"]
                            }
                        }
                    }, 
                    {
                    "type": "function",
                    "function": {
                        "name": "getNickname",
                        "description": "Get the nickname of a city",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
                                },
                            "required": ["location"]
                            }
                        } 
                }]
                , file_ids= []
            )
            print('Weather bot created!')
            return assistant
        else:
            return self.client.retrieve_assistant(assistant_id)
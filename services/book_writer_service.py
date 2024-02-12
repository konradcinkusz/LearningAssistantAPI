from services.base_service import BaseService

class BookWriterService(BaseService):
    def __init__(self):
        super().__init__(service_name="Book writer")

    def create_or_retrieve_assistant(self):
        assistant_id = self._find_first_asistant_by_name()
        if assistant_id is None:
            assistant = self.client.create_assistant(
                name=self.service_name,
                instructions="You are the book writer. Your task is to create realistic Science Fiction books based on input context from the user. Your goal is to craft compelling and believable science fiction narratives that captivate the audience. Your response should reflect an understanding of the science fiction genre and the ability to infuse realistic elements into imaginative and futuristic storylines. Emphasize the importance of blending scientific concepts with creative storytelling to engage readers and evoke a sense of authenticity within the fictional world.",
                tools=[],
                model="gpt-4-turbo-preview",
                file_ids=[]
            )
            print('Book writer created!')
            return assistant
        else:
            return self.client.retrieve_assistant(assistant_id)
from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI()

    def create_assistant(self, name, instructions, tools, model, file_ids):
        return self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            tools=tools,
            model=model,
            file_ids=file_ids
        )
    
    def submit_tool_outputs(self, thread_id, run_id, tool_outputs):
        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )

    def list_assistants(self, order="desc", limit="20"):
        return self.client.beta.assistants.list(order=order, limit=limit)

    def retrieve_assistant(self, assistant_id):
        return self.client.beta.assistants.retrieve(assistant_id)

    def create_thread(self):
        return self.client.beta.threads.create()

    def create_message(self, thread_id, role, content):
        return self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=content
        )

    def create_run(self, thread_id, assistant_id, instructions):
        return self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            instructions=instructions
        )

    def retrieve_run(self, thread_id, run_id):
        return self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

    def list_messages(self, thread_id):
        return self.client.beta.threads.messages.list(thread_id)

    def upload_file(self, file_path, purpose):
        with open(file_path, "rb") as file:
            return self.client.files.create(file=file, purpose=purpose)

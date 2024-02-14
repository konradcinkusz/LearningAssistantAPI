from openai import OpenAI

client = OpenAI()

def remove_all_assistants(assistants_data):
    for assistant in assistants_data:
        assistant_id = assistant.id
        try:
            # Attempt to delete the assistant by ID
            response = client.beta.assistants.delete(assistant_id)
            print(f"Deleted assistant with ID: {assistant_id}")
        except Exception as e:
            # Handle any errors that occur during deletion
            print(f"Error deleting assistant with ID {assistant_id}: {e}")


my_assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
)

# Extract the data attribute from the my_assistants object
assistants_data = my_assistants.data

remove_all_assistants(assistants_data)
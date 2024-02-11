import time

from openai import OpenAI

from utils.pretty_print import pretty_print_thread_messages_colored_desc

client = OpenAI()

math_tutor = "Math Tutor"

my_assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
)

def find_first_math_tutor_id(assistants_data):
    for assistant in assistants_data:
        name = assistant.name.lower()  # Normalize to lower case for case-insensitive comparison
        description = (assistant.description or '').lower()  # Same here, with safe handling of None
        if math_tutor.lower() in name or math_tutor.lower() in description:
            return assistant.id
    return None  # Return None if no Math Tutor is found

# Extract the data attribute from the my_assistants object
assistants_data = my_assistants.data

# Find the first Math Tutor's ID
math_tutor_id = find_first_math_tutor_id(assistants_data)

if math_tutor_id == None:
    # Upload a file with an "assistants" purpose
    math_file = client.files.create(
      file=open("data/retrieval_knowledge_files/knowledge.pdf", "rb"),
      purpose='assistants'
    )

    # Upload a file with an "assistants" purpose
    python_math_file = client.files.create(
        file=open("data/code_interpreter_files/math_basic_functions.py", "rb"),
        purpose='assistants'
    )

    assistant = client.beta.assistants.create(
        name=math_tutor,
        instructions="You are a personal math tutor. Write and run code to answer math questions. Find the right definition in the PDF Fundamentals of Mathematics I. Always return example python code.",
        tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
        model="gpt-4-turbo-preview",
        #model="gpt-3.5-turbo-16k",
        file_ids=[python_math_file.id, math_file.id]
    )

    print('Math tutor created!')
else:
    assistant = client.beta.assistants.retrieve(math_tutor_id)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    #content="I need to solve the equation `3x + 11 = 14`. Can you help me? Prepare analysis based on your knowledge, based on the additional resources like my math book, and then create the python code to resolve more problems."
    content="I need to create python program that solve the equation `x^2+3x+11-14=0`. Can you do it for?"
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Konrad. The user is eager to learn math deeply and write proper python code."
)

end_statuses = ['completed', 'cancelled', 'failed', 'expired']

# Initialize the start time
start_time = time.time()

while True:
    run_status = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
    ).status

    print(f"Current status: {run_status}")

    # Calculate elapsed time in seconds
    elapsed_time = time.time() - start_time

    if run_status in end_statuses:
        print(f"Process ended with status: {run_status}")
        print(f"Total time: {elapsed_time:.2f} seconds")
        break
    
    time.sleep(10)

list_of_thread_messages = client.beta.threads.messages.list(thread.id)

messages = []
for message in list_of_thread_messages:
    # Extract the message content
    message_content = message.content[0].text
    annotations = message_content.annotations
    citations = []

    # Iterate over the annotations and add footnotes
    for index, annotation in enumerate(annotations):
        # Replace the text with a footnote
        message_content.value = message_content.value.replace(annotation.text, f' [{index}]')

        # Gather citations based on annotation attributes
        if (file_citation := getattr(annotation, 'file_citation', None)):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
        elif (file_path := getattr(annotation, 'file_path', None)):
            cited_file = client.files.retrieve(file_path.file_id)
            citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
            # Note: File download functionality not implemented above for brevity

    # Add footnotes to the end of the message before displaying to user
    message_content.value += '\n' + '\n'.join(citations)
    messages.append(message_content.value)

# print(messages)
# print(list_of_thread_messages.data)

print('Pretty colored:')

pretty_print_thread_messages_colored_desc(list_of_thread_messages.data)
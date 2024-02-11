from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
#api_key  = os.environ['OPENAI_API_KEY']

client = OpenAI()

assistant = client.beta.assistants.retrieve("asst_QTbKMhYl3CJp3a0wanAqFUgq")

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Can you write for me a book about quantum programming in the nearest galaxy?"
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
)

import time

# Assuming `client` is already initialized and `thread_id` and `initial_run_id` are known
thread_id = thread.id
run_id = run.id

# Define a list of end states
end_states = ['completed', 'cancelled', 'failed', 'expired']

# Start a loop to periodically check the status of the run
while True:
    # Retrieve the current status of the run
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    ).status
    
    print(f"Current run status: {run_status}")  # Optional: for logging the status
    
    # Check if the run status is in one of the end states
    if run_status in end_states:
        print(f"Process ended with status: {run_status}")
        break  # Exit the loop if the process is completed or in a relevant end state
    
    # Wait for a specified time before checking the status again to avoid overwhelming the server
    time.sleep(10)  # Adjust the sleep time as necessary


messages = client.beta.threads.messages.list(
  thread_id=thread.id
)
print(messages)
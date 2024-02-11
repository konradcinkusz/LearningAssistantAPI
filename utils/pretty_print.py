from termcolor import colored

def pretty_print_thread_messages_colored_desc(thread_messages):
    # Sort messages in descending order by 'created_at' attribute
    sorted_messages = sorted(thread_messages, key=lambda x: x.created_at, reverse=False)

    for msg in sorted_messages:
        role = msg.role
        # Assuming the content is a list, but we'll just print the first item's value for simplicity
        content = msg.content[0].text.value if msg.content else "No content"

        # Set color based on role
        color = "blue" if role == "assistant" else "green"

        # Print role and content with color
        print(colored(f"{role.upper()}\t", color) + content)
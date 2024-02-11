from services.math_tutor_service import MathTutorService
from dotenv import load_dotenv, find_dotenv

def main():
    _ = load_dotenv(find_dotenv())
    # Initialize MathTutorService with the OpenAIClient instance
    math_tutor_service = MathTutorService()
    
    # Attempt to create or retrieve the Math Tutor assistant
    assistant = math_tutor_service.create_or_retrieve_math_tutor()
    
    if assistant is None:
        print("Failed to create or retrieve the Math Tutor assistant.")
        return
    
    print("Math Tutor Assistant is ready to help you.")
    
    # Create a thread
    math_tutor_service.create_thread()
    
    # Post a message to the thread
    math_tutor_service.post_message("I need to solve the equation `x^2 + 3x + 11 - 14 = 0`. Can you help?")
    
    # Assuming you have the assistant ID from the assistant object
    assistant_id = assistant.id  # Example; replace with actual retrieval
    
    # Instructions for the assistant
    instructions = "Please solve the given equation."
    
    # Run the assistant and wait for its completion
    math_tutor_service.run_assistant_and_wait(assistant_id, instructions)

    # The method 'run_assistant_and_wait' now internally waits for completion and can also print messages,
    # so you no longer need to separately fetch and print messages unless you've designed it to only fetch in 'fetch_and_print_messages'.

if __name__ == "__main__":
    main()

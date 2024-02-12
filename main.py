from application.book_writer_application import BookWriterApplication
from application.math_tutor_application import MathTutorApplication

def main():
    # Create a dictionary with boolean keys and application objects as values
    applications = {
        False: BookWriterApplication(),   # This will run
        True: MathTutorApplication()    # This will not run
    }

    any(app.run() for should_run, app in applications.items() if should_run)

if __name__ == "__main__":
    main()

from application.book_writer_application import BookWriterApplication
from application.math_tutor_applications.quadratic_equation import MathTutorApplication
from application.math_tutor_applications.sorting import MathTutorSorting
from application.weather_application import WeatherApplication

def main():
    
    # Create a dictionary with boolean keys and application objects as values
    applications = {
        False: BookWriterApplication(),
        False: MathTutorApplication(),
        False: MathTutorSorting(),
        True: WeatherApplication(),
    }

    any(app.run() for should_run, app in applications.items() if should_run)

if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import messagebox, ttk
from application.book_writer_application import BookWriterApplication
from application.math_tutor_applications.quadratic_equation import MathTutorApplication
import threading

def update_progress_bar(progress_bar, status_label, app_name, process_function):
    status_label.config(text="Running...")
    progress_bar.start(10)
    threading.Thread(target=lambda: run_application(process_function, progress_bar, status_label, app_name)).start()

def run_application(app, progress_bar, status_label, app_name):
    try:
        app.run()
        messagebox.showinfo("Success", f"{app_name} ran successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run {app_name}: {e}")
    finally:
        progress_bar.stop()
        status_label.config(text="Ready")

def main():
    root = tk.Tk()
    root.title("Application Runner")
    root.geometry("400x200")

    # Status labels and progress bars for applications
    status_label_book_writer = tk.Label(root, text="Ready")
    status_label_book_writer.pack()
    progress_bar_book_writer = ttk.Progressbar(root, orient="horizontal", mode="indeterminate", length=280)
    progress_bar_book_writer.pack()

    book_writer_btn = tk.Button(root, text="Run Book Writer", command=lambda: update_progress_bar(progress_bar_book_writer, status_label_book_writer, "Book Writer", BookWriterApplication()))
    book_writer_btn.pack(pady=10)

    status_label_math_tutor = tk.Label(root, text="Ready")
    status_label_math_tutor.pack()
    progress_bar_math_tutor = ttk.Progressbar(root, orient="horizontal", mode="indeterminate", length=280)
    progress_bar_math_tutor.pack()

    math_tutor_btn = tk.Button(root, text="Run Math Tutor", command=lambda: update_progress_bar(progress_bar_math_tutor, status_label_math_tutor, "Math Tutor", MathTutorApplication()))
    math_tutor_btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

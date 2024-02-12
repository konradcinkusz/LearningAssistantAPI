Before running the main file you have to define your own .env file with your openAI key OPENAI_API_KEY="your_value"

1. knowledge.pdf didn't work, although it isn't a part of assistas
a. Math Tutor return issue with opening the pdf file
2. I am not receiving "the code"


TODO
Think about good examples of assistants. 


## NOTES

any(app.run() for should_run, app in applications.items() if should_run)

This line uses any() to iterate over the generator expression. The generator will execute app.run() for each item where should_run is True. The use of any() is a bit of a hack here: it's primarily used to consume the generator and cause the side effects (calling app.run()), rather than to evaluate to True or False based on the iterated values. This is because the expression inside the generator (app.run() for should_run, app in applications.items() if should_run) only gets executed for its side effects (running the run method of the application objects), and any() is needed to force the generator to proceed through its items.
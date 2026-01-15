import random

def get_questions():
    return [
        {
            "question": "What is the correct way to create a function in Python?",
            "options": ["a) function my_func():", "b) def my_func():", "c) create my_func():", "d) my_func():"],
            "answer": "b"
        },
        {
            "question": "Which of these is used to define a list in Python?",
            "options": ["a) {}", "b) ()", "c) []", "d) <>"],
            "answer": "c"
        },
        {
            "question": "What is the output of print(type(10))?",
            "options": ["a) <class 'float'>", "b) <class 'str'>", "c) <class 'list'>", "d) <class 'int'>"],
            "answer": "d"
        },
        {
            "question": "How do you start a comment in Python?",
            "options": ["a) //", "b) /*", "c) #", "d) --"],
            "answer": "c"
        },
        {
            "question": "Which keyword is used for a loop that continues while a condition is true?",
            "options": ["a) for", "b) during", "c) loop", "d) while"],
            "answer": "d"
        }
    ]

def run_chatbot():
    questions = get_questions()
    print("Welcome to the Python Quiz Chatbot!")
    print("Answer the questions by typing the letter of the correct option (a, b, c, or d).")
    print("Type 'quit' at any time to exit the chat.\n")

    while True:
        q_data = random.choice(questions)
        print(q_data["question"])
        for option in q_data["options"]:
            print(option)
        
        user_input = input("\nYour answer (or 'quit'): ").strip().lower()

        if user_input == 'quit':
            print("Thanks for playing! Goodbye.")
            break
        
        if user_input == q_data["answer"]:
            print("Correct! Well done.\n")
        elif user_input in ['a', 'b', 'c', 'd']:
            print(f"Wrong. The correct answer was {q_data['answer']}.\n")
        else:
            print("Invalid input. Please enter a, b, c, d, or 'quit'.\n")

if __name__ == '__main__':
    run_chatbot()

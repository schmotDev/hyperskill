import random
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Python Quiz API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Question(BaseModel):
    id: int
    question: str
    options: List[str]

class AnswerRequest(BaseModel):
    question_id: int
    answer: str

class AnswerResponse(BaseModel):
    correct: bool
    correct_answer: Optional[str] = None
    message: str

# Data from main.py
QUESTIONS_DATA = [
    {
        "id": 1,
        "question": "What is the correct way to create a function in Python?",
        "options": ["a) function my_func():", "b) def my_func():", "c) create my_func():", "d) my_func():"],
        "answer": "b"
    },
    {
        "id": 2,
        "question": "Which of these is used to define a list in Python?",
        "options": ["a) {}", "b) ()", "c) []", "d) <>"],
        "answer": "c"
    },
    {
        "id": 3,
        "question": "What is the output of print(type(10))?",
        "options": ["a) <class 'float'>", "b) <class 'str'>", "c) <class 'list'>", "d) <class 'int'>"],
        "answer": "d"
    },
    {
        "id": 4,
        "question": "How do you start a comment in Python?",
        "options": ["a) //", "b) /*", "c) #", "d) --"],
        "answer": "c"
    },
    {
        "id": 5,
        "question": "Which keyword is used for a loop that continues while a condition is true?",
        "options": ["a) for", "b) during", "c) loop", "d) while"],
        "answer": "d"
    }
]

@app.get("/questions", response_model=List[Question])
async def get_all_questions():
    """Retrieve all available quiz questions (without answers)."""
    return [Question(**{k: v for k, v in q.items() if k != "answer"}) for q in QUESTIONS_DATA]

@app.get("/questions/random", response_model=Question)
async def get_random_question():
    """Retrieve a random quiz question (without answer)."""
    q = random.choice(QUESTIONS_DATA)
    return Question(**{k: v for k, v in q.items() if k != "answer"})

@app.post("/verify", response_model=AnswerResponse)
async def verify_answer(request: AnswerRequest):
    """Verify if the provided answer for a specific question is correct."""
    question = next((q for q in QUESTIONS_DATA if q["id"] == request.question_id), None)
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    user_answer = request.answer.strip().lower()
    is_correct = user_answer == question["answer"]
    
    if is_correct:
        return AnswerResponse(
            correct=True,
            message="Correct! Well done."
        )
    else:
        return AnswerResponse(
            correct=False,
            correct_answer=question["answer"],
            message=f"Wrong. The correct answer was {question['answer']}."
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

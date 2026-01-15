const API_URL = 'http://localhost:8000';
let currentQuestionId = null;
let score = 0;

const questionText = document.getElementById('question-text');
const optionsContainer = document.getElementById('options-container');
const feedback = document.getElementById('feedback');
const nextBtn = document.getElementById('next-btn');
const scoreDisplay = document.getElementById('score');

async function fetchRandomQuestion() {
    try {
        const response = await fetch(`${API_URL}/questions/random`);
        if (!response.ok) throw new Error('Failed to fetch question');
        const question = await response.json();
        displayQuestion(question);
    } catch (error) {
        questionText.textContent = 'Error loading question. Is the API running?';
        console.error(error);
    }
}

function displayQuestion(question) {
    currentQuestionId = question.id;
    questionText.textContent = question.question;
    optionsContainer.innerHTML = '';
    feedback.classList.add('hidden');
    nextBtn.classList.add('hidden');

    question.options.forEach(option => {
        const button = document.createElement('button');
        button.textContent = option;
        button.className = 'option-btn';
        button.onclick = () => handleOptionClick(option[0], button);
        optionsContainer.appendChild(button);
    });
}

async function handleOptionClick(selectedLetter, button) {
    // Disable all buttons after selection
    const buttons = optionsContainer.querySelectorAll('.option-btn');
    buttons.forEach(btn => btn.disabled = true);
    button.classList.add('selected');

    try {
        const response = await fetch(`${API_URL}/verify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question_id: currentQuestionId,
                answer: selectedLetter
            }),
        });

        const result = await response.json();
        showFeedback(result);
    } catch (error) {
        console.error('Error verifying answer:', error);
    }
}

function showFeedback(result) {
    feedback.textContent = result.message;
    feedback.className = result.correct ? 'correct' : 'wrong';
    feedback.classList.remove('hidden');
    
    if (result.correct) {
        score++;
        scoreDisplay.textContent = score;
    }

    nextBtn.classList.remove('hidden');
}

nextBtn.onclick = () => {
    fetchRandomQuestion();
};

// Initial load
fetchRandomQuestion();

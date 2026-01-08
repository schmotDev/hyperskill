## AI Diet and Meal Planner

Short project, to design multi-agent workflows via REST APIs by using FastAPI to structure, validate, and expose agent services.  
It interacts with LLM providers using prompts, implement prompt engineering techniques and orchestrate LLM-based agents.

<br>

### Summary

A multi-agent AI system using FastAPI where each agent plays a role in designing the perfect recipe depending on what you have in your kitchen and your nutritional needs.

<br>

### To run the script

* First you need to set up the FastApi service.
The service can be started by typing:
`uvicorn main:app --reload --port 8000`  

This will make the servcie available at: `http://localhost:8000/`

<br>

* You need to add a `.env` file with your OpenRouter API KEY  and the Base URL of OpenRouter

```.env
OPENROUTER_API_KEY=sk-xxxxx
OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

<br>

### Example of conversation with the agent

## AI Diet and Meal Planner

Short project, to design multi-agent workflows via REST APIs by using FastAPI to structure, validate, and expose agent services.  
It interacts with LLM providers using prompts, implement prompt engineering techniques and orchestrate LLM-based agents.

<br>

### Summary

A multi-agent AI system using FastAPI where each agent plays a role in designing the perfect recipe depending on what you have in your kitchen and your nutritional needs.

<br>

### To run the script

* You need to add a `.env` file with your OpenRouter API KEY  and the Base URL of OpenRouter

    ```.env
    OPENROUTER_API_KEY=sk-xxxxx
    OPENAI_BASE_URL=https://openrouter.ai/api/v1
    ```

<br>

* The FastAPI service can be started by typing:
`uvicorn main:app --reload --port 8000`  

    This will make the service available at: `http://localhost:8000/`

<br>

### Example of conversation with the agent

*   you can send requests to the FastAPI such as:

```Request example with /plan endpoint - (linux)
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"base_recipe":"Vegan Stir Fry"}'
```
```Output:
{
  "title": "Vegan Stir Fry Deluxe",
  "ingredients": ["tofu", "bell pepper", "soy sauce", "garlic", "oil"],
  "steps": [
    { "step_number": 1, "instruction": "Press and cube the tofu." },
    { "step_number": 2, "instruction": "Heat oil in a pan and sauté garlic." },
    { "step_number": 3, "instruction": "Add tofu and cook until lightly browned." },
    { "step_number": 4, "instruction": "Add bell pepper slices and stir-fry for 5 minutes." },
    { "step_number": 5, "instruction": "Add soy sauce and stir well. Cook for another 2 minutes." },
    { "step_number": 6, "instruction": "Serve hot over rice or noodles." }
  ]
}
```

<br>

```Request example with /recommend endpoint - (linux)
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"items":["tofu","bell pepper","garlic","oil"],"diet":"vegan","recipe_count":2}'
```
```Output:
{
  "recipes": [
    {
      "title": "Vegan Garlic Pepper Tofu",
      "ingredients": ["tofu", "bell pepper", "garlic", "oil"],
      "steps": [
        { "step_number": 1, "instruction": "Slice tofu into cubes." },
        { "step_number": 2, "instruction": "Heat oil, sauté garlic until fragrant." },
        { "step_number": 3, "instruction": "Add tofu, stir-fry until golden." },
        { "step_number": 4, "instruction": "Add bell peppers, cook until tender." },
        { "step_number": 5, "instruction": "Serve hot with rice or quinoa." }
      ]
    },
    {
      "title": "Quick Vegan Tofu & Bell Pepper Stir Fry",
      "ingredients": ["tofu", "bell pepper", "garlic", "oil"],
      "steps": [
        { "step_number": 1, "instruction": "Cut tofu and peppers into strips." },
        { "step_number": 2, "instruction": "Warm oil in skillet, sauté garlic." },
        { "step_number": 3, "instruction": "Cook tofu strips until crispy." },
        { "step_number": 4, "instruction": "Add peppers and stir-fry quickly." },
        { "step_number": 5, "instruction": "Serve immediately with noodles or salad." }
      ]
    }
  ]
}
```
 <br>

You can transform the request to be used with Powershell (ask your favorite AI chatbot)

```Invoke-RestMethod -Method POST -Uri http://localhost:8000/plan -Headers @{ "Content-Type" = "application/json" } -Body '{"base_recipe":"Vegan Stir Fry"}' ```

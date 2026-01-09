from fastapi import FastAPI
from models import (
    InventoryInput,
    InventoryResponse,
    DietInput,
    DietResponse,
    AskInput,
    PlanInput,
    RecipeResponse,
    RecommendInput,
    RecommendOutput
)
from agents.inventory_agent import InventoryAgent
from agents.diet_agent import DietAgent
from agents.manager_agent import ManagerAgent
from agents.planner_agent import PlannerAgent
from mylogging import get_logger

logger = get_logger("app.api")



app = FastAPI(
    title="AI Diet & Meal Planner",
    description="Backend service for AI-powered diet and meal planning",
    version="1.0.0"
)

@app.get("/", response_model=dict)
async def root():
    return {"message": "Success!"}



inventory_agent = InventoryAgent()
diet_agent = DietAgent()
manager_agent = ManagerAgent()
planner_agent = PlannerAgent()

@app.post("/inventory", response_model=InventoryResponse)
def inventory_endpoint(payload: InventoryInput):
    return inventory_agent.run(payload.items)


@app.post("/diet", response_model=DietResponse)
def diet_endpoint(payload: DietInput):
    return diet_agent.run(payload.items, payload.diet)


@app.post("/ask")
def ask(input: AskInput):
    logger.info("Received /ask request: items=%s, diet=%s", input.items, input.diet)
    result = manager_agent.run(input.items, input.diet)
    logger.info("/ask response: suggestions=%s", result["suggestions"])
    return result



@app.post("/plan", response_model=RecipeResponse)
def plan(input: PlanInput):
    logger.info(
        "Received /plan request: base_recipe=%s",
        input.base_recipe
    )
    recipe = planner_agent.run(input.base_recipe)
    logger.info(
        "/plan response: recipe_title=%s, steps=%d",
        recipe.title,
        len(recipe.steps)
    )
    return recipe


@app.post("/recommend", response_model=RecommendOutput)
def recommend(input: RecommendInput):
    logger.info(
        "Received /recommend request: items=%s, diet=%s, recipe_count=%d",
        input.items,
        input.diet,
        input.recipe_count
    )

    result = planner_agent.recommend(
        input.items,
        input.diet,
        max_recipes=input.recipe_count
    )

    logger.info(
        "/recommend response: recipes_returned=%d",
        len(result["recipes"])
    )

    return result

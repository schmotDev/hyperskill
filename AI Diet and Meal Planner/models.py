from pydantic import BaseModel
from typing import List



class RecipeStep(BaseModel):
    step_number: int
    instruction: str

class RecipeResponse(BaseModel):
    title: str
    ingredients: List[str]
    steps: List[RecipeStep]


class RecommendInput(BaseModel):
    items: List[str]
    diet: str
    recipe_count: int = 5  # default to 5 if not provided

# ---------- Inputs ----------

class InventoryInput(BaseModel):
    items: List[str]


class DietInput(BaseModel):
    items: List[str]
    diet: str


class AskInput(BaseModel):
    items: List[str]
    diet: str


class PlanInput(BaseModel):
    base_recipe: str



# ---------- Outputs ----------

class InventoryResponse(BaseModel):
    usable_items: List[str]
    message: str


class DietResponse(BaseModel):
    compatible_items: List[str]
    suggested_recipe_ideas: List[str]

class RecommendOutput(BaseModel):
    recipes: List[RecipeResponse]
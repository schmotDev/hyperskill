from typing import List
from services.llm_client import LLMClient
from models import RecipeResponse, RecipeStep
from agents.manager_agent import ManagerAgent

class PlannerAgent:
    def __init__(self):
        self.manager_agent = ManagerAgent()
        self.llm = LLMClient()

    def run(self, base_recipe: str) -> RecipeResponse:
        prompt = (
            f"You are a professional chef and recipe writer.\n"
            f"Take the base recipe idea: '{base_recipe}'\n"
            "Create a complete, detailed recipe with:\n"
            "- title\n"
            "- ingredients list (only use ingredients from the base recipe if possible)\n"
            "- step-by-step cooking instructions\n\n"
            "Return ONLY valid JSON matching this structure:\n"
            "{\n"
            "  'title': str,\n"
            "  'ingredients': [str],\n"
            "  'steps': [{'step_number': int, 'instruction': str}]\n"
            "}"
        )

        result = self.llm.call_model_json(prompt)
        # Convert steps into RecipeStep objects
        steps = [RecipeStep(**step) for step in result.get("steps", [])]
        return RecipeResponse(
            title=result.get("title", base_recipe),
            ingredients=result.get("ingredients", []),
            steps=steps
        )

    def recommend(self, items: List[str], diet: str, max_recipes: int = 5) -> dict:
        """Generate multiple complete recipes by combining ManagerAgent (/ask) + /plan"""
        # Step 1: Get suggestions from ManagerAgent
        ask_result = self.manager_agent.run(items, diet)

        # Step 2: Take up to `max_recipes` suggestions
        base_recipes = ask_result.get("suggestions", [])[:max_recipes]

        # Step 3: Generate full recipes using run()
        full_recipes = [self.run(base_recipe) for base_recipe in base_recipes]

        return {"recipes": full_recipes}


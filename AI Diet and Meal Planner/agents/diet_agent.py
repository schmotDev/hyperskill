from services.llm_client import LLMClient
from typing import List
from models import DietResponse

class DietAgent:

    def __init__(self):
        self.llm = LLMClient()

    def run(self, items: List[str], diet: str) -> DietResponse:
        prompt = (
            "You are a professional diet planner.\n"
            f"Diet type: {diet}\n"
            "Given the following list of ingredients:\n"
            f"{items}\n\n"
            "Apply the dietary rules strictly.\n"
            "Return a JSON object with:\n"
            "- compatible_items: ingredients that comply with the diet\n"
            "- suggested_recipe_ideas: EXACTLY five diet-friendly recipe ideas "
            "using only compatible items\n\n"
            "Respond ONLY with valid JSON."
        )

        result = self.llm.call_model_json(prompt)
        return DietResponse(**result)
from services.llm_client import LLMClient
from typing import List
from models import InventoryResponse


class InventoryAgent:

    def __init__(self):
        self.llm = LLMClient()

    def run(self, items: List[str]) -> InventoryResponse:

        prompt = (
            "You are a kitchen assistant.\n"
            "Given the following JSON array of ingredients:\n"
            f"{items}\n\n"
            "Return a JSON object with:\n"
            "- usable_items: an array of ingredients that are non-empty, edible, "
            "and suitable for cooking (remove blanks, duplicates, or invalid items)\n"
            "- message: a short confirmation string\n\n"
            "Respond ONLY with valid JSON."
        )

        result = self.llm.call_model_json(prompt)
        return InventoryResponse(**result)
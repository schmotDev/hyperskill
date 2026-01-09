from typing import List, Dict
from agents.inventory_agent import InventoryAgent
from agents.diet_agent import DietAgent

class ManagerAgent:
    def __init__(self):
        self.inventory_agent = InventoryAgent()
        self.diet_agent = DietAgent()

    def run(self, items: List[str], diet: str) -> Dict:
        # Step 1: Clean/validate items via InventoryAgent
        usable_items = self.inventory_agent.run(items)

        # Step 2: Filter diet-friendly items via DietAgent
        diet_result = self.diet_agent.run(usable_items, diet)
        compatible_items = diet_result.compatible_items
        suggestions = diet_result.suggested_recipe_ideas

        # Step 3: Combine results
        return {
            "usable_items": usable_items,
            "diet_filtered": compatible_items,
            "suggestions": suggestions
        }

from openai import OpenAI
import os
import dotenv
from typing import Dict, Any
import json

dotenv.load_dotenv()


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_url = os.getenv("OPENAI_BASE_URL")
        #self.model = "gpt-4o-mini"
        self.model = "xiaomi/mimo-v2-flash:free"

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
        )

    def call_model_json(self, prompt: str) -> Dict[str, Any]:

        messages = [{"role": "user", "content": prompt}]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            response_format={"type": "json_object"},
        )

        message_content = response.choices[0].message.content

        # Parse JSON safely
        try:
            parsed_json = json.loads(message_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse model output as JSON: {message_content}") from e

        return parsed_json
import logging
from typing import Dict, List

import openai
from openai import OpenAI


class LLMClient:
    """Manages communication with the LLM provider."""

    def __init__(self, api_key: str) -> None:
        """Initialize LLM client using OpenAI."""
        self.api_key: str = api_key
        self.client = OpenAI(api_key=api_key)

    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """Get a response from the LLM (OpenAI)."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=2048,
                top_p=1.0,
            )
            return response.choices[0].message.content
        except openai.APIError as e:
            error_message = f"Error getting LLM response: {e}"
            logging.error(error_message)
            return f"I encountered an error: {error_message}. Please try again."

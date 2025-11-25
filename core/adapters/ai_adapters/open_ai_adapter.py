import openai
from django.conf import settings

from core.adapters.ai_adapters.base import AIAgentAdapter


class OpenAIAdapter(AIAgentAdapter):
    def __init__(self):
        self.model = 'gpt-3.5-turbo'

        self.agent = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    def answer(self, prompt: str) -> str:
        response = self.agent.chat.completions.create(
            model=self.model,
            messages=[
                {'role': 'system', 'content': prompt},
            ],
        )
        return response.choices[0].message.content

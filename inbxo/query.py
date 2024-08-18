from diskcache import Cache
import openai
import os
import json
from typing import Any
import slugify

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")


class Query:

    def __init__(self, question: str, response_format: Any, model_name="gpt-4o-mini"):
        self.question = question
        self.response_format = response_format
        self.model_name = model_name
        self.client = openai.OpenAI()

        slug_name = slugify.slugify(question)
        self.cache = Cache(f"cache/chatgpt_{model_name}/{slug_name}")

    def __call__(self, target: str, force: bool = False):
        if target not in self.cache or force:
            self.cache[target] = self.compute(target)

        return self.cache[target]

    def compute(self, target: str):

        print(f"{self.question} : {target}")

        completion = self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.question},
                {"role": "user", "content": target},
            ],
            response_format=self.response_format,
        )

        message = completion.choices[0].message

        if not message.parsed:
            raise ValueError(f"Failed: {message.refusal}")

        js = message.parsed.json()
        js = json.loads(js)

        return js

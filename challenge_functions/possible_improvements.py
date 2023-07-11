import openai
import os
import asyncio
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

openai.api_key = os.getenv("OPEN_AI_API_KEY")

GPT_MODEL = "gpt-3.5-turbo"

PROMPT_BEGINNING = """Analyze the following enumerated list of customer reviews for a restaurant and provide concise recommendations to improve the service:\n"""


def get_improvements(selected_list, df):
    if not selected_list:
        return

    selected_rows = df.iloc[selected_list, :]
    selected_rows_list = selected_rows["body"].to_list()

    prompt = PROMPT_BEGINNING

    for i, review in enumerate(selected_rows_list, 1):
        prompt += f"{i}. {review}\n"

    response = openai.ChatCompletion.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=GPT_MODEL,
        temperature=0,
    )

    return response["choices"][0]["message"]["content"]

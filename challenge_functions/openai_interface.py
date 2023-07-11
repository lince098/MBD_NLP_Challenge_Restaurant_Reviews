import openai
import os
import asyncio
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

openai.api_key = os.getenv("OPEN_AI_API_KEY")

GPT_MODEL = "gpt-3.5-turbo"


async def summarize(selected_list, df):
    if not selected_list:
        return

    PROMPT_BEGINNING = """Please analyze this restaurant review and provide a concise summary highlighting its key points:\n"""

    selected_rows = df.iloc[selected_list, :]
    selected_rows_list = selected_rows["body"].to_list()

    requests_prompts = [PROMPT_BEGINNING + msg for msg in selected_rows_list]

    responses = await asyncio.gather(
        *[__send_request(prompt) for prompt in requests_prompts]
    )

    logger.debug(responses)
    logger.debug(selected_rows_list)
    return [
        {"Review": msg, "Summary": response}
        for msg, response in zip(selected_rows_list, responses)
    ]


def get_improvements(selected_list, df):
    if not selected_list:
        return

    PROMPT_BEGINNING = """Analyze the following enumerated list of customer reviews for a restaurant and provide concise recommendations to improve the service:\n"""

    selected_rows = df.iloc[selected_list, :]
    selected_rows_list = selected_rows["body"].to_list()

    prompt = PROMPT_BEGINNING

    for i, review in enumerate(selected_rows_list, 1):
        prompt += f"{i}. {review}\n"

    response = asyncio.run(__send_request(prompt))

    return response


async def get_translations(selected_list, df, target_language):
    if not selected_list:
        return

    PROMPT_BEGINNING = f"""Translate the following text to {target_language}:\n"""

    selected_rows = df.iloc[selected_list, :]
    selected_rows_list = selected_rows["body"].to_list()

    requests_prompts = [PROMPT_BEGINNING + msg for msg in selected_rows_list]

    responses = await asyncio.gather(
        *[__send_request(prompt) for prompt in requests_prompts]
    )

    logger.debug(responses)
    logger.debug(selected_rows_list)
    return [
        {"Review": msg, "Translation": response}
        for msg, response in zip(selected_rows_list, responses)
    ]


async def __send_request(prompt):
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

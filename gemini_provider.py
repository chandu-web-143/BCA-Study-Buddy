import time
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

load_dotenv()
_client = genai.Client()

DEFAULT_MODELS = ["gemini-3.8-flash", "gemini-3.5-flash"]


class ProviderError(Exception):
    """Raised when no model could answer."""


def generate(prompt, system=None, models=None, retries=3):
    models = models or DEFAULT_MODELS
    config = types.GenerateContentConfig(system_instruction=system) if system else None

    for model in models:
        for attempt in range(retries):
            try:
                r = _client.models.generate_content(
                    model=model, contents=prompt, config=config
                )
                usage = r.usage_metadata
                return {
                    "text": r.text,
                    "model": model,
                    "input_tokens": usage.prompt_token_count if usage else None,
                    "output_tokens": usage.candidates_token_count if usage else None,
                }
            except errors.ServerError:
                print(f"{model} busy, retry {attempt + 1}...")
                time.sleep(3)
            except errors.ClientError as e:
                print(f"{model} problem: {e}")
                break

    raise ProviderError("No model worked. Read the messages above to see why.")

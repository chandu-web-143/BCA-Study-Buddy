import time
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

load_dotenv()

TIMEOUT_MS = 30000  # 30 seconds, this library counts in milliseconds
_client = genai.Client(http_options=types.HttpOptions(timeout=TIMEOUT_MS))

DEFAULT_MODELS = ["gemini-3.8-flash", "gemini-3.5-flash"]


class ProviderError(Exception):
    """Raised when no model could answer."""


class AuthError(ProviderError):
    """Raised when the API key is missing, invalid or not allowed."""


def generate(prompt, system=None, models=None, retries=3):
    models = models or DEFAULT_MODELS
    config = types.GenerateContentConfig(system_instruction=system) if system else None
    last_problem = "unknown"

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

            except errors.ClientError as e:
                code = getattr(e, "code", None)
                if code in (400, 401, 403) and "API key" in str(e):
                    raise AuthError("Your API key is missing or invalid. Check your .env file.")
                if code == 429:
                    last_problem = "rate limit"
                    print(f"{model}: rate limit, waiting 10 seconds...")
                    time.sleep(10)
                    continue  # retry the same model
                last_problem = f"{model}: request problem (code {code})"
                print(last_problem)
                break  # try the next model

            except errors.ServerError:
                last_problem = f"{model} busy"
                print(f"{model} busy, retry {attempt + 1}...")
                time.sleep(3)

            except Exception as e:  # timeouts and network problems
                last_problem = f"{model}: network or timeout ({type(e).__name__})"
                print(last_problem)
                time.sleep(3)

    raise ProviderError(f"No model worked. Last problem: {last_problem}")
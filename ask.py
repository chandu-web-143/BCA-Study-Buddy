import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()
client = genai.Client()

MODELS = ["gemini-3.8-flash", "gemini-3.5-flash"]
PROMPT = "Explain what a database is in 3 simple lines for a BCA student."

def ask(prompt):
    for model in MODELS:
        for attempt in range(3):
            try:
                response = client.models.generate_content(model=model, contents=prompt)
                return response.text
            except errors.ServerError:
                print(f"{model} busy, retry {attempt + 1}...")
                time.sleep(3)
            except errors.ClientError as e:
                print(f"{model} problem: {e}")
                break  # try the next model
        return "No model worked. Read the messages above to see why."

print(ask(PROMPT))
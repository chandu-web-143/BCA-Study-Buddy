import time
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

load_dotenv()
client = genai.Client()

MODELS = ["gemini-3.8-flash", "gemini-3.5-flash"]

SYSTEM = """You are a friendly tutor for BCA students at Bangalore University.
Explain in simple English with one small example.
Keep answers under 150 words unless asked for more.
End every answer with one quick question to check understanding.
If you are not sure about the exact syllabus, say so and do not invent it."""

def ask(question):
    config = types.GenerateContentConfig(system_instruction=SYSTEM)
    for model in MODELS:
        for attempt in range(3):
            try:
                r = client.models.generate_content(
                    model=model, contents=question, config=config
                )
                return r.text
            except errors.ServerError:
                print(f"{model} busy, retry {attempt + 1}...")
                time.sleep(3)
            except errors.ClientError as e:
                print(f"{model} problem: {e}")
                break
    return "No model worked. Read the messages above to see why."

print("BCA Study Buddy. Type your question, or 'exit' to quit.")
while True:
    q = input("\nYou: ").strip()
    if q.lower() == "exit":
        break
    if not q:
        continue
    print("\nTutor:", ask(q))
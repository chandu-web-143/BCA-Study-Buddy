from gemini_provider import generate, ProviderError

SYSTEM = """You are a friendly tutor for BCA students at Bangalore University.
Explain in simple English with one small example.
Keep answers under 150 words unless asked for more.
End every answer with one quick question to check understanding.
If you are not sure about the exact syllabus, say so and do not invent it."""


def ask(question):
    try:
        return generate(question, system=SYSTEM)["text"]
    except ProviderError as e:
        return str(e)


def quiz(topic):
    prompt = (
        f"Make a 5-question multiple choice quiz on '{topic}' for a BCA student. "
        "Give 4 options (A to D) per question. "
        "Put all the answers with a one-line explanation at the very end."
    )
    return ask(prompt)


print("BCA Study Buddy. Type your question, or 'exit' to quit.")
while True:
    q = input("\nYou: ").strip()
    if q.lower() == "exit":
        break
    if not q:
        continue
    if q.lower().startswith("quiz:"):
        print("\nQuiz:", quiz(q[5:].strip()))
    else:
        print("\nTutor:", ask(q))
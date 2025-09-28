import openai, os
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_ai(question):
    prompt = f"You are an AI assistant helping citizens with safety, health, education, jobs. Question: {question}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

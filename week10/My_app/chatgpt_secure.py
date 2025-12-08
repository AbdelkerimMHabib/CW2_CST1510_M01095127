from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('OpenAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=api_key)
messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

print("ChatGPT Console Chat (type 'quit' to exit)")
print("-" * 50)

while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    messages.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    assistant_message = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_message})
    print(f"AI: {assistant_message}\n")


from openai import OpenAI
client = OpenAI(api_key="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")


# Initialize messages list with system message
messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

print("ChatGPT with Memory. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break# Add user message to history
    messages.append({"role": "user", "content": user_input})

   
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages  
    )

    # Extract AI response
    ai_message = response.choices[0].message.content

    # Add AI response to history
    messages.append({"role": "assistant", "content": ai_message})

    print(f"AI: {ai_message}\n")

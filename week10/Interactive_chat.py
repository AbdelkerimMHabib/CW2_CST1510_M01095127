from openai import OpenAI
client= OpenAI(api_key= "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")

print("ChatGPT Console Chat")
print("Type 'quit' to exit\n")

while True:
    user_input = input("You:")
    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    response= client.chat.completions.create(
        model="gpt-4o-mini",
        messages= [{"role": "user", "content": user_input}]
    )

    answer= response.choices[0].message.content
    print(f"AI: {answer}\n")
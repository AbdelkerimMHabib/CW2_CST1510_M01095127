from openai import OpenAI

# Initialize the OpenAI client with your API key
client = OpenAI(api_key="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")
  

# Make a simple API call
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! What is AI?"}
    ]
)

# Print the response
print(completion.choices[0].message.content)

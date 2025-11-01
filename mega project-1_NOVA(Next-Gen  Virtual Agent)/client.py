from openai import OpenAI

client = OpenAI(
    api_key="NA",  # your Perplexity API key
    base_url="https://api.perplexity.ai"  # direct Perplexity endpoint
)

response = client.chat.completions.create(
    model="sonar-pro",  # choose an appropriate Perplexity model
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Nova, skilled like Alexa or Google Assistant."},
        {"role": "user", "content": "who is Virat Kohli?"}
    ],
    max_tokens = 75 
)

print(response.choices[0].message.content)
 
from openai import OpenAI

client = OpenAI()  # la clé est lue automatiquement

response = client.responses.create(
    model="gpt-5.2",
    input="Bonjour, explique-moi l’API OpenAI"
)

print(response.output_text)

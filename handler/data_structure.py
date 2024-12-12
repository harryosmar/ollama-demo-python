from ollama import chat
from pydantic import BaseModel

class Country(BaseModel):
  name: str
  capital: str
  languages: list[str]


def extract_country_data(text: str) -> Country:
    response = chat(
        messages=[
            {
                'role': 'user',
                'content': text,
            }
        ],
        model='llama3.2',
        format=Country.model_json_schema(),
    )
    json_data = response.message.content
    if json_data is not None:
        return Country.model_validate_json(json_data)
    else:
        return Country.model_validate_json('{}')  # Using an empty JSON object as default


# Example usage
country_data = extract_country_data('Tell me about Canada.')
print(country_data)
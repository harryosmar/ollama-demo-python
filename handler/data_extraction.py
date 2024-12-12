from ollama import chat
from pydantic import BaseModel

class Pet(BaseModel):
    name: str
    animal: str
    age: int
    color: str | None
    favorite_toy: str | None

class PetList(BaseModel):
    pets: list[Pet]

def extract_pet_data(text: str) -> PetList:
    response = chat(
        messages=[
            {
                'role': 'user',
                'content': text,
            }
        ],
        model='llama3.2',
        format=PetList.model_json_schema(),
    )
    json_data = response.message.content
    if json_data is not None:
        return PetList.model_validate_json(json_data)
    else:
        return PetList.model_validate_json('{}')  # Using an empty JSON object as default
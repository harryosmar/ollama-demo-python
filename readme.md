
## Install Ollama

Download ollama [https://ollama.com/download](https://ollama.com/download), choose your platform and click on download.

## Check ollama installation

Run the following command in the terminal:

```shell
ollama --version
```

example output:

```shell
ollama version is 0.5.1
```

## Start ollama server

Run the following command in the terminal:

```shell
ollama serve
```

by default, ollama will start on port 11434, open your browser and go to [http://localhost:11434](http://localhost:11434)  

## Download models llama3.2

We choose [llama3.2](https://ollama.com/library/llama3.2) because it is popular and smallest model with 2.0 GB size. Imagine you can run LLM on your local machine. This model only contains 3b parameters. This model outperform many of the available open source and closed chat models on common industry benchmarks.

Run the following command in the terminal:

```shell
ollama run llama3.2
```

Check if the model is downloaded

```shell
ollama list
```

Output:

```shell
NAME                       ID              SIZE      MODIFIED        
llama3.2:latest            a80c4f17acd5    2.0 GB    n weeks ago
```

## Run using curl directly to ollama server

### Use case 1 : extract country data

- Input country name
- Output country data as json schema 
```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "capital": {
      "type": "string"
    },
    "languages": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": [
    "name",
    "capital",
    "languages"
  ]
}
```

#### Request

Run the following command in the terminal:

json schema above included in the request in field `format`

- input text : "Tell me about Canada."

```shell
curl --location 'http://127.0.0.1:11434/api/chat' \
--header 'Content-Type: application/json' \
--data '{
  "model": "llama3.2",
  "messages": [{"role": "user", "content": "Tell me about Canada."}],
  "stream": false,
  "format": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string"
      },
      "capital": {
        "type": "string"
      },
      "languages": {
        "type": "array",
        "items": {
          "type": "string"
        }
      }
    },
    "required": [
      "name",
      "capital",
      "languages"
    ]
  }
}'
```

#### Response

output:

```json
{
    "model": "llama3.2",
    "created_at": "2024-12-12T07:47:22.184905Z",
    "message": {
        "role": "assistant",
        "content": "{ \"capital\": \"Ottawa\", \"languages\": [\"English\", \"French\"], \"name\":\"Canada\" }"
    },
    "done_reason": "stop",
    "done": true,
    "total_duration": 1232600000,
    "load_duration": 33616458,
    "prompt_eval_count": 30,
    "prompt_eval_duration": 495000000,
    "eval_count": 29,
    "eval_duration": 700000000
}
``` 

see field `message.content` using the same json schema as above

```json
{
  "capital": "Ottawa",
  "languages": [
    "English",
    "French"
  ],
  "name": "Canada"
}
``` 


### Use case 2 : extract pets data

This is a more complex example of json schema

- Input : pets description
- Output : pets data as json schema 
```json
{
  "$defs": {
    "Pet": {
      "properties": {
        "age": {
          "title": "Age",
          "type": "integer"
        },
        "animal": {
          "title": "Animal",
          "type": "string"
        },
        "color": {
          "anyOf": [
            {
              "const": "black"
            },
            {
              "const": "grey"
            }
          ],
          "title": "Color"
        },
        "favorite_toy": {
          "anyOf": [
            {
              "const": "yarn"
            },
            {
              "const": "tennis balls"
            }
          ],
          "title": "Favorite Toy"
        },
        "name": {
          "title": "Name",
          "type": "string"
        }
      },
      "required": [
        "name",
        "animal",
        "age",
        "color",
        "favorite_toy"
      ],
      "title": "Pet",
      "type": "object"
    }
  },
  "properties": {
    "pets": {
      "items": {
        "$ref": "#/$defs/Pet"
      },
      "title": "Pets",
      "type": "array"
    }
  },
  "required": [
    "pets"
  ],
  "title": "PetList",
  "type": "object"
}
```

#### Request

Run the following command in the terminal:

- input text : "I have two pets. A cat named Luna who is 5 years old and loves playing with yarn. She has grey fur. I also have a 2 year old black cat named Loki who loves tennis balls.

```shell
curl --location 'http://127.0.0.1:11434/api/chat' \
--header 'Content-Type: application/json' \
--data '{
  "format": {
    "$defs": {
      "Pet": {
        "properties": {
          "age": {
            "title": "Age",
            "type": "integer"
          },
          "animal": {
            "title": "Animal",
            "type": "string"
          },
          "color": {
            "anyOf": [
              { "const": "black" },
              { "const": "grey" }
            ],
            "title": "Color"
          },
          "favorite_toy": {
            "anyOf": [
              { "const": "yarn" },
              { "const": "tennis balls" }
            ],
            "title": "Favorite Toy"
          },
          "name": {
            "title": "Name",
            "type": "string"
          }
        },
        "required": [
          "name",
          "animal",
          "age",
          "color",
          "favorite_toy"
        ],
        "title": "Pet",
        "type": "object"
      }
    },
    "properties": {
      "pets": {
        "items": {
          "$ref": "#/$defs/Pet"
        },
        "title": "Pets",
        "type": "array"
      }
    },
    "required": [
      "pets"
    ],
    "title": "PetList",
    "type": "object"
  },
  "messages": [
    {
      "content": "I have two pets. A cat named Luna who is 5 years old and loves playing with yarn. She has grey fur. I also have a 2 year old black cat named Loki who loves tennis balls.",
      "role": "user"
    }
  ],
  "model": "llama3.2",
  "stream": false,
  "tools": []
}
'
```

#### Response

output:

```json
{
    "model": "llama3.2",
    "created_at": "2024-12-12T08:32:37.316804Z",
    "message": {
        "role": "assistant",
        "content": "{ \"pets\": [ { \"age\": 5, \"animal\": \"cat\", \"color\": \"grey\", \"favorite_toy\": \"yarn\" , \"name\": \"Luna\"}, { \"age\": 2, \"animal\": \"cat\", \"color\": \"black\", \"favorite_toy\": \"tennis balls\" , \"name\": \"Loki\"}] }"
    },
    "done_reason": "stop",
    "done": true,
    "total_duration": 7159731958,
    "load_duration": 829545916,
    "prompt_eval_count": 68,
    "prompt_eval_duration": 4620000000,
    "eval_count": 82,
    "eval_duration": 1697000000
}
```

see field `message.content` using the same json schema as above

```json
{
  "pets": [
    {
      "age": 5,
      "animal": "cat",
      "color": "grey",
      "favorite_toy": "yarn",
      "name": "Luna"
    },
    {
      "age": 2,
      "animal": "cat",
      "color": "black",
      "favorite_toy": "tennis balls",
      "name": "Loki"
    }
  ]
}
```


## Run demo python app

Recommend to use python 3.10.* with venv

### Create venv

Clone this repository

```shell
git clone https://github.com/harryosmar/ollama-demo-python.git
```

Run the following command in the terminal:

```shell
cd ollama-demo-python

python3 -m venv venv
```

### Activate venv

Run the following command in the terminal:

```shell
source ./venv/bin/activate
```

### Install requirements

Run the following command in the terminal:      

```shell
pip install -r requirements.txt
```

- [Flask](https://flask.palletsprojects.com/en/2.3.x/) used as api framework
- [pydantic](https://pydantic-docs.helpmanual.io/) used for data validation, create json schema from python class

### Run app

Run the following command in the terminal:

```shell
flask --app main run
```

### endpoints

[swagger](http://127.0.0.1:5000/apidocs/)
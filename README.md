
# ai-helper

A small Python helper library for working with artificial intelligence providers that use the OpenAI schema.

---


## Installation

```bash
pip install git+https://git.jackhuey.com/ai-helper.git
```

---

## Usage

### Basic usage
```python
import ai

openai = ai.Provider("your-api-key")

model = ai.AI(openai, "gpt-4.1-mini", "You are a helpful AI assistant.")

while True:
    prompt = input("You: ")
    response = model.prompt(prompt)
    print(response)
```
---

### Using a different provider
If you want to use a provider other than OpenAI (e.g. GitHub models), pass it as a string to ai.Provider.

```python
github = ai.Provider("your-api-key", baseUrl="https://models.github.ai/inference")
```
---

### Tool Calls
To enable tool calls, pass a list of tool definitions to ai.AI.
If a tool takes no parameters, you may pass an empty list.

```python
model = ai.AI(provider, "gpt-4.1-mini", "You are a helpful AI assistant.",
    {
        "name": "web",
        "description": "Browse the web.",
        "parameters": [
            {
                "url": {
                    "type": "string",
                    "description": "The URL of the page you want to visit."
                }
            }
        ]
    }
)
```
If the model uses a tool call, ai.AI.prompt will return a list of instances of ai.AI.ToolCall.

ai.AI.ToolCall has the attributes name, a string of the name (e.g. "web" from the example above), and arguments, a dictionary of the parameters passed (e.g. {"url": "google.com"} from the example above).

ai.AI.ToolCall has the method respond(), which takes one parameter, the response as a string. You must call respond for all tool calls returned by ai.AI.prompt.

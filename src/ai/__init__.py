from openai import OpenAI
import ast

class Provider:
    def __init__(self, apiKey, baseUrl=None):
        self.apiKey = apiKey
        self.baseUrl = baseUrl

class AI:
    def __init__(self, provider, model, systemPrompt, tools=[]):
        if provider.baseUrl:
            self.client = OpenAI(api_key=provider.apiKey, base_url=provider.baseUrl)
        else:
            self.client = OpenAI(api_key=provider.apiKey)
        self.model = model
        self.history = [{"role": "system", "content": systemPrompt}]
        self.tools = []

        for tool in tools:
            parameters = {}
            for parameter in tool["parameters"]:
                parameters = {
                    "type": "object",
                    "properties": {
                        parameter: {"type": tool["parameters"][parameter]["type"], "description": tool["parameters"][parameter]["description"]}
                    },
                "required": list(tool["parameters"].keys())
                }

            self.tools.append({
            "type":"function",
            "function":{
                "name": tool["name"],
                "description": tool["description"],
                "parameters": parameters
            }
        })

    class ToolCall:
        def __init__(self, model, name, arguments, id):
            self.model = model
            self.name = name
            self.arguments = ast.literal_eval(arguments)
            self.id = id

        def respond(self, response):
            self.model.history.append({"role": "tool", "tool_call_id": self.id, "content": response})

    def prompt(self, prompt):
        self.history.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(model=self.model, 
messages=self.history, tools=self.tools).choices[0].message
        if response.tool_calls:
            self.history.append({"role": "assistant", "tool_calls": [tc.model_dump() for tc in response.tool_calls], "content": None})
            return [self.ToolCall(self, toolCall.function.name, toolCall.function.arguments, toolCall.id) for toolCall in response.tool_calls]
        else:
            self.history.append({"role": "assistant", "content": response.content})
            return response.content



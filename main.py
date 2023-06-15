import openai
import os
import dotenv
import json
from colorama import Fore, Style

import function_execution

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
extra_comments = False

messages = []
"""
function structure:
"name": "Name of the function, it will be used to call it, use snake_case",
"description": "Description of what do the function",
"parameters": {
    "type": "object",
    "properties": {
        "parameter_name": {
            "type": "type of the parameter",
            "description": "Description of the parameter" (optional),
            "enum": ["list", "of", "possible", "values"] (optional)
        },
        ...
    },
    "required": ["parameter_name", ...] (optional)
}

"""
functions = [
    {
        "name": "get_course_info",
        "description": "get the information of a course/nrc (nrc must be a 4 digit number)",
        "parameters": {
            "type": "object",
            "properties": {
                "nrc": {
                    "type": "integer",
                    "description": "The nrc of the course, e.g. 2935"
                },
                "request": {
                    "type": "string",
                    "enum": ["teacher", "department", "subject", "group", "name", "available places", "enrolled amount", "schedule", "all"],
                }
            },
            "required": ["nrc", "request"]
        }
    }
]

while True:
    text_input = input("You: ")

    if text_input == "exit":
        break

    messages.append({"role": "user", "content": text_input})

    function_call_end = False
    not_end = True

    while not_end or function_call_end:
        not_end = False
        function_call_end = False

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto",
            max_tokens=300,
            stream=True
        )

        actual_content = ""
        actual_function_name = ""
        actual_function_arguments = ""

        for message in response:
            # Function call
            if "function_call" in message["choices"][0]["delta"]:
                if "name" in message["choices"][0]["delta"]["function_call"]:
                    actual_function_name = message["choices"][0]["delta"]["function_call"]["name"]
                    actual_function_arguments = ""
                    if extra_comments:
                        print(f'Function call({message["choices"][0]["delta"]["function_call"]["name"]}) : ', end='')

                if "arguments" in message["choices"][0]["delta"]["function_call"]:
                    actual_function_arguments += message["choices"][0]["delta"]["function_call"]["arguments"]
                    if extra_comments:
                        print(message["choices"][0]["delta"]["function_call"]["arguments"], end='')

            # Content of the message
            if "content" in message["choices"][0]["delta"]:
                if message["choices"][0]["delta"]["content"] is not None:
                    actual_content += message["choices"][0]["delta"]["content"]
                    print(message["choices"][0]["delta"]["content"], end='')

            # Conversation end condition
            if message["choices"][0]["finish_reason"] is not None:
                if message["choices"][0]["finish_reason"] == "function_call":
                    function_call_end = True
                elif message["choices"][0]["finish_reason"] == "length":
                    not_end = True
                elif message["choices"][0]["finish_reason"] == "stop":
                    print("\n\nStop conversation")
                break

        if function_call_end:
            messages.append(
                {
                    "role": "assistant",
                    "content": text_input,
                    "function_call": {
                        "name": actual_function_name,
                        "arguments": actual_function_arguments
                    }
                }
            )

            actual_function_arguments = json.loads(actual_function_arguments)

            # TODO: Function Execution - CHANGE FOR EACH FUNCTION
            if actual_function_name == "get_course_info":
                nrc = actual_function_arguments["nrc"]
                request = actual_function_arguments["request"]
                result = function_execution.get_course_info(nrc, request)
            else:
                result = "{'error': 'Function not found'}"

            print(f'{Fore.BLUE} Executed function {actual_function_name} with arguments {actual_function_arguments} {Style.RESET_ALL}', end='')
            messages.append({"role": "function", "name": actual_function_name, "content": result})
        else:
            messages.append({"role": "assistant", "content": text_input})

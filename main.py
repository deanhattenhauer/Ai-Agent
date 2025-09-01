import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, schema_get_file_content, schema_write_file
from functions.run_python import schema_run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

if len(sys.argv) < 2:
    print("error: no prompt provided")
    sys.exit()

user_prompt = sys.argv[1]
if "--verbose" in sys.argv:
    print("User prompt:", user_prompt)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file
    ]
) 

for _ in range(20):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.function_calls:
            for fc in response.function_calls:
                result = call_function(fc, verbose="--verbose" in sys.argv)
                messages.append(types.Content(role="user", parts=result.parts))
        else:
            print("Final response:")
            print(response.text)
            break
    except Exception as e:
        if "--verbose" in sys.argv:
            print(f"Error: {e}")
        break
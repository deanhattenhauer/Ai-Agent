import os
from google.genai import types

def get_files_info(working_directory, directory="."):

    working_abs_path = os.path.abspath(working_directory)
    target_abs_path = os.path.join(working_directory, directory)
    full_path = os.path.abspath(target_abs_path)
    
    try:
        if not full_path.startswith(working_abs_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
    
        directory_items = os.listdir(full_path)

        results = []
    
        for item in directory_items:
            item_full_path = os.path.join(full_path, item)

            file_size = os.path.getsize(item_full_path)
            is_dir = os.path.isdir(item_full_path)
            
            formatted_items = f'- {item}: file_size={file_size} bytes, is_dir={is_dir}'
            results.append(formatted_items)
    except Exception as e:
        return f'Error: {str(e)}'

    return '\n'.join(results)

def get_file_content(working_directory, file_path):

    working_abs_path = os.path.abspath(working_directory)
    target_abs_path = os.path.join(working_directory, file_path)
    full_path = os.path.abspath(target_abs_path)
    
    try:
        if not full_path.startswith(working_abs_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000

        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            extra_char = f.read(1)

            if extra_char != "":
                file_content_string += f'[...File \"{file_path}\" truncated at {MAX_CHARS} characters]'

        return file_content_string

    except Exception as e:
        return f'Error: {str(e)}'

def write_file(working_directory, file_path, content):

    working_abs_path = os.path.abspath(working_directory)
    target_abs_path = os.path.join(working_directory, file_path)
    full_path = os.path.abspath(target_abs_path)

    try:
        if not full_path.startswith(working_abs_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        create_dir = os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {str(e)}'
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a single file within the working directory. If the file exceeds 10,000 characters, the returned content is truncated and a truncation note is appended.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file relative to the working directory (e.g., 'main.py', 'pkg/util.py')."
            ),
        },
        required=["file_path"]
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes (creating or overwriting) a single file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file relative to the working directory (e.g., 'main.py', 'pkg/util.py')."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text to write into the file."
            ),
        },
        required=["file_path", "content"]
    ),
)
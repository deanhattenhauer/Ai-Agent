import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    
    if args is None:
        args = []

    working_abs_path = os.path.abspath(working_directory)
    target_abs_path = os.path.join(working_directory, file_path)
    full_path = os.path.abspath(target_abs_path)

    try:
        if not full_path.startswith(working_abs_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        
        if not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        completed_process = subprocess.run(["python", full_path, *args], timeout=30, capture_output=True, cwd=working_directory)

        stdout_str = completed_process.stdout.decode() if completed_process.stdout else ""
        stderr_str = completed_process.stderr.decode() if completed_process.stderr else ""  
        
        if not stdout_str and not stderr_str:
            return 'No output produced.'
        
        output_parts = []
        if stdout_str:
            output_parts.append(f"STDOUT: {stdout_str}")
        if stderr_str:
            output_parts.append(f"STDERR: {stderr_str}")
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")

        return "\n".join(output_parts)
                
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory with optional CLI arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of string arguments to pass to the script.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)
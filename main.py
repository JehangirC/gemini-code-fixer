import time
import json
import os
from script_executor import execute_script
from traceback_parser import parse_traceback_with_gemini, extract_python_files_from_traceback
from file_handler import get_file_contents, update_script
from fix_suggester import suggest_fix_with_ai

def write_full_execution_log(log_data, log_file="full_execution_log.json"):
    """
    Writes the complete execution log to a JSON file.

    Args:
        log_data: A list of dictionaries, where each dictionary represents the context of an iteration.
        log_file: The path to the log file.
    """

    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=4)

    print(f"Full execution log saved to: {log_file}")

def main():
    script_path = "script.py"
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")  # or replace with your GCP project ID
    model_name = "gemini-2.0-flash-001"  # Or your preferred model
    max_iterations = 10
    iteration = 0
    full_log_data = []  # List to store the execution context of each iteration

    while iteration < max_iterations:
        iteration += 1
        print(f"\nIteration: {iteration}")

        success, output, stack_trace = execute_script(script_path)

        # Initialize parsed_traceback, ai_response, and file_contents to None
        parsed_traceback = None
        ai_response = None
        file_contents = {}

        if not success:
            print("Script execution failed!")
            print("Stack Trace:\n", stack_trace)

            parsed_traceback = parse_traceback_with_gemini(stack_trace, project_id, model_name)
            print("Parsed Traceback:\n", parsed_traceback)

            python_files = extract_python_files_from_traceback(parsed_traceback)
            print("Python files involved:\n", python_files)

            file_contents = get_file_contents(python_files)

            ai_response = suggest_fix_with_ai(script_path, stack_trace, file_contents, project_id, model_name)

            if ai_response:
                print("\nAI Suggested Fix:")
                print(json.dumps(ai_response, indent=2))

                if "full_corrected_script" in ai_response:
                    update_script(script_path, ai_response["full_corrected_script"])
                    print(f"Script updated with AI's suggestion. Retrying...")
                    time.sleep(2)
                else:
                    print("AI did not provide a 'full_corrected_script'. Cannot update script.")
            else:
                print("AI could not provide a fix.")
        else:
            print("Script executed successfully!")
            print("Output:\n", output)

        iteration_context = {
            "iteration": iteration,
            "success": success,
            "output": output,
            "stack_trace": stack_trace,
            "parsed_traceback": parsed_traceback,
            "ai_response": ai_response,
            "file_contents": file_contents,
        }

        full_log_data.append(iteration_context)

        write_full_execution_log(full_log_data)

        if success:
            break

    if iteration == max_iterations:
        print(f"\nReached maximum iterations ({max_iterations}). Script may not be fully corrected.")

if __name__ == "__main__":
    main()

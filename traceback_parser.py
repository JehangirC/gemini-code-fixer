from google import genai
from google.genai import types
import json

def parse_traceback_with_gemini(stack_trace, project_id, model_name="gemini-2.0-flash-exp"):
    """
    Parses a Python stack trace using an AI model to extract files and errors.

    Args:
      stack_trace: The stack trace string.
      project_id: Your GCP project ID.
      model_name: The name of the AI model to use.

    Returns:
      A list of dictionaries, each containing "element" (file or error) and "content".
    """

    client = genai.Client(
        vertexai=True,
        project=project_id,
        location="us-central1"
    )

    model = model_name
    message = f'''
    Given this stack trace, output a list of all files and errors involved in the trace
    Error Output:
    {stack_trace}
    '''

    contents = [
        types.Content(
            role="user",
            parts=[{"text": message}]
        )
    ]

    response_schema = {
        "type": "ARRAY",
        "items": {
            "type": "OBJECT",
            "properties": {
                "element": {
                    "type": "STRING",
                    "description": "file or error"
                },
                "content": {
                    "type": "STRING"
                }
            }
        }
    }

    generate_content_config = types.GenerateContentConfig(
        temperature=0,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        safety_settings=[types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="OFF"
        )],
        response_mime_type="application/json",
        response_schema=response_schema,
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        print("Error decoding AI response as JSON.")
        return []

def extract_python_files_from_traceback(parsed_traceback):
    """
    Extracts Python file paths from the AI-parsed traceback.

    Args:
      parsed_traceback: Output from parse_traceback_with_ai.

    Returns:
      A set of unique Python file paths.
    """
    python_files = set()
    for item in parsed_traceback:
        if item["element"] == "file":
            if "content" in item.keys():
                content = item["content"]
                python_files.add(content)
    return python_files

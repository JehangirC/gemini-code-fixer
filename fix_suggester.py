from google import genai
from google.genai import types
import json

def suggest_fix_with_ai(original_script, stack_trace, file_contents, project_id, model_name="gemini-2.0-flash-exp"):
    """
    Sends the original script, stack trace, and file contents to an AI
    to suggest a fix.

    Args:
      original_script: Path to the original script.
      stack_trace: The stack trace string.
      file_contents: A dictionary of file paths and their contents.
      project_id: Your GCP project ID.
      model_name: The name of the AI model.

    Returns:
      The AI's response as a JSON object (if successful) or None.
    """

    client = genai.Client(
        vertexai=True,
        project=project_id,
        location="us-central1"
    )

    model = model_name

    # Format the prompt
    prompt = f"""
    You are a coding assistant tasked with fixing errors in Python scripts.

    Original Script ({original_script}):
    ```python
    {file_contents.get(original_script, "File content not found.")}
    ```

    Stack Trace:
    ```
    {stack_trace}
    ```

    Relevant File Contents:
    """
    for file_path, content in file_contents.items():
        if file_path != original_script:
            prompt += f"```python\n# {file_path}\n{content}\n```\n\n"

    prompt += """
    Analyze the error and provide a solution. Your response must be a JSON object with the following structure:

    {{
    "reasoning": "Step-by-step reasoning of the error and the proposed fix.",
    "suggested_fix": "A brief description of the changes needed.",
    "full_corrected_script": "The complete, corrected Python script that fixes the error. It should keep same logic and structure of original script."
    }}
    """

    contents = [
        types.Content(
            role="user",
            parts=[
                {"text": prompt}
            ]
        )
    ]

    response_schema = {
        "type": "OBJECT",
        "properties": {
            "reasoning": {
                "type": "STRING"
            },
            "suggested_fix": {
                "type": "STRING"
            },
            "full_corrected_script": {
                "type": "STRING"
            }
        },
        "required": [
            "reasoning",
            "suggested_fix",
            "full_corrected_script"
        ]
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
        return None

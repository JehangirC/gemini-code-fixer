# Gemini-Code-Fixer

An automated Python script fixer powered by Google's Gemini AI model. This tool automatically detects, analyzes, and fixes errors in Python scripts using AI-powered suggestions.

## Features

- Automatic error detection and stack trace analysis
- AI-powered error fixing suggestions
- Handles multiple file dependencies
- Iterative fixing attempts with maximum retry limit
- Detailed execution logging
- Support for common Python libraries (pandas, matplotlib, numpy)

## Prerequisites

- Python 3.7+
- Google Cloud Project & gcloud sdk installed
- Required Python packages (see pyproject.toml)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jehangirc/gemini-code-fixer.git
cd gemini-code-fixer
```

2. Install required packages:
```bash
uiv pip install .
```

3. Export your Google Cloud Project ID:
```Bash
export GOOGLE_CLOUD_PROJECT='your-project-id'  # Replace with your GCP project ID
```

## Usage

1. Place your Python script to be fixed in the same directory as `main.py` and name it `script.py`

2. Run the fixer:
```bash
python main.py
```

The tool will:
1. Execute your script
2. If errors occur, analyze the stack trace
3. Generate and apply fixes
4. Repeat until the script runs successfully or reaches maximum iterations (10)
5. Log all actions in `full_execution_log.json`

## Project Structure

- `main.py` - Main execution script
- `script_executor.py` - Handles Python script execution
- `traceback_parser.py` - Parses error stack traces using Gemini AI
- `file_handler.py` - Manages file operations
- `fix_suggester.py` - Generates fix suggestions using Gemini AI
- `pyproject.toml` - Required Python packages
- `script.py` - Broken code to test with

## How It Works

1. **Script Execution**: Runs the target Python script and captures any errors
2. **Error Analysis**: Uses Gemini AI to parse stack traces and identify relevant files
3. **Context Collection**: Gathers contents of all related Python files
4. **Fix Generation**: Sends error context to Gemini AI for fix suggestions
5. **Fix Application**: Applies suggested fixes to the original script
6. **Verification**: Re-runs the script to verify the fix
7. **Logging**: Records all actions and responses in a JSON log file

## Configuration

- Maximum fix attempts: 10 (configurable in `main.py`)
- Default Gemini model: "gemini-2.0-flash-001" (configurable)
- Log file: `full_execution_log.json`

## Limitations

- Relies on Gemini knowledge. Google search grounding to be implemented.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and feature requests, please use the GitHub Issues section of the repository.

## Source

This code is fork of [Gemini-code-fixer](https://github.com/cnemri/gemini-code-fixer), it has been improved by using environment variables, using uv as a package manager and dependancy resolver, fixing bugs with parts.from_text() and adding a pyproject.toml file with requirements.

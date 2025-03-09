import subprocess

def execute_script(script_path):
    """ Runs python script and returns output and error if any
    Args:
        script_path (str): Path to python script
    Returns:
        bool: True if script ran successfully, False otherwise
        str: Output of the script
        str: Error message if any
    """
    try:
        process = subprocess.run(['python', script_path], capture_output= True,text = True ,check=True)
        return True, process.stdout, None
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

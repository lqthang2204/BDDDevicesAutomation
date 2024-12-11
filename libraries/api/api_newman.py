import subprocess
import shutil
import platform
from project_runner import logger
import os

def check_newman():
    """
    Check if Newman is installed and available in the PATH.
    """
    newman_path = shutil.which("newman")
    if not newman_path:
        logger.error("Newman is not installed or not found in the system PATH.\nYou can install Newman by running: npm install -g newman\nEnsure Node.js and npm are installed on your system before proceeding.")
    return True

def run_command(file, data_file = 0):
    if check_newman() :
        # Construct the command
        command = ["newman", "run", file]
        if data_file:
            command.extend(["-d", data_file])

        try:
            # Use subprocess to run the command
            if platform.system() == "Windows":
                p = subprocess.Popen(" ".join(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            output, error = p.communicate()
            logger.debug(output.decode('utf-8').strip())
            # Handle the process return code
            if p.returncode != 0:
                error_msg = error.decode('utf-8').strip() if error else 'Unknown error'
                response = f"Error while running the command: {error_msg}"
                assert False, response
            else:
                response = f"Command succeeded:\n{output.decode('utf-8').strip()}"
            # logging.(response)
            logger.info(response)

        except Exception as e:
            error_msg = f"An exception occurred: {str(e)}"
            response = f"Error while running the command: {error_msg}"
            assert False, response

# Example usage
# file = "E:/Work-Space-Research\Selenium-with-python-behave/resources/postman-test/collection/apichallenges_2.postman_collection.json"
# data_file = "E:/Work-Space-Research/Selenium-with-python-behave/resources/postman-test/data-file/apichallenges.data.json"
# file_1 = "E:/Work-Space-Research\Selenium-with-python-behave/resources/postman-test/collection/apichallenges.postman_collection.json"
# # data_file = ""
# response = run_command(file_1)
# response_2 = run_command(file, data_file)
# print(response)

# run_command_without_file_data("E:/Work-Space-Research\Selenium-with-python-behave/resources/postman-test/collection/apichallenges.postman_collection.json")
# run_command_with_file_data("E:/Work-Space-Research\Selenium-with-python-behave/resources/postman-test/collection/apichallenges_2.postman_collection.json", "E:/Work-Space-Research/Selenium-with-python-behave/resources/postman-test/data-file/apichallenges.data.json")


import gzip
import subprocess
import shutil
import platform
from project_runner import logger
import json
from libraries.data_generators import check_match_pattern, get_test_data_for
from Utilities.process_value_input import procees_value

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
            # Handle the process return code
            if p.returncode != 0:
                logger.debug(output.decode('utf-8').strip())
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
def read_file_data(file_path):
    """
    Reads a JSON file and prints its content.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        list | dict: Parsed JSON data if successful, None otherwise.
    """
    """
       Reads a JSON file and prints its content.

       Args:
           file_path (str): The path to the JSON file.

       Returns:
           dict or list: Parsed JSON data if successful, None otherwise.
       """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # Parse JSON file into Python object
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return data


def update_data(data, table, dict_save_value):
    data = read_file_data(data)
    if not data:
        raise ValueError("Data read from the file is empty or invalid.")

    for row in table:
        # Extract the key and column from the table row
        key, column = row[0], row[1]

        # Ensure the first item in data is a dictionary
        if key in data[0]:
            # Try fetching a value using both methods
            value = get_test_data_for(column, dict_save_value)
            value = procees_value().get_value(column, dict_save_value)

            # Update the value in the data dictionary
            if value is not None:
                data[0][key] = value
    return data


def write_file_data(data, file_path):
    """
    Writes the given data to a file in JSON format.

    Parameters:
        data (dict or list): The data to be written to the file.
        file_path (str): The path to the file where the data should be saved.

    Returns:
        bool: True if the data was successfully written, False otherwise.
    """
    try:
        # Write the JSON data to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Data written to '{file_path}' successfully.")
        return True
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to encode data to JSON. {e}")
    except PermissionError:
        print(f"Error: Permission denied when writing to '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False
def delete_file_data(file_path):
    import os
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"File '{file_path}' deleted successfully.")
            logger.info(f"File '{file_path}' deleted successfully.")
        except Exception as e:
            print(f"An error occurred while deleting the file: {e}")
            assert False, f"An error occurred while deleting the file: {e}"
    else:
        print(f"File '{file_path}' not found.")
        assert False, f"File '{file_path}' not found."
def check_file_exist(file_path):
    import os
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        return True
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        logger.error(f"Error: The file '{file_path}' was not found.")
        raise FileNotFoundError
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logger.error(f"An unexpected error occurred: {e}")
        return False

#     logger.info(row)





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


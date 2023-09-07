import os
import csv
import paramiko
import argparse
from datetime import datetime

# Define a global debug flag
debug = False

def debug_print(message) -> None:
    if debug:
        print(message)

def combine_files(ssh, source_dir, input_file, output_file) -> None:
    """Combines text log files for IMEI numbers into a single output file.

        Parameters:
        ssh (SSHClient): SSH connection to remote server
        source_dir (str): Directory on server containing log files 
        input_file (str): Local CSV file with list of IMEI numbers
        output_file (str): Local path to write combined log file

        This function:
        - Opens the input CSV file containing IMEI numbers
        - Constructs the log file path on the server for each IMEI
        - Uses SSH to get the contents of each remote log file
        - Appends the log text to the combined output
        - Adds a separator string between each log file
        - Writes the final combined text to the local output file
    """
    combined_text = []

    # Separator between log files
    separator = "==================================================================="

    # Read the CSV file to obtain the list of IMEI serial numbers
    with open(input_file, 'r') as csvfile:
        imei_serials = csv.reader(csvfile)
        for imei in imei_serials:
            imei = imei[0].strip()  # Assuming the serial number is in the first column
            directory_path = os.path.join(source_dir, imei)
            print(f"\r Reading imei: {imei} , Found!", end='\r', flush=True)
            debug_print(f"Reading imei: {imei}, Found!")

            log_file_name = f"{imei}_log_file.txt"
            log_file_path = os.path.join(directory_path, log_file_name)
            debug_print(f"log_file_path: {log_file_path}")

            try:
                command = f"cat {log_file_path}"
                debug_print(f"command: {command}")
                stdin, stdout, stderr = ssh.exec_command(command)
                outlines = stdout.readlines()
                resp = ''.join(outlines)
                debug_print(resp)
                combined_text.append(resp)
                combined_text.append(separator)
            except FileNotFoundError:
                print(f"file {log_file_path} not exist")
                continue  # Log file doesn't exist, move to the next IMEI

    # Combine the text from all log files and save it locally
    combined_text = '\n'.join(combined_text)
    print(f"Writing to output file: {output_file}")
    with open(output_file, 'w') as local_output_file:
        local_output_file.write(combined_text)

def main() -> None:
    """Main function to handle command line arguments and orchestrate the log combining process.

        This parses the command line arguments to get:
        - Input CSV file path containing IMEI numbers 
        - Model name to determine source log directory on server
        - SSH server address and username

        It then:
        - Constructs full paths for source directory, output file
        - Sets up SSH connection to remote server
        - Calls combine_files() to concatenate the logs
        - Closes the SSH connection when done

        Any errors are printed, and a success message is printed when the process completes.
        """
    parser = argparse.ArgumentParser(description="Combine IMEI log files")
    parser.add_argument("-c", "--csv", type=str, help="Input CSV file containing IMEI serial numbers, or path for file if it not in same directoy")
    parser.add_argument("-m", "--model", type=str, help="Model name (e.g., em9191) to specify source directory")
    parser.add_argument("-s", "--address", type=str, help="SSH server IP address, the default is 10.148.38.142")
    parser.add_argument("-u", "--username", type=str, help="remote user name to connect with SSH")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")



    args = parser.parse_args()

    global debug
    input_file = args.csv or 'imei_serials.csv'
    model = args.model or 'em9191'
    username = args.username or 'jade'
    server_address = args.address or '10.148.38.142'
    debug = args.debug
    


    source_directory = f'/var/www/html/wiki/data/media/iot/{model}'
    date_file = datetime.utcnow().strftime("%Y-%m-%d")
    output_file = f'/home/jade/em91/logs/combined_log_{date_file}.txt'

    # SSH connection to the remote WIKI server
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    debug_print(f"conneting to ssh {username}@{server_address}")

    try:
        ssh.connect(server_address , username=username)
        combine_files(ssh, source_directory, input_file , output_file)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        print("Process completed successfully")
        ssh.close()

if __name__ == "__main__":
    main()
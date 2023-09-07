import os
import csv
from datetime import datetime
import paramiko

def combine_files(ssh, source_dir, output_file) -> None:
    combined_text = []
    input_file = input("Enter input filename:  ") or 'imei_serials.csv'

    # Separator between log files
    separator = "==================================================================="

    # Read the CSV file to obtain the list of IMEI serial numbers
    with open(input_file, 'r') as csvfile:
        imei_serials = csv.reader(csvfile)
        for imei in imei_serials:
            imei = imei[0].strip()  # Assuming the serial number is in the first column
            directory_path = os.path.join(source_dir, imei)
            print(f"\r Reading imei: {imei} , Found!", end='\r', flush=True)

            log_file_name = f"{imei}_log_file.txt"
            log_file_path = os.path.join(directory_path, log_file_name)
            # print(f"logfile path {log_file_path}",end='\r', flush=True)

            try:
                command = f"cat {log_file_path}"
                stdin, stdout, stderr = ssh.exec_command(command)
                outlines=stdout.readlines()
                resp=''.join(outlines)
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

if __name__ == "__main__":
    date_file = datetime.utcnow().strftime("%Y-%m-%d")
    source_directory = '/var/www/html/wiki/data/media/iot/em9191'
    output_file = f'/home/jade/em91/logs/combined_log_{date_file}.txt'  # Update to your local output file path
    

    print("Start reading the log files")
    # SSH connection to the remote WIKI server
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect('10.148.38.142', username='jade')
        # Call the combine_files function with the SSH connection
        combine_files(ssh, source_directory, output_file)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        print("Process completed sucessfuly") 
        ssh.close()

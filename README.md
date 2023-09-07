# combine_txt_files
 cli tool to combine text files to one file


## Log File Combiner

This tool combines text log files for different IMEI numbers into a single output file.

## Usage
`python combine_imei_logs.py [-h] [-c CSV] [-m MODEL] [-s ADDRESS] [-u USERNAME] [-d]
`
#### Required arguments:

`-c, --csv CSV` - Path to input CSV file containing list of IMEI numbers
### Optional arguments:

`-h, --help` - Show help message and exit.

`-m, --model MODEL` - Model name (e.g. em9191) to determine log file location on server. Default is 'em9191'.

`-s, --address ADDRESS` - IP address of SSH server. Default is '10.148.38.142'.

`-u, --username USERNAME` - SSH username. Default is 'jade'.

`-d, --debug` - Enable debug logging.

## How it works
- The script connects via SSH to a remote server containing log files for different IMEI numbers.
- It takes a CSV file as input with the list of IMEI numbers to combine.
- For each IMEI, it constructs the file path on the remote server and uses SSH to concatenate the contents.
- A separator string is added between each log file in the output.
- Finally, the combined log text is written to a local output file.

Debug logging can be enabled to see details on the files being processed.
from pathlib import Path
import argparse
import sys
import csv
import random

header = ["Model", "Wynik", "Czas"]

def read_args(): 
        parser = argparse.ArgumentParser(
                description="Script to generate or read catalog structure based on months, days, and time of day."
        )
        
        parser.add_argument(
                "-m", "--months",
                nargs="+",  
                required=True,
                help="List of months to include, e.g., styczeń luty marzec"
        )
        
        parser.add_argument(
                "-d", "--days",
                nargs="+",
                required=True,
                help="List of days corresponding to each month, e.g., pn-wt(ranges are allowed) pt"
        )
        
        parser.add_argument(
        "-t", "--time",
        nargs="*",  
        default=[],  
        help="Time of day for each day (r=morning, w=evening). Default is morning."
        )
        
        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument(
                "-c", "--create",
                dest="mode",
                action="store_const",
                const="create",
                help="Create files"
        )
        group.add_argument(
                "-r", "--read",
                dest="mode",
                action="store_const",
                const="read",
                help="Read files"
        )

        parser.set_defaults(mode="read")  
        return parser
        
# function used by : read_csv_time, write_to_csv
# @param1 path to file or directory
# if the path isn't directory or file -> program terminates
# if path is directory -> add Dane.csv as file 
# if path is file -> do nothing
def get_path(path : Path):
        if not path.is_file():
                if (path.is_dir()):
                        return path / "Dane.csv"
                else :
                        exit("Invalid path specified, Internal program error")
        return path

def verify_header(fieldnames):
        # remove extra spaces and empty strings
        cleaned = [f.strip() for f in fieldnames if f.strip()]

        if cleaned != header:
                sys.exit(f"Invalid CSV header. Expected {header}, got {cleaned}")

# Returns time from csv file
# Returns 0 for invalid path
# Exits if 
# - invalid path (file, or directory doesn't exist)
# - invalid file format
def read_csv_time(path : Path):
        
        path = get_path(path)
        
        with open(path, newline='') as csv_file:
                reader = csv.DictReader(csv_file, delimiter=';')
                
                verify_header(reader.fieldnames)
                
                 # read rows and clean keys/values
                rows = []
                for row in reader:
                        cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k and k.strip()}
                        rows.append(cleaned_row)
                
                #only one row allowed + headers 
                if (len(rows) != 1):
                        sys.exit("Invalid file format")
                
                if rows[0]["Model"] != "A":
                        return 0
                
                time_str = rows[0]["Czas"]
                time_value = int(time_str.strip('s'))

                return time_value

def generate_random():
        return {
                header[0] : random.choice(["A", "B", "C"]),
                header[1] : random.randint(0, 1000),
                header[2] : f"{random.randint(0,1000)}s"
        }
                             

# Writes to csv file         
# Exits if invalid path (file, or directory doesn't exist)             
def write_to_csv(path: Path): 
        path = get_path(path)
        
        with open(path, "w", newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=header, delimiter=';')
                writer.writeheader()
                writer.writerow(generate_random())


if __name__ == "__main__":
        parser = read_args()
        args = parser.parse_args()
        
        if len(args.months) != len(set(args.months)):
                sys.exit("Months must be distinct")

        if len(args.months) != len(args.days):
                sys.exit("Number of days must be equal to number of months")
        
        # Verified program arguments
        days = args.days
        months = args.months
        times = args.time
        
        if args.mode == "create":
                print("Hi")
        elif args.mode == "read":
                print("Hello")
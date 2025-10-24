from pathlib import Path
import sys
import csv
import random

header = ["Model", "Wynik", "Czas"]

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
# Exits if invalid path (file, or directory doesn't exist)
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
        #p = Path(".")
        #write_to_csv(p)
        #print(read_csv_time(p))
    
from pathlib import Path
import sys
import csv

def verify_header(fieldnames):
        # remove extra spaces and empty strings
        cleaned = [f.strip() for f in fieldnames if f.strip()]

        expected = ["Model", "Wynik", "Czas"]
        if cleaned != expected:
                sys.exit(f"Invalid CSV header. Expected {expected}, got {cleaned}")

# Returns time from csv file
# Returns 0 for invalid path
# Exits if invalid file format
def read_csv_time(path : Path):
        
        if not path.is_file():
                return 0

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
                
                time_str = rows[0]["Czas"]
                time_value = int(time_str.strip('s'))

                return time_value
                           


if __name__ == "__main__":
        print("Hello World")
    
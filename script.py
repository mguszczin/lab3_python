import argparse
import csv
import random
import sys
from pathlib import Path

HEADER = ["Model", "Wynik", "Czas"]

DAYS_NAMES = {
    "pn": "poniedzialek",
    "wt": "wtorek",
    "sr": "sroda",
    "cz": "czwartek",
    "pt": "piatek",
    "so": "sobota",
    "nd": "niedziela"
}

VALID_MONTHS = [
    "styczen", "luty", "marzec", "kwiecien", "maj", "czerwiec",
    "lipiec", "sierpien", "wrzesien", "pazdziernik", "listopad", "grudzien"
]

VALID_DAYS = ["pn", "wt", "sr", "cz", "pt", "so", "nd"]


# Returns an ArgumentParser configured to read:
# - months
# - days
# - time
# - mode: operation mode, either "create" to generate files or "read" to read existing files (default is "read")
# Examples are in main
def read_args():
    parser = argparse.ArgumentParser(
        description="Script to generate or read catalog structure based on months, days, and time of day.")

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
def get_path(path: Path):
    if not path.is_file():
        if path.is_dir():
            return path / "Dane.csv"
        else:
            sys.exit("Invalid path specified, Internal program error")
    return path


def verify_header(fieldnames):
    # remove extra spaces and empty strings
    cleaned = [f.strip() for f in fieldnames if f.strip()]

    if cleaned != HEADER:
        sys.exit(f"Invalid CSV header. Expected {HEADER}, got {cleaned}")


# Returns time from csv file
# Returns 0 for invalid path
# Exits if
# - invalid path (file, or directory doesn't exist)
# - invalid file format
def read_csv_time(path: Path):

    path = get_path(path)
    if not path.exists():
        sys.exit(f"Invalid path specified: {path}")

    with open(path, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')

        verify_header(reader.fieldnames)

        # read rows and clean keys/values
        rows = []
        for row in reader:
            cleaned_row = {k.strip(): v.strip()
                           for k, v in row.items() if k and k.strip()}
            rows.append(cleaned_row)

        # only one row allowed + headers
        if (len(rows) != 1):
            sys.exit("Invalid file format")

        if rows[0]["Model"] != "A":
            return 0

        time_str = rows[0]["Czas"]
        time_value = int(time_str.strip('s'))

        return time_value


def generate_random_csv_entry():
    return {
        HEADER[0]: random.choice(["A", "B", "C"]),
        HEADER[1]: random.randint(0, 1000),
        HEADER[2]: f"{random.randint(0, 1000)}s"
    }


# Writes to csv file
# Exits if invalid path (file, or directory doesn't exist)
def write_to_csv(path: Path):
    path = get_path(path)

    with open(path, "w", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=HEADER, delimiter=';')
        writer.writeheader()
        writer.writerow(generate_random_csv_entry())


# Generates the paths for months, days and times of day
def generate_paths(months, days, times) -> list[Path]:

    paths = []
    times = ["wieczorem" if time == "w" else "rano" for time in times]
    times_index = 0  # we want to iterate over times separately from the rest
    
    for month, day_entry in zip(months, days):
    
        if '-' in day_entry:
        
            start, end = day_entry.split('-', 1)
            days_from_range = []
            is_in_range = False
            
            for key, value in DAYS_NAMES.items():
                if key == start:
                    is_in_range = True
                if is_in_range:
                    days_from_range.append(value)
                if key == end:
                    is_in_range = False
                
            if is_in_range:  # this means that we exited the loop without reaching the end key
                sys.exit(f"Invalid day range: {day_entry}")
                
        else:
            days_from_range = [DAYS_NAMES[day_entry]]
            
        for day in days_from_range:
        
            if times_index < len(times):
                time = times[times_index]
                paths.append(Path(f"{month}/{day}/{time}"))
                times_index += 1
            else:
                paths.append(Path(f"{month}/{day}/rano"))
                
    return paths


# Creates all the necessary directiories for paths 'paths' to exist
def make_dirs(paths: list[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


# Check if months and days are in VALID_DAYS and months are in
# VALID_MONTHS + check len
def verify_args(args):
    if len(args.months) != len(set(args.months)):
        sys.exit("Months must be distinct")

    if len(args.months) != len(args.days):
        sys.exit("Number of days must be equal to number of months")

    for m in args.months:
        if m not in VALID_MONTHS:
            sys.exit("Invalid month")

    for day_entry in args.days:
        if '-' in day_entry:
            start, end = day_entry.split('-', 1)
            if start not in VALID_DAYS or end not in VALID_DAYS:
                sys.exit(f"Invalid day range: {day_entry}")
        else:
            if day_entry not in VALID_DAYS:
                sys.exit(f"Invalid day: {day_entry}")


# Already implemented:
# - generate_paths & make_dirs: makes the required dirs and generates paths for reading/writing
# - write_to_csv(path): writes data to a CSV file at the given path
# - read_csv_time(path): reads time data from a CSV file at the given path
# - reading & verification of arguments: parses command-line arguments and validates months/days/time
if __name__ == "__main__":
    parser = read_args()
    args = parser.parse_args()

    verify_args(args)

    # Verified program arguments
    months = args.months
    days = args.days
    times = args.time
    
    paths = generate_paths(months, days, times)
    make_dirs(paths)
    
    if args.mode == "create":
        print("Writing to files")
        for path in paths:
            write_to_csv(path)
            print(f"Wrote to {get_path(path)}")
    elif args.mode == "read":
        print("Reading from files")
        total_time = 0
        for path in paths:
            total_time += read_csv_time(path)
        print(f"Total time: {total_time}s")

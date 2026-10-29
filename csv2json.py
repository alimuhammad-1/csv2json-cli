import argparse
import csv
import json
import os
import sys

def convert_csv_to_json(csv_path, json_path=None, indent=2):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Error: Source CSV file '{csv_path}' does not exist.")
    
    if os.path.getsize(csv_path) == 0:
        raise ValueError(f"Error: Source CSV file '{csv_path}' is completely empty.")

    records = []
    # Using utf-8-sig to automatically strip BOM headers if present from Excel exports
    with open(csv_path, mode='r', encoding='utf-8-sig', newline='') as f:
        # Detect delimiter dynamically or fall back to standard comma
        sample = f.read(2048)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample)
        except csv.Error:
            dialect = csv.excel

        reader = csv.DictReader(f, dialect=dialect)
        
        if not reader.fieldnames or all(h is None or h.strip() == '' for h in reader.fieldnames):
            raise ValueError("Error: CSV file lacks valid column headers.")

        for row in reader:
            # Clean dictionary keys and values
            cleaned_row = {
                (k.strip() if k else f"col_{i}"): (v.strip() if v else None)
                for i, (k, v) in enumerate(row.items())
            }
            records.append(cleaned_row)

    json_data = json.dumps(records, indent=indent, ensure_ascii=False)

    if json_path:
        with open(json_path, mode='w', encoding='utf-8') as f:
            f.write(json_data)
        return f"Successfully converted '{csv_path}' -> '{json_path}' ({len(records)} records)."
    
    return json_data

def build_parser():
    parser = argparse.ArgumentParser(
        prog="csv2json",
        description="A robust CLI tool to convert CSV files into formatted JSON output.",
        epilog="Example usage: csv2json input.csv -o output.json --indent 4"
    )
    parser.add_argument("csv_file", help="Path to the input CSV file.")
    parser.add_argument("-o", "--output", help="Path to save the generated JSON output file (prints to stdout if omitted).")
    parser.add_argument("--indent", type=int, default=2, help="Number of spaces for JSON indentation (default: 2).")
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = convert_csv_to_json(args.csv_file, args.output, args.indent)
        print(result)
    except Exception as e:
        sys.stderr.write(f"{str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()

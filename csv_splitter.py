import csv
import os
from pathlib import Path

CSV_FILE_PATH = "VFXSHOT-SLATE-2.csv"
MAX_ROWS_PER_FILE = 100
# folder you want to save files in
OUTPUT_BASE_PATH = '/Users/604567947/Downloads/SplitCSVFiles/'

def split_csv_file():
    input_path = Path(CSV_FILE_PATH)
    
    if not input_path.exists():
        print(f"ERROR: File not found: {CSV_FILE_PATH}")
        return
    
    output_folder = Path(OUTPUT_BASE_PATH) / input_path.stem
    output_folder.mkdir(parents=True, exist_ok=True)
    
    base_name = input_path.stem
    extension = input_path.suffix
    created_files = []
    
    # using replace for now because of encoding issues
    with open(CSV_FILE_PATH, 'r', newline='', encoding='utf-8', errors='replace') as infile:
        reader = csv.reader(infile)
        header = next(reader, None)
        if not header:
            print("ERROR: Empty CSV file")
            return
        
        file_count = 1
        row_count = 0
        current_file = None
        current_writer = None
        
        for row in reader:
            if row_count == 0:
                if current_file:
                    current_file.close()
                output_filename = f"{base_name}_part{file_count:03d}{extension}"
                output_filepath = output_folder / output_filename
                
                current_file = open(output_filepath, 'w', newline='', encoding='utf-8')
                current_writer = csv.writer(current_file)
                current_writer.writerow(header)
                
                created_files.append(output_filepath)
                print(f"Created: {output_filename}")
                file_count += 1
            
            current_writer.writerow(row)
            row_count += 1
            
            if row_count >= MAX_ROWS_PER_FILE:
                row_count = 0
                
        if current_file:
            current_file.close()
    
    print(f"\nsplit into {len(created_files)} files")

if __name__ == "__main__":
    split_csv_file()
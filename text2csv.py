import os
import pandas as pd
import numpy as np

def txt_to_csv(path):
    """Converts trivia questions from text files to a structured CSV format, excluding true/false questions."""
    questions, key, dist1, dist2, dist3, dist4 = [], [], [], [], [], []
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("#Q"):
                question_text = line[3:]
                answer_key_line = lines[i + 1].strip()
                answer_key = answer_key_line[1:] if answer_key_line.startswith("^") else np.nan

                # Collect options
                options = lines[i + 2:i + 6]
                options_text = [opt.strip()[2:].strip() for opt in options if opt.strip() and opt.strip()[0] in ['A', 'B', 'C', 'D']]
                
                # Only add to the list if all four options are present and valid
                if len(options_text) == 4 and all(opt not in ["True", "False"] for opt in options_text):
                    questions.append(question_text)
                    key.append(answer_key)
                    dist1.append(options_text[0])
                    dist2.append(options_text[1])
                    dist3.append(options_text[2])
                    dist4.append(options_text[3])

                # Move index to the line after the last option
                i += 6
            else:
                # Move to the next line if not a question block
                i += 1

    return pd.DataFrame({
        "Questions": questions,
        "Correct": key,
        "A": dist1,
        "B": dist2,
        "C": dist3,
        "D": dist4
    })

def parse_files(sourcePath, destination):
    """Parses all .txt files in the sourcePath and saves them as .csv files in the destination."""
    if not os.path.exists(destination):
        os.makedirs(destination, exist_ok=True)
    for file in os.listdir(sourcePath):
        if file.endswith('.txt'):
            print(f"Processing {file}...")
            full_path = os.path.join(sourcePath, file)
            csv_data = txt_to_csv(full_path)
            csv_filename = os.path.splitext(file)[0] + '.csv'
            csv_data.to_csv(os.path.join(destination, csv_filename), index=False)
            print(f"Saved to {csv_filename}")

# Example paths (replace with your actual paths)
sourcePath = '/Users/matthieudebeaucorps/Desktop/Projects/trivia/categories'
destination = '/Users/matthieudebeaucorps/Desktop/Projects/trivia/categories_csv'

# Process the files
parse_files(sourcePath, destination)
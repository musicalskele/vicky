import subprocess
import concurrent.futures
from tqdm import tqdm

# Specify the file path here
filepath = 'mod_list.txt'

def process_line(line):
    line = line.strip()
    if "modrinth.com" in line:
        command = f"""packwiz modrinth add {line} -y"""
    elif "curseforge.com" in line:
        command = f"""packwiz curse add {line} -y"""
    else:
        print(f"Error: Unknown URL format in line: {line}, searching on modrinth")
        command = f"""packwiz modrinth add "{line}" -y"""
    
    print(f"Executing: {command}\n")
    subprocess.run(command, shell=True)

def process_line_with_progress(line, pbar):
    process_line(line)
    pbar.update(1)

# Read all lines from the file
with open(filepath) as fp:
    lines = fp.readlines()

# Run the commands in parallel with a progress bar
with tqdm(total=len(lines)) as pbar:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_line_with_progress, line, pbar) for line in lines]
        concurrent.futures.wait(futures)

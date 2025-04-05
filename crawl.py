import pyperclip
import time
import csv
import os
from datetime import datetime

def lets_copy(output_file):
    previous_clipboard = ""
    current_topic = None
    dataset = [] 
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    file_exists = os.path.isfile(output_file)
    
    try:
        with open(output_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Topic', 'URL', 'Timestamp'])
    except PermissionError:
        print(f"Error: Cannot write to {output_file}. Check file permissions.")
        return
    except Exception as e:
        print(f"Error creating file: {e}")
        return
    
    print("\nClipboard monitor started. Copy your topics and URLs one by one...")
    print("First copy the topic name, then its URL.")
    print("Press Ctrl+C to stop and save the dataset.\n")
    
    try:
        while True:
            current_clipboard = pyperclip.paste().strip()
            if current_clipboard != previous_clipboard and current_clipboard:
                if current_topic is None:
                    current_topic = current_clipboard
                    print(f"Topic saved: {current_topic}")
                else:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    dataset.append([current_topic, current_clipboard, timestamp])
                    print(f"Pair saved: {current_topic} | {current_clipboard}")
                    try:
                        with open(output_file, 'a', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow([current_topic, current_clipboard, timestamp])
                    except Exception as e:
                        print(f"Error saving to file: {e}")
                    
                    current_topic = None  
                
                previous_clipboard = current_clipboard
            
            time.sleep(0.3) 
    
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
        print(f"Dataset saved to: {os.path.abspath(output_file)}")
        print(f"Total pairs collected: {len(dataset)}")

if __name__ == "__main__":
   
    try:
        import pyperclip
    except ImportError:
        import subprocess
        import sys
        print("Installing pyperclip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
        import pyperclip
    
    print("Clipboard to CSV Dataset Creator")
    print("-------------------------------")
    
    while True:
        file_name = input("Enter file name (without extension): ").strip()
        if not file_name:
            print("File name cannot be empty. Please try again.")
            continue
        
        output_file = f"dataset/{file_name}.csv"
        if os.path.isfile(output_file):
            overwrite = input(f"File '{output_file}' exists. Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                continue
        
        break
    
    lets_copy(output_file)
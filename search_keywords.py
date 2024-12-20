import os

def search_keyword_in_files(keyword, directory):
    """
    Search for a specific keyword in Python files within a directory.

    Args:
        keyword (str): The keyword to search for.
        directory (str): The directory to search in.

    Prints:
        File paths containing the keyword.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        if keyword in f.read():
                            print(f"Found '{keyword}' in {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

# Set the keywords to search for
keywords = ["data_client", "export_utils", "report_utils"]

# Define the target directory for the search
directory = "app"

# Search for each keyword in the specified directory
for keyword in keywords:
    search_keyword_in_files(keyword, directory)

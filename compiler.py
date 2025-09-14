import os

def generate_file_structure(directory, exclude_dirs, extensions, prefix=""):
    """
    Recursively generates a string representation of the directory structure,
    excluding specified directories and only including files with specified extensions.
    """
    structure = ""
    # Filter out excluded directories and get a list of items to display
    all_contents = sorted(os.listdir(directory))
    filtered_contents = []
    for item in all_contents:
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            if item not in exclude_dirs:
                filtered_contents.append(item)
        else:
            if any(item.endswith(ext) for ext in extensions):
                filtered_contents.append(item)

    for i, item in enumerate(filtered_contents):
        path = os.path.join(directory, item)
        is_last = i == len(filtered_contents) - 1
        
        # Add a visual indicator for directory/file
        indicator = "├── " if not is_last else "└── "
        structure += f"{prefix}{indicator}{item}\n"
        
        # Recurse for subdirectories
        if os.path.isdir(path):
            new_prefix = prefix + ("│   " if not is_last else "    ")
            structure += generate_file_structure(path, exclude_dirs, extensions, new_prefix)
    return structure

def compile_codebase_for_prompting(root_dir, output_file, extensions):
    """
    Compiles a codebase into a single text file, optimized for AI prompting.
    The file includes a directory structure overview and the content of each
    file with its path.
    
    Args:
        root_dir (str): The root directory of the codebase.
        output_file (str): The path to the output text file.
        extensions (list): A list of file extensions to include.
    """
    # Check if the root directory exists
    if not os.path.isdir(root_dir):
        print(f"Error: The directory '{root_dir}' does not exist.")
        return

    print(f"Compiling codebase from '{root_dir}'...")
    
    # Define the list of directories to exclude
    directories_to_exclude = [
        '.git', '__pycache__', 'node_modules', 'dist', 'build', 'venv', '.idea',
        '__init__.pyc', 'compiled_codebase.txt' # Exclude the output file itself
    ]

    # Generate the file structure
    print("Generating file structure...")
    file_structure_overview = generate_file_structure(root_dir, directories_to_exclude, extensions)

    # Collect all file contents
    compiled_content = ""
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # This is the key part: modify dirnames in-place to prune the traversal
        dirnames[:] = [d for d in dirnames if d not in directories_to_exclude]
        
        for filename in filenames:
            # Check if the file has a desired extension
            if any(filename.endswith(ext) for ext in extensions):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read()
                        relative_path = os.path.relpath(file_path, root_dir)
                        # Add a clear separator for each file, optimized for AI parsing
                        compiled_content += f"\n\n### File: {relative_path}\n\n```\n{file_content}\n```\n"
                except Exception as e:
                    print(f"Could not read file {file_path}: {e}")
    
    # Write to the output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write the file structure overview first
            f.write("Codebase Structure Overview:\n\n")
            f.write(file_structure_overview)
            f.write("\n\n" + "="*50 + "\n\n")
            
            # Then write the compiled content of each file
            f.write("Compiled Code Contents:\n")
            f.write(compiled_content)

        print(f"Successfully compiled codebase to '{output_file}'.")
    except Exception as e:
        print(f"Error writing to file '{output_file}': {e}")


# --- Script Usage Example ---
if __name__ == "__main__":
    # Customize these variables
    root_directory = "frontend"  # The current directory
    output_filename = "codebase_frontend.txt"
    
    # List of common file extensions. You can modify this.
    # A complete list is also provided in a separate file.
    file_extensions = [
        '.py', '.js', '.html', '.css', '.vue'
    ]

    compile_codebase_for_prompting(root_directory, output_filename, file_extensions)

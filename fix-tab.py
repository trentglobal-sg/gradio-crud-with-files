# fix_indentation.py
import argparse
import sys
import re

def fix_indentation(file_path, tab_size=4):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    
    # Split content into lines
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Count leading tabs and spaces separately
        leading_tabs = len(re.findall(r'^\t+', line))
        leading_spaces = len(re.findall(r'^ +', line))
        
        # If there are tabs in the indentation, convert them to spaces
        if leading_tabs > 0:
            # Remove all leading whitespace
            stripped_line = line.lstrip()
            # Calculate the equivalent spaces for tabs
            equivalent_spaces = ' ' * (leading_tabs * tab_size + leading_spaces)
            # Rebuild the line with spaces
            fixed_line = equivalent_spaces + stripped_line
            fixed_lines.append(fixed_line)
        else:
            # No tabs, keep as is
            fixed_lines.append(line)
    
    # Write the fixed content back to the file
    with open(file_path, 'w') as file:
        file.write('\n'.join(fixed_lines))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fix inconsistent indentation in a Python file.')
    parser.add_argument('file', help='Path to the Python file to fix')
    parser.add_argument('--tabsize', type=int, default=4, help='Number of spaces per tab (default: 4)')
    args = parser.parse_args()
    
    # Create a backup first
    import shutil
    backup_path = args.file + '.bak'
    shutil.copy2(args.file, backup_path)
    print(f"Created backup at '{backup_path}'")
    
    fix_indentation(args.file, args.tabsize)
    print(f"Fixed indentation in '{args.file}'")
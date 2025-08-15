#!/usr/bin/env python3
"""
Convert favorite files from VS Code settings to text format.
Reads .vscode/settings.json and converts .ipynb files to .txt files.
"""

import json
import os
import sys
from pathlib import Path
import nbformat
from nbformat import v4

def convert_notebook_to_text(notebook_path, output_path):
    """Convert a Jupyter notebook to plain text format."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Converted from: {notebook_path}\n")
            f.write("=" * 60 + "\n\n")
            
            for i, cell in enumerate(nb.cells, 1):
                if cell.cell_type == 'markdown':
                    f.write(f"## Cell {i} (Markdown)\n")
                    f.write("-" * 30 + "\n")
                    f.write(cell.source)
                    f.write("\n\n")
                    
                elif cell.cell_type == 'code':
                    f.write(f"## Cell {i} (Code)\n")
                    f.write("-" * 30 + "\n")
                    f.write("```python\n")
                    f.write(cell.source)
                    f.write("\n```\n\n")
                    
                    # Include outputs if they exist
                    if hasattr(cell, 'outputs') and cell.outputs:
                        f.write("### Output:\n")
                        for output in cell.outputs:
                            if output.output_type == 'stream':
                                f.write(f"```\n{output.text}```\n")
                            elif output.output_type == 'execute_result':
                                if 'text/plain' in output.data:
                                    f.write(f"```\n{output.data['text/plain']}```\n")
                            elif output.output_type == 'error':
                                f.write(f"```\nError: {output.ename}: {output.evalue}\n```\n")
                        f.write("\n")
                        
        print(f"✓ Converted: {notebook_path} -> {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error converting {notebook_path}: {e}")
        return False

def copy_text_file(source_path, output_path):
    """Copy a text file to the output directory."""
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Copied from: {source_path}\n")
            f.write("=" * 60 + "\n\n")
            f.write(content)
            
        print(f"✓ Copied: {source_path} -> {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error copying {source_path}: {e}")
        return False

def main():
    # Get the script directory (where .vscode/settings.json should be)
    script_dir = Path(__file__).parent.parent.parent
    settings_file = script_dir / ".vscode" / "settings.json"
    
    if not settings_file.exists():
        print(f"Error: {settings_file} not found!")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path.home() / "Documents" / "favorites_txt"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    # Read settings.json
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except Exception as e:
        print(f"Error reading settings.json: {e}")
        sys.exit(1)
    
    # Get favorites
    favorites = settings.get("favorites.resources", [])
    if not favorites:
        print("No favorites found in settings.json")
        return
    
    print(f"Found {len(favorites)} favorite items")
    
    converted_count = 0
    skipped_count = 0
    
    for favorite in favorites:
        file_path = favorite.get("filePath", "")
        if not file_path:
            continue
            
        # Convert relative path to absolute
        full_path = script_dir / file_path
        
        # Handle directories - convert all files in the directory
        if full_path.is_dir():
            print(f"📁 Processing directory: {full_path}")
            # Create subdirectory in output
            dir_name = str(Path(file_path)).replace("/", "_").replace("\\", "_")
            sub_output_dir = output_dir / dir_name
            sub_output_dir.mkdir(exist_ok=True)
            
            # Find all supported files in the directory
            supported_extensions = ['.ipynb', '.py', '.txt', '.md', '.rst']
            for ext in supported_extensions:
                for file in full_path.rglob(f'*{ext}'):
                    if file.is_file():
                        relative_to_dir = file.relative_to(full_path)
                        output_name = str(relative_to_dir).replace("/", "_").replace("\\", "_")
                        
                        if file.suffix == '.ipynb':
                            output_name = output_name.replace('.ipynb', '.txt')
                            output_path = sub_output_dir / output_name
                            if convert_notebook_to_text(file, output_path):
                                converted_count += 1
                            else:
                                skipped_count += 1
                        else:
                            if not output_name.endswith('.txt'):
                                output_name += '.txt'
                            output_path = sub_output_dir / output_name
                            if copy_text_file(file, output_path):
                                converted_count += 1
                            else:
                                skipped_count += 1
            continue
        
        if not full_path.exists():
            # Try to find the file by searching for it
            print(f"⚠ File not found at expected location: {full_path}")
            # Try to find it in the repository
            possible_files = list(script_dir.rglob(Path(file_path).name))
            if possible_files:
                print(f"  Found possible matches:")
                for pf in possible_files[:3]:  # Show first 3 matches
                    print(f"    {pf}")
                # Use the first match
                full_path = possible_files[0]
                print(f"  Using: {full_path}")
            else:
                skipped_count += 1
                continue
            
        # Skip if still not found
        if not full_path.exists():
            print(f"⚠ File not found: {full_path}")
            skipped_count += 1
            continue
        
        # Generate output filename
        relative_path = Path(file_path)
        output_name = str(relative_path).replace("/", "_").replace("\\", "_")
        
        if full_path.suffix == '.ipynb':
            output_name = output_name.replace('.ipynb', '.txt')
            output_path = output_dir / output_name
            
            if convert_notebook_to_text(full_path, output_path):
                converted_count += 1
            else:
                skipped_count += 1
                
        elif full_path.suffix in ['.py', '.txt', '.md', '.rst']:
            if not output_name.endswith('.txt'):
                output_name += '.txt'
            output_path = output_dir / output_name
            
            if copy_text_file(full_path, output_path):
                converted_count += 1
            else:
                skipped_count += 1
                
        else:
            print(f"⚠ Skipping unsupported file type: {full_path}")
            skipped_count += 1
    
    print(f"\nSummary:")
    print(f"✓ Converted: {converted_count} files")
    print(f"⚠ Skipped: {skipped_count} files")
    print(f"📁 Output directory: {output_dir}")
    
    # Show what was created
    if output_dir.exists():
        print(f"\nGenerated files:")
        for txt_file in sorted(output_dir.rglob("*.txt")):
            rel_path = txt_file.relative_to(output_dir)
            file_size = txt_file.stat().st_size
            print(f"  {rel_path} ({file_size} bytes)")

if __name__ == "__main__":
    main()

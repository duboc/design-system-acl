import os
import shutil
from typing import Dict
import json
from pathlib import Path

def save_component_files(files: Dict[str, str], output_dir: str) -> None:
    """Save component files to the specified directory."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for file_name, content in files.items():
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w') as f:
            f.write(content)

    # Create package.json if it doesn't exist
    package_json = os.path.join(output_dir, "package.json")
    if not os.path.exists(package_json):
        create_package_json(output_dir)

def create_package_json(output_dir: str) -> None:
    """Create a package.json file for the component"""
    package_data = {
        "name": os.path.basename(output_dir),
        "version": "1.0.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "typescript": "^4.9.5",
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject"
        }
    }
    
    with open(os.path.join(output_dir, "package.json"), "w") as f:
        json.dump(package_data, f, indent=2)

def create_component_preview(files: Dict[str, str]) -> str:
    """Create a preview environment for the component"""
    # The preview is now generated in the component generator
    return ""

def cleanup_old_files(directory: str, max_age_days: int = 7) -> None:
    """Clean up old generated files"""
    # TODO: Implement cleanup logic for old generated components
    pass

def create_component_archive(output_dir: str) -> str:
    """Create a zip archive of the component"""
    archive_name = os.path.basename(output_dir)
    shutil.make_archive(archive_name, 'zip', output_dir)
    return f"{archive_name}.zip" 
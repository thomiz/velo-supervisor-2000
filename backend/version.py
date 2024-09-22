#!/usr/bin/env python3
"""Script to maintain version number"""

import subprocess

def get_git_version():
    try:
        # Get the latest tag
        tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode().strip()
        
        # Get the number of commits since the last tag
        commit_count = subprocess.check_output(['git', 'rev-list', f'{tag}..HEAD', '--count']).decode().strip()
        
        # Combine tag and commit count
        version = f"{tag}.{commit_count}"
    except subprocess.CalledProcessError:
        # If no tags are found, use a default version
        version = "0.0.0"
    
    return version

# Write version to a file
with open('current_version.txt', 'w') as f:
    f.write(get_git_version())

print(f"Current version: {get_git_version()}")
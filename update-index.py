#!/usr/bin/env python3
"""
Update the workflow-results index.html with current workflow directories.

This script scans the workflow-results directory for workflow run directories
and updates the JavaScript data in index.html to reflect the current state.

Usage:
    python update-index.py
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime


def calculate_duration(started_at, completed_at):
    """Calculate duration between two ISO timestamps."""
    if not started_at or not completed_at:
        return None
    
    try:
        from datetime import datetime
        start = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
        end = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
        duration = end - start
        
        # Format as HH:MM:SS
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    except Exception:
        return None


def load_workflow_metadata(dir_path):
    """Load workflow metadata from workflow-metadata.json if it exists."""
    metadata_file = dir_path / 'workflow-metadata.json'
    if metadata_file.exists():
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Extract the requested information
                actor = data.get('workflow', {}).get('actor', 'Unknown')
                release_version = data.get('inputs', {}).get('release-version', 'Unknown')
                
                execution = data.get('execution', {})
                started_at = execution.get('started_at', '').strip()
                duration_formatted = execution.get('duration_formatted', None)
                
                # If no duration but we have start and end times, calculate it
                if not duration_formatted:
                    completed_at = execution.get('completed_at', '').strip()
                    if started_at and completed_at:
                        duration_formatted = calculate_duration(started_at, completed_at)
                
                # Clean up empty strings
                if not started_at:
                    started_at = None
                if not duration_formatted:
                    duration_formatted = None
                
                return {
                    'actor': actor if actor != 'Unknown' else None,
                    'release_version': release_version if release_version != 'Unknown' else None,
                    'started_at': started_at,
                    'duration_formatted': duration_formatted
                }
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Could not parse metadata for {dir_path.name}: {e}")
    
    return {
        'actor': None,
        'release_version': None,
        'started_at': None,
        'duration_formatted': None
    }


def scan_workflow_directories():
    """Scan for workflow directories and collect metadata."""
    workflows = []
    current_dir = Path('.')
    
    for dir_path in sorted(current_dir.iterdir(), reverse=True):
        if dir_path.is_dir() and dir_path.name not in ['__pycache__', '.git']:
            # Check if it looks like a workflow directory (YYYY-MM-DD-RUNID format)
            match = re.match(r'(\d{4})-(\d{2})-(\d{2})-(\d+)', dir_path.name)
            if match:
                year, month, day, run_id = match.groups()
                
                # Check for index.html (summary available)
                has_index = (dir_path / 'index.html').exists()
                
                # Count job directories
                job_count = len([d for d in dir_path.iterdir() if d.is_dir()])
                
                # Load workflow metadata
                metadata = load_workflow_metadata(dir_path)
                
                workflows.append({
                    'name': dir_path.name,
                    'year': year,
                    'month': month,
                    'day': day,
                    'run_id': run_id,
                    'has_index': has_index,
                    'job_count': job_count,
                    'actor': metadata['actor'],
                    'release_version': metadata['release_version'],
                    'started_at': metadata['started_at'],
                    'duration_formatted': metadata['duration_formatted']
                })
    
    return workflows


def update_index_html(workflows):
    """Update the index.html file with current workflow data."""
    index_file = Path('index.html')
    
    if not index_file.exists():
        print("Error: index.html not found in current directory")
        return False
    
    # Read current index.html
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Generate JavaScript data for workflows with metadata
    js_workflows = []
    for workflow in workflows:
        # Create a JavaScript object with all the metadata
        metadata_js = "{"
        metadata_js += f"name: '{workflow['name']}'"
        metadata_js += f", hasIndex: {str(workflow['has_index']).lower()}"
        metadata_js += f", jobCount: {workflow['job_count']}"
        
        if workflow['actor']:
            metadata_js += f", actor: '{workflow['actor']}'"
        else:
            metadata_js += ", actor: null"
            
        if workflow['release_version']:
            metadata_js += f", releaseVersion: '{workflow['release_version']}'"
        else:
            metadata_js += ", releaseVersion: null"
            
        if workflow['started_at']:
            metadata_js += f", startedAt: '{workflow['started_at']}'"
        else:
            metadata_js += ", startedAt: null"
            
        if workflow['duration_formatted']:
            metadata_js += f", duration: '{workflow['duration_formatted']}'"
        else:
            metadata_js += ", duration: null"
            
        metadata_js += "}"
        js_workflows.append(metadata_js)
    
    workflows_js = ',\n                '.join(js_workflows)
    
    # Replace the workflow directories/data array with the new workflow metadata
    # Try both the old and new variable names
    pattern1 = r'(const workflowDirectories = \[)(.*?)(\];)'
    pattern2 = r'(const workflowData = \[)(.*?)(\];)'
    
    replacement = f'\\1\n                {workflows_js}\n            \\3'
    
    if re.search(pattern1, content, flags=re.DOTALL):
        updated_content = re.sub(pattern1, replacement, content, flags=re.DOTALL)
        # Update the variable name
        updated_content = updated_content.replace('const workflowDirectories = [', 'const workflowData = [')
    elif re.search(pattern2, content, flags=re.DOTALL):
        updated_content = re.sub(pattern2, replacement, content, flags=re.DOTALL)
    else:
        print("Warning: Could not find workflow data array to update")
        updated_content = content
    
    # Update the checkForIndex function with actual workflow data
    workflows_with_index = [w['name'] for w in workflows if w['has_index']]
    index_list_js = ', '.join([f"'{name}'" for name in workflows_with_index])
    
    # Replace the checkForIndex function
    check_for_index_pattern = r'(function checkForIndex\(workflowName\) \{.*?return )(.*?)(\;.*?\})'
    check_for_index_replacement = f'\\1[{index_list_js}].includes(workflowName)\\3'
    
    updated_content = re.sub(check_for_index_pattern, check_for_index_replacement, updated_content, flags=re.DOTALL)
    
    # Update the generation timestamp while preserving the dynamic date element
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pattern = r'(Last updated: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \| Auto-generated from directory scan)'
    if re.search(pattern, updated_content):
        # Update existing timestamp
        replacement = f'Last updated: {current_time} | Auto-generated from directory scan'
        updated_content = re.sub(pattern, replacement, updated_content)
    else:
        # First time update - replace the original footer
        pattern = r'(Generated on <span id="current-date"></span>)'
        replacement = f'Last updated: {current_time} | Auto-generated from directory scan'
        updated_content = updated_content.replace('Generated on <span id="current-date"></span>', replacement)
    
    # Write updated content
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    return True


def main():
    """Main function."""
    print("Scanning workflow directories...")
    workflows = scan_workflow_directories()
    
    if not workflows:
        print("No workflow directories found.")
        return
    
    print(f"Found {len(workflows)} workflow directories:")
    for workflow in workflows[:5]:  # Show first 5
        status = "✅ Summary" if workflow['has_index'] else "📁 Raw files"
        print(f"  {workflow['name']} ({workflow['job_count']} jobs) - {status}")
    
    if len(workflows) > 5:
        print(f"  ... and {len(workflows) - 5} more")
    
    print("\nUpdating index.html...")
    if update_index_html(workflows):
        print("✅ Successfully updated index.html")
        print("🌐 Open workflow-results/index.html in your browser to view the updated listing")
    else:
        print("❌ Failed to update index.html")


if __name__ == "__main__":
    # Change to workflow-results directory if not already there
    if not Path('generate-workflow-summary.py').exists():
        if Path('workflow-results/generate-workflow-summary.py').exists():
            os.chdir('workflow-results')
        else:
            print("Error: Please run this script from the project root or workflow-results directory")
            exit(1)
    
    main()
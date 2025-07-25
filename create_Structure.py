import os

folders = [
    'agents',
    'core', 
    'llm',
    'nodes/departments',
    'graph'
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    # Create empty __init__.py files
    with open(os.path.join(folder, '__init__.py'), 'w') as f:
        pass
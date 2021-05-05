import os
from os import path
from pathlib import Path
root_project_path = Path(__file__).parent.parent.parent
print(str(root_project_path))
path_to_data = Path.joinpath(root_project_path, '/data')
print(path_to_data)

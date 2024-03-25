import pathlib
import yaml

def read_yaml_file(file: pathlib.Path):
    with open(file, 'r') as f:
        content = f.read()
        yaml_content = yaml.safe_load(content)
        return yaml_content

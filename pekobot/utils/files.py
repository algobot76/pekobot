"""File utilities"""
from typing import AnyStr, Dict

import yaml


def load_yaml_file(file_path: AnyStr) -> Dict:
    """Loads the data from a YAML file.

    Args:
        file_path: A file path.

    Returns:
        File data as a dict.
    """
    with open(file_path, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data

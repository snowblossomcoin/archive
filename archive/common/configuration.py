import sys
import pathlib
import json


default_config = {
    "log_level": 10,
    "raw_path": "log_test/raw/",
    "html_path": "log_test/html/",
    "legacy": False,
    "communities": [
        {
            "name": "my_project",
            "platforms": [
                 {
                     "name": "slack",
                     "credentials": {
                         "token": "random"
                     }
                 }
            ]
        }
    ]
}


def get_file_config(path):
    path = pathlib.Path(path)
    if path.is_file():
        with open(path.resolve(), 'r') as f:
            return json.load(f)
    else:
        return None


def get_cli_config():
    config = {}

    position = 1
    arg_count = len(sys.argv)
    while position < arg_count:
        if "-" in sys.argv[position]:
            key = sys.argv[position].split('--')[-1]
            if position + 1 <= arg_count:
                value = sys.argv[position+1]
                if "true" in value.lower():
                    value = True
                elif "false" in value.lower():
                    value = False
                config[key] = value
                position += 1
        position += 1

    return config


def mix_configs(configs):
    config = {}
    for c in configs:
        if c:
            config.update(c)
    return config

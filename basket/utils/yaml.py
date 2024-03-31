import pathlib
import yaml


def read_yaml_file(file: pathlib.Path):
    with open(file, 'r') as f:
        content = f.read()
        yaml_content = yaml.safe_load(content)
        return yaml_content


def dump_exp_yaml(file: pathlib.Path, configs, tap_times=None):
    with open(file, 'w') as f:
        content = {}
        for key in configs.keys():
            if isinstance(configs[key], (str, pathlib.Path)):
                configs[key] = read_yaml_file(configs[key])
        for key_yaml, key_dict_list in ('environment', ['env']), \
                ('optimizer', ['opt']), ('loss', []):
            for key_dict in key_dict_list + [key_yaml]:
                if key_dict in configs.keys():
                    item = configs[key_dict]
                    if key_yaml in item: 
                        content[key_yaml] = item[key_yaml]
                    else:
                        content[key_yaml] = item
        if tap_times is not None:
            content['tap_times'] = tap_times
        f.write(yaml.dump(content))

import pathlib
import yaml


def read_yaml_file(file: pathlib.Path):
    with open(file, 'r') as f:
        content = f.read()
        yaml_content = yaml.safe_load(content)
        return yaml_content


def dump_exp_yaml(file: pathlib.Path, configs,
                  tap_times=None, init_tap_times=None):
    with open(file, 'w') as f:
        content = {}
        for key in configs.keys():
            if isinstance(configs[key], (str, pathlib.Path)):
                configs[key] = read_yaml_file(configs[key])
        for key_yaml, key_dict_list in ('environment', ['env']), \
                ('optimizer', ['opt']), ('loss', []), ('sim', []):
            for key_dict in key_dict_list + [key_yaml]:
                if key_dict in configs.keys():
                    item = configs[key_dict]
                    if key_yaml in item: 
                        content[key_yaml] = item[key_yaml]
                    else:
                        content[key_yaml] = item
        if tap_times is not None:
            content['tap_times'] = tap_times
        if init_tap_times is not None:
            content['init_tap_times'] = init_tap_times
        f.write(yaml.dump(content))

def setting_write_in(file: pathlib.Path, key, value):
    with open(file, 'r') as env:
        data = yaml.safe_load(env)
    if isinstance(value, list):
        for i in range(len(value)):
            data['environment'][key][i] += value[i]
    else:
        data['environment'][key] = value

    with open(file, 'w') as env:
        yaml.safe_dump(data, env)

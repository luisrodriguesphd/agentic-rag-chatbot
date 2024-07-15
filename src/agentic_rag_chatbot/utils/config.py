import os
os.environ['HF_HOME'] = ".cache/huggingface"

import yaml

from dotenv import load_dotenv
from functools import lru_cache


def get_params():
    """
    Function to get the parameters.
    It load and parse the parameters from params.yml file.
    """

    params_path = os.path.join("conf", "params.yml")
    with open(params_path) as f:
        try:
            params = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise(e)
    
    for k, v in params.items():
        if "_dir" in k.lower():
            params[k] = os.path.join(*params[k])

    return params 

@lru_cache(maxsize=None)
def set_secrets():
    """
    Function to set the secrets.
    It load the parameters from .env file and set as env vars.
    """
    params = get_params()

    secrets_path = os.path.join(params['conf_dir'], params['secrets_file'])

    if os.path.exists(secrets_path):
        _ = load_dotenv(secrets_path, override=True)
    else:
        print(f'The secret file {secrets_path} does not exist!')

import json
from pprint import pprint
from collections import ChainMap


def load_settings(env):
    # assume file name is <env>.json
    with open(f'{env}.json') as f:
        settings = json.load(f)
    return settings


def settings(env):
    common_settings = load_settings('common')
    env_settings = load_settings(env)
    return chain_recursive(env_settings, common_settings)


def chain_recursive(d1, d2):
    chain = ChainMap(d1, d2)
    for k, v in d1.items():
        if isinstance(v, dict) and k in d2:
            chain[k] = chain_recursive(d1[k], d2[k])
    return chain


d1 = load_settings('common')
d2 = load_settings('dev')
d3 = load_settings('prod')

dev = chain_recursive(d2, d1)
prod = chain_recursive(d3, d1)

pprint(dev)
pprint(prod)

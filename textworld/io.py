import orjson as json
from pathlib import Path


def get_assets_path():
    return Path(__file__).parent / 'assets'

def load_json_asset(filename):
    with open(get_assets_path() / filename) as f:
        return json.loads(f.read())

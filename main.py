import json

from graph import Graph


def load_config(config_filename: str) -> dict:
    with open(config_filename) as f:
        config = json.load(f)
    return config


def pretty_print_config(config: dict):
    print(json.dumps(config, indent=2, sort_keys=False))


if __name__ == '__main__':
    config = load_config('config.json')
    graph = Graph(config)
    graph.show_plot()

import json

from graph import Graph, Point, LineSegment


def load_config(config_filename: str) -> dict:
    with open(config_filename) as f:
        config = json.load(f)
    return config


def pretty_print_config(config: dict):
    print(json.dumps(config, indent=2, sort_keys=False))


if __name__ == '__main__':
    config = load_config('config.json')
    graph = Graph(config)
    graph.add_point(Point(6, 6))
    graph.add_line(LineSegment(Point(1, 1), Point(7, 7)))
    graph.start_point = Point(1, 1)
    graph.end_point = Point(20, 20)
    graph.set_continuous_path([0, 1, 4], [5, 2, 4])
    graph.show_plot()

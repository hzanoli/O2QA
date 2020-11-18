import json


class AxisConfig:
    def __init__(self, view_range=None, log=False):
        self.view_range = view_range
        self.log = log


class PlotConfig:
    def __init__(self, x_axis=None, y_axis=None):
        if x_axis is not None:
            self.x_axis = AxisConfig(**x_axis)
        else:
            self.x_axis = AxisConfig()
        if y_axis is not None:
            self.y_axis = AxisConfig(**y_axis)
        else:
            self.y_axis = AxisConfig()


class JsonConfig(dict):
    def __init__(self, json_file_name=None):
        if json_file_name is not None:
            with open(json_file_name) as json_file:
                values = json.load(json_file)
                super().__init__({k: PlotConfig(**v) for k, v in values.items()})
        else:
            super(JsonConfig, self).__init__()

    def get(self, key):
        if super(JsonConfig, self).get(key) is not None:
            return super(JsonConfig, self).get(key)

        return PlotConfig()

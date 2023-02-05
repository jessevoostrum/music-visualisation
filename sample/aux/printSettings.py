import json


f = open('../fontSettings.json')
settings = json.load(f)


for key in settings['DejaVu Sans'].keys():
    print(f"self.{key} = fontDependentSettings['{key}']")
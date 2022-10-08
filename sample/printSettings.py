import json

f = open('settings.json')
settings = json.load(f)


for key in settings.keys():
    print(f"self.{key} = settings['{key}']")
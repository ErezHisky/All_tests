import json

with open('D:/Documents/TestersDocs/tpc.json') as f:
  tpc_data = json.load(f)

tpc_data["cells"][2]["pwr tx"]["static"]["total freqs"] = 4
tpc_data["cells"][2]["pwr tx"]["static"]["temps"][0]["tcp num p1db"] = [21, 22, 26]


with open('D:/Documents/TestersDocs/tpc1.json', 'w') as json_file:
  json.dump(tpc_data, json_file, indent=4)

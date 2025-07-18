import json 






filename = "data/test.json"

fakedata = [
    {'x0': 263, 'y0': 380, 'x1': 263, 'y1': 380, 'color': '#000000', 'lineWidth': '5'},
     {'x0': 263, 'y0': 380, 'x1': 263, 'y1': 380, 'color': '#000000', 'lineWidth': '5'}       
            ]

with open(filename, 'r') as file:
    data = json.load(file)
    print(data)


with open(filename, 'w') as file:
    data['contents'] = fakedata
    json.dump(data, file, indent=4)
    print("Data written to file successfully.")

    print(data['contents'])


with open(filename, 'r') as file:
    data = json.load(file)
    print("Updated data:", data)
    print("Contents:", data['contents'])
    print("Contents length:", len(data['contents']))
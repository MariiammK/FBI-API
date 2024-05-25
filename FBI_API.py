import requests
import json
import sqlite3

info = {}


#dallas, miami, chicago, houston,
# location = 'miami'
location = input("Enter location: ")


url = 'https://api.fbi.gov/wanted/v1/list'
param = {'field_offices': location}

response = requests.get(url, params=param)

print("Response: ", response)
print("Status Code:", response.status_code)
print("Headers: ", response.headers)
print("Server: ", response.headers['Server'])
print("Date: ", response.headers['Date'])
print("Result in str format: ", response.text)
#
content = response.json()
print(json.dumps(content, indent=4))


## json ფაილის შექმნა
file = open('FBI_data.json', 'w')
json.dump(content, file, indent=4)


## json ფაილიდან ინფოს ამოკითხვა
# მითითებულ ქალაქში ძებნილ დამნაშავეთა რაოდენობა
def totsl(c):
    print(c["total"])

# სრული ინფორმაცია კონკრეტული დამნაშავის შესახებ
def all_info(c, n):   # n - meromele index?
    print(json.dumps(c["items"][n], indent=4))

# მნიშვნელოვანი ინფორმაცია კონკრეტული დამნაშავის შესახებ
def important_info(c, n):
    global info   # მონაცემების Dictionary-ში შენახვა დამჭირდა, რათა ინფორმაციის არარსებობის შემთხვევაში, None არ დაებეჭდა

    info["subjects"] = c["items"][n]["subjects"]
    info["title"] = c["items"][n]["title"]
    info["description"] = c["items"][n]["description"]
    info["race"] = c["items"][n]["race"]
    info["nationality"] = c["items"][n]["nationality"]
    info["place of birth"] = c["items"][n]["place_of_birth"]
    info["sex"] = c["items"][n]["sex"]
    info["minimal age"] = c["items"][n]["age_min"]
    info["age range"] = c["items"][n]["age_range"]
    info["Maximal Wight"] = c["items"][n]["weight_max"]
    info["Maximal Height"] = c["items"][n]["height_max"]
    info["hair"] = c["items"][n]["hair"]
    info["eyes"] = c["items"][n]["eyes"]

    for i, j in info.items():
        if j == None:
            print("{}:  information not found ".format(i))
        else:
            print("{}:  {} ".format(i, j))

# დამნაშავის ყალბი სახელები
def aliases(c, n):
    if (c["items"][n]["aliases"] != None):
        print("Aliases:")
        for i in range(len(c["items"][n]["aliases"])):
            print(i+1, c["items"][n]["aliases"][i])
    else:
        print("No aliases found")


## json ფაილიდან ინფოს ამოკითხვა
with open('FBI_data.json', 'r') as file:
    c = json.load(file)
    print(c)

    # მომხმარებლის სურვილის მიხედვით გამოიძახება აღნიშნული ფუნქციები:
    n = int(input("Enter the appropriate number \n1. How many people are wanted by the FBI? \n2. Need important information about specific person \n3. Need all information about specific person \n4. Need info about aliases"))
    id = None
    if n == 2 or n == 3 or n == 4:
        id = int(input("Which person's information do you want to receive in the list, enter number: "))

    if n == 1:
        totsl(c)
    elif n == 2:
        important_info(c, id)
    elif n == 3:
        all_info(c, id)
    elif n == 4:
        aliases(c, id)
    else:
        print("incorrect number")


## ბაზის შექმნა და მასში ინფორმაციის შენახვა
conn = sqlite3.connect('FBI_Data1.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS wanted (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title VARCHAR(100),
        Sex VARCHAR(50),
        Nationality VARCHAR(100),
        Race VARCHAR(100),
        Image VARCHAR(100)
    )
''')

# # ინახავს ინფორმაციას დამნაშავის სახელის, სქესის, ეროვნებისა და რასის შესახებ
# pers = (content["items"][n]["title"],
#         content["items"][n]["sex"],
#         content["items"][n]["nationality"],
#         content["items"][n]["race"])

# c.execute('''INSERT INTO wanted (Title, Sex, Nationality, Race) VALUES (?, ?, ?, ?)''', pers)
# conn.commit()


# # ინახავს ინფორმაციას დამნაშავეების სახელის, სქესის, ეროვნების, რასის შესახებ და მათი სურათის ლინკს
data = response.json()["items"]

dataa = []
for i in data:
    dataa.append(
        (i["title"],
         i["sex"],
         i["nationality"],
         i["race"],
         i["images"][0]["original"],)
    )

c.executemany("INSERT INTO wanted (Title, Sex, Nationality, Race, Image) VALUES (?, ?, ?, ?, ?)", dataa)
conn.commit()


# ბაზიდან ინფორმაციის დაბეჭდვა
# ბეჭდავს იმ ადამიანების სახელებს, რომელთა სქესიც არის მამრობითი
gender = c.execute("SELECT * FROM wanted WHERE Sex = 'Male'")

for i in gender:
    print(i["Title"])

conn.close()











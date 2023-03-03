from bs4 import BeautifulSoup
import os

# Iterate folders to create array of Car names
handlings = './handlings'
carnames = [name for name in os.listdir(handlings) if os.path.isdir(os.path.join(handlings, name))]

# Extfiles name will be the corresponding value of value we're scraping from each Handling.meta, for each vehicle
# Currently, we are scraping fInitialDriveForce, fInitialDriveMaxFlatVel, fCollisionDamageMult and fWeaponDamageMult
extfiles = ["fInitialDriveForce.txt","fInitialDriveMaxFlatVel.txt","fCollisionDamageMult.txt","fWeaponDamageMult.txt"]

# Clears the content of external files so if we re-run the script, it doesnt append to existing content
print("Cleaning param files...")
for file in extfiles:
    f = open(file, 'r+')
    f.truncate(0)

# Get parameter values and remove '.txt'
accel = extfiles[0].split(".")[0]
topspeed = extfiles[1].split(".")[0]
coldmg = extfiles[2].split(".")[0]
wsdmg = extfiles[3].split(".")[0]

# Get values and write to file for each parameter we've defined above
def get_values(param):
    soup2  = soup.find(param)
    value = soup2['value']
    if value == None:
        value = "ERROR"
    #print("{ VehicleHashCode." + car.capitalize() + ", " + value + " },")
    paramfile = param + ".txt"
    with open(paramfile, 'a') as the_file:
        the_file.write("{ VehicleHashCode." + car[0].upper() + car[1:] + ", " + value + " },\n")

# Iterate over each car and populate new file with values
print("Scraping values...")
for car in carnames:
    handlingpath = handlings + "/" + car + "/handling.meta"
    with open(handlingpath, 'r') as f:
        data = f.read()
        soup = BeautifulSoup(data, "xml")
        get_values(accel)
        get_values(topspeed)
        get_values(coldmg)
        get_values(wsdmg)

cars_hashvalues_from_server = []
with open("vehHashValues.txt") as hashvalues:
    for line in hashvalues:
        cars_hashvalues_from_server.append(line.split(" = ")[0])

capitalized_cars = [car[0].upper() + car[1:] for car in carnames]
cars_set1 = set(cars_hashvalues_from_server)
cars_set2 = set(capitalized_cars)
missing_vehs = cars_set1 - cars_set2

print("Missing Vehicles from Hashvalues: ", missing_vehs)

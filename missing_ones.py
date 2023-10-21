import os
import requests

# Function to download an image from a URL
def download_image(url, folder_path, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(folder_path, filename), 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

# Read the list of vehicles with numbers from not_found_vehicles.txt
with open("not_found_vehicles.txt", "r") as txt_file:
    vehicles_with_numbers = [line.strip() for line in txt_file.readlines()]

# Create a folder to store the downloaded images
output_folder = './car_images'
os.makedirs(output_folder, exist_ok=True)

base_url = "" # get the base url

# List to store vehicles that are still not found
still_not_found = []

for vehicle_name in vehicles_with_numbers:
    parts = vehicle_name.split()
    if len(parts) > 1 and parts[-1].isnumeric():
        modified_name = parts[0] + '_' + parts[-1]
        car_url = base_url + modified_name.capitalize()
        page = requests.get(car_url)

        if page.status_code == 200:
            image_url = None  # Initialize to None

            if image_url:
                image_filename = f"{vehicle_name}.png"
                download_image(image_url, output_folder, image_filename)
                print(f"Downloaded image for {vehicle_name}")
            else:
                still_not_found.append(vehicle_name)
        else:
            still_not_found.append(vehicle_name)
    else:
        still_not_found.append(vehicle_name)

print("Vehicles still not found:")
for vehicle in still_not_found:
    print(vehicle)

with open("still_not_found_vehicles.txt", "w") as txt_file:
    for vehicle in still_not_found:
        txt_file.write(vehicle + "\n")

print("Image download for modified names and updated not found list completed.")
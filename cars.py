import time
from bs4 import BeautifulSoup
import os
import requests

# Function to download an image from a URL


def download_image(url, folder_path, filename):
    # response = requests.get(url)
    # if response.status_code == 200:
    #     with open(os.path.join(folder_path, filename), 'wb') as file:
    #         file.write(response.content)
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(folder_path, filename), 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)


# Iterate folders to create an array of Car names
handlings = './handlings'
carnames = [name for name in os.listdir(
    handlings) if os.path.isdir(os.path.join(handlings, name))]

# Create a folder to store the downloaded images
output_folder = './car_images'
os.makedirs(output_folder, exist_ok=True)

base_url = "" # Get the base url for images
not_found_vehicles = []  # Create an empty list to store the names of vehicles not found

for carname in carnames:
    # Generate the URL for the car's page
    suffix = "-GTAV-front.png"
    car_url = base_url + carname.capitalize()
    page = requests.get(car_url)

    print(car_url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        
        # Find all <figure> elements with class "pi-item pi-image"
        figure_elements = soup.find_all("figure", {"class": "pi-item pi-image"})

        if len(figure_elements) >= 2:
            # Get the second <figure> element (index 1)
            second_figure_element = figure_elements[1]
            
            # Find the <a> tag within the second <figure>
            image_link = second_figure_element.find("a", {"class": "image image-thumbnail"})
            
            if image_link and 'href' in image_link.attrs:
                # Extract the 'href' attribute, which is the image URL
                image_url = image_link['href']
                image_filename = f"{carname}.png"
                print(image_url)
                download_image(image_url, output_folder, image_filename)
                print(f"Downloaded image for {carname}")
            else:
                not_found_vehicles.append(carname)  # Vehicle not found, add to the list
        else:
            not_found_vehicles.append(carname)  # Vehicle not found, add to the list
    else:
        not_found_vehicles.append(carname)  # Vehicle not found, add to the list
        print(f"Failed to fetch {car_url}")

# Print the list of vehicles not found
print("Vehicles not found/downloaded:")
for vehicle in not_found_vehicles:
    print(vehicle)

# Write the list to a .txt file
with open("not_found_vehicles.txt", "w") as txt_file:
    for vehicle in not_found_vehicles:
        txt_file.write(vehicle + "\n")

print("Image download and not found list completed.")


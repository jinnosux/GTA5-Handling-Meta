from PIL import Image
import os

input_folder = "car_images"
output_folder = "resized_car_vehicles"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

image_files = os.listdir(input_folder)

new_width = 576
new_height = 324

# Set the compression quality (0-100, higher values mean better quality)
compression_quality = 60

for image_file in image_files:
    if image_file.lower().endswith((".png", ".jpg", ".jpeg")):
        image_path = os.path.join(input_folder, image_file)
        img = Image.open(image_path)
        
        img = img.convert("RGB")
        
        resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        
        lowercase_image_file = image_file.lower()
        
        output_path = os.path.join(output_folder, lowercase_image_file)
        resized_img.save(output_path, format="JPEG", quality=compression_quality)
        
        print(f"Resized {image_file} to {new_width}x{new_height} with quality {compression_quality}")

print("Image resizing and compression completed.")

if not os.path.exists(output_folder):
    print(f"The folder '{output_folder}' does not exist.")
else:
    for filename in os.listdir(output_folder):
        if os.path.isfile(os.path.join(output_folder, filename)):
            new_filename = filename.lower()
            if filename != new_filename:
                try:
                    os.rename(os.path.join(output_folder, filename), os.path.join(output_folder, new_filename))
                    print(f"Renamed '{filename}' to '{new_filename}'")
                except Exception as e:
                    print(f"Failed to rename '{filename}': {str(e)}")
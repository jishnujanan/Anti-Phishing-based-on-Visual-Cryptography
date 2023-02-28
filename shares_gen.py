import os
from PIL import Image
import numpy as np

def generate_shares(image_array, k, n):
    # Get the shape of the input image
    height, width, channels = image_array.shape

    # Initialize a list to hold the shares
    shares = []

    # Generate k-1 random arrays with the same shape as the input image
    for i in range(k-1):
        random_array = np.random.randint(0, 256, size=(height, width, channels))
        shares.append(random_array)

    # Compute the last share as the XOR of the input image and all the random arrays
    last_share = image_array.copy()
    for share in shares:
        last_share = np.bitwise_xor(last_share, share)
    shares.append(last_share)

    # Return the list of shares
    return shares

def split_image(image_path, k, n, output_dir):
    # Load the input image
    image = Image.open(image_path).convert("RGB")

    # Convert the image to a NumPy array
    image_array = np.array(image)

    # Split the image into k shares with a threshold of n
    shares = generate_shares(image_array, k, n)

    # Save each share as a separate image file
    for i, share in enumerate(shares):
        # Convert the share array to a PIL.Image object
        share = share.astype('uint8')
        share_image = Image.fromarray(share)

        # Save the share image to a file
        share_path = os.path.join(output_dir, f"share_{i+1}.png")
        share_image.save(share_path)

    # Return the list of share paths
    return [os.path.join(output_dir, f"share_{i+1}.png") for i in range(k)]


def recombine_shares(share_paths, output_path):
    # Load the first share image and get its size
    share_image = Image.open(share_paths[0])
    share_width, share_height = share_image.size

    # Initialize an array to hold the recombined image
    recombined_image = np.zeros((share_height, share_width, 3), dtype=np.uint8)

    # XOR all the share arrays to obtain the recombined image array
    for share_path in share_paths:
        share_image = Image.open(share_path)
        share_array = np.array(share_image)
        recombined_image = np.bitwise_xor(recombined_image, share_array)

    # Convert the recombined image array to a PIL.Image object and save it to a file
    recombined_image = Image.fromarray(recombined_image)
    recombined_image.save(output_path)

    # Return the path to the recombined image file
    return output_path

input_image_path = "captcha.png"
output_dir = "share_images"
k = 2
n = 2
# Split the input image into shares and save them as separate image files
share_paths = split_image(input_image_path, k, n, output_dir)

print("Share images saved to:")
for share_path in share_paths:
    print(share_path)
output_path = "recombined_image.png"

# Recombine the shares into the original image and save it to a file
recombined_path = recombine_shares(share_paths, output_path)

print("Recombined image saved to:")
print(recombined_path)

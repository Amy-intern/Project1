import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import BytesIO
from PIL import Image
import imagehash

# File path
momo = "C:/Users/aimee/Documents/Workspace/Project 1/Scrapers/storage/key_value_stores/default/results.csv"
print(momo)
list_of_platforms = [momo]
official_brand_name = "NIKE 耐吉"

plt.rc('font', family='Microsoft JhengHei')

def fetch_image_from_url(url):
    """Fetch an image from a URL and return a PIL Image object."""
    response = requests.get(url)
    response.raise_for_status()
    image_data = BytesIO(response.content)
    return Image.open(image_data)

def compute_image_hash(image):
    """Compute the perceptual hash of a PIL image."""
    return imagehash.phash(image)

def counting_brands(csv_name):
    count_brands = {}
    count_images = {}
    image_hashes = {}  # To store image hashes and their corresponding URLs

    for chunk in pd.read_csv(csv_name, chunksize=10):
        for _, entry in chunk.iterrows():
            # Ensure the columns exist in the DataFrame
            if 'brand' in entry and 'image' in entry and 'product_name' in entry:
                if entry['brand'] != official_brand_name:
                    # Count brands
                    if entry['brand'] in count_brands:
                        count_brands[entry['brand']] += 1
                    else:
                        count_brands[entry['brand']] = 1

                    # Process images and compute hashes
                    image_url = entry['image']
                    try:
                        image = fetch_image_from_url(image_url)
                        image_hash = compute_image_hash(image)

                        # Group images by their perceptual hash
                        hash_key = str(image_hash)
                        if hash_key in image_hashes:
                            image_hashes[hash_key].append(image_url)
                        else:
                            image_hashes[hash_key] = [image_url]

                        # Count images by product names
                        if entry['product_name'] in count_images:
                            count_images[entry['product_name']].append(image_url)
                        else:
                            count_images[entry['product_name']] = [image_url]
                    
                    except Exception as e:
                        print(f"Error processing image {image_url}: {e}")

    # Convert image counts by product name
    count_images = {k: len(v) for k, v in count_images.items()}

    # Plot brand counts
    plt.bar(count_brands.keys(), count_brands.values())
    plt.xlabel('Brands')
    plt.ylabel('Number of Results')
    plt.title('Number of Entries per Unofficial Supplier')
    plt.tight_layout()
    plt.show()
    
    # Plot product name counts
    plt.figure(figsize=(13, 8))
    plt.barh(count_images.keys(), count_images.values())
    plt.ylabel('Product Names')
    plt.xlabel('Number of Results')
    plt.title('Number of Unofficial Entries per Product')
    plt.tight_layout()
    plt.show()

    # Optional: Print out image hash details
    for hash_key, urls in image_hashes.items():
        print(f'Hash: {hash_key}, Number of Images: {len(urls)}')

for i in list_of_platforms:
    counting_brands(i)
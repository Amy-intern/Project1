"""import pandas as pd
import matplotlib.pyplot as plt


momo = "C:/Users/aimee/Documents/Workspace/Project 1/Scrapers/storage/key_value_stores/default/results.csv"
print(momo)
list_of_platforms = [momo]
official_brand_name = "NIKE 耐吉"

plt.rc('font', family='Microsoft JhengHei')


def counting_brands(csv_name):
    count_brands = {}
    count_images = {}
    for chunk in pd.read_csv(csv_name, chunksize=10):
        for _, entry in chunk.iterrows():
            # Ensure the columns exist in the DataFrame
            if 'brand' in entry and 'image' in entry and 'product_name' in entry:
                if entry['brand'] != official_brand_name:
                    if entry['brand'] in count_brands.keys():
                        count_brands[entry['brand']] += 1
                    else:
                        count_brands[entry['brand']] = 1

                    if entry['product_name'] in count_images:
                        count_images[entry['product_name']].append(entry['image'])
                    else:
                        count_images[entry['product_name']] = [entry['image']]
    
    # Fix the assignment to the dictionary
    count_images = {k: len(v) for k, v in count_images.items()}
    
    plt.bar(count_brands.keys(), count_brands.values())
    plt.xlabel('Brands')
    plt.ylabel('Number of Results')
    plt.title('Number of Entries per Unofficial Supplier')
    plt.tight_layout()
    plt.show()
    
    plt.figure(figsize=(13, 8))
    plt.barh(count_images.keys(), count_images.values())
    plt.ylabel('Product Names')
    plt.xlabel('Number of Results')
    plt.title('Number of Unofficial Entries per Product')
    plt.tight_layout()
    plt.show()

for i in list_of_platforms:
    counting_brands(i)"""

import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import io
import urllib.request

# CSV file path
momo = "C:/Users/aimee/Documents/Workspace/Project 1/Scrapers/storage/key_value_stores/default/results.csv"
list_of_platforms = [momo]
official_brand_name = "NIKE 耐吉"

# Set up the font for the plots
plt.rc('font', family='Microsoft JhengHei')

def compare_images_from_url(url_1, url_2):
    """
    Compare two images pixel by pixel by downloading them from their URLs using urllib.
    Returns True if they are identical, False otherwise.
    """
    try:
        # Download the images using urllib
        with urllib.request.urlopen(url_1) as url1:
            img1 = Image.open(io.BytesIO(url1.read())).convert('RGB')

        with urllib.request.urlopen(url_2) as url2:
            img2 = Image.open(io.BytesIO(url2.read())).convert('RGB')

        # Resize the images to the same size (optional, but often needed)
        if img1.size != img2.size:
            img2 = img2.resize(img1.size)

        # Convert images to numpy arrays
        img1_array = np.array(img1)
        img2_array = np.array(img2)

        # Compare pixel by pixel
        return np.array_equal(img1_array, img2_array)

    except Exception as e:
        print(f"Error comparing images from URLs {url_1} and {url_2}: {e}")
        return False


def counting_brands(csv_name):
    count_brands = {}
    count_images = {}
    image_groups = {}  # To store grouped image URLs that are identical

    for chunk in pd.read_csv(csv_name, chunksize=10):
        for _, entry in chunk.iterrows():
            # Ensure the columns exist in the DataFrame
            if 'brand' in entry and 'image' in entry and 'product_name' in entry:
                # Only process entries that are not from the official brand
                if entry['brand'] != official_brand_name:
                    # Count occurrences of each brand
                    if entry['brand'] in count_brands:
                        count_brands[entry['brand']] += 1
                    else:
                        count_brands[entry['brand']] = 1

                    # Image comparison and grouping based on similarity
                    image_url = entry['image']  # Assuming this is a URL to an image
                    found_similar = False

                    # Compare with existing groups of images
                    for group in image_groups.values():
                        if compare_images_from_url(image_url, group[0]):
                            group.append(image_url)
                            found_similar = True
                            break

                    # If no similar image found, create a new group
                    if not found_similar:
                        image_groups[len(image_groups)] = [image_url]

                    # Count images by product names
                    if entry['product_name'] in count_images:
                        count_images[entry['product_name']].append(image_url)
                    else:
                        count_images[entry['product_name']] = [image_url]

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

    

# Run the analysis for each platform in the list
for i in list_of_platforms:
    counting_brands(i)

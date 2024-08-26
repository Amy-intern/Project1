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
    #Gets Pil image from url
    response = requests.get(url)
    image_data = BytesIO(response.content) #gets content of the image
    return Image.open(image_data)

def compute_image_hash(image):
    #Gets perceptual hash of a PIL image.
    return imagehash.phash(image)

def is_similar(hash1, hash2):
    # Checks similarity
    if hash1 - hash2 <= 5:
        return True
    else:
        return False

def counting_brands(csv_name):
    count_brands = {}
    count_images = {}
    image_hashes = {}  

    for chunk in pd.read_csv(csv_name, chunksize=10):
        for _, entry in chunk.iterrows():
            if entry['brand'] != official_brand_name:
                
                if entry['brand'] in count_brands:
                    count_brands[entry['brand']] += 1
                else:
                    count_brands[entry['brand']] = 1
                
                #Get shashes
                image_url = entry['image']
                
                image = fetch_image_from_url(image_url)
                image_hash = compute_image_hash(image)

                # Groups images by p-hash
                hash_key = str(image_hash)
                
                for i in image_hashes:
                    if is_similar(image_hash, i):
                        image_hashes[hash_key].append(image_url)
                    else:
                        image_hashes[hash_key].append(image_url)

                # Counts images by product name
                if entry['product_name'] in count_images:
                    count_images[entry['product_name']].append(image_url)
                else:
                    count_images[entry['product_name']] = [image_url]

    # Convert image counts by product name
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
    counting_brands(i)
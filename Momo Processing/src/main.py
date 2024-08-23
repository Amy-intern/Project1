import pandas as pd
import matplotlib.pyplot as plt

momo = "C:/Users/aimee/Documents/Workspace/Project 1/Scrapers/storage/key_value_stores/default/results.csv"
print(momo)
list_of_platforms = [momo]
official_brand_name = "Nike"

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
    counting_brands(i)
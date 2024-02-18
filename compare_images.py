import os
import csv
import sys

def list_directories(path, skip_list):
    """List directories in a given path, excluding any that match the skip list"""
    all_dirs = next(os.walk(path))[1]
    return [d for d in all_dirs if all(not skip_term in d for skip_term in skip_list)]

def has_fips_variant(base_image, all_dirs):
    """Check if a base image has a corresponding '-fips' variant"""
    return "YES" if f"{base_image}-fips" in all_dirs else "NO"

def compare_directories(dir1, dir2, skip_list):
    """Compare two directories and return a list of tuples with comparison data"""
    dir1_contents = set(list_directories(dir1, skip_list))
    dir2_contents = set(list_directories(dir2, skip_list))
    all_dirs = dir1_contents.union(dir2_contents)  # Combine all unique directories

    base_images = sorted([img for img in all_dirs if "-fips" not in img])

    comparison_list = []

    # Initialize counters
    only_in_dir1 = 0
    only_in_dir2 = 0
    total_fips_images = 0  # Counter for FIPS images

    for image in all_dirs:  # Iterating through all_dirs to count FIPS
        if "-fips" in image:
            total_fips_images += 1  # Increment FIPS counter

    for image in base_images:
        in_dir1 = "YES" if image in dir1_contents else "NO"
        in_dir2 = "YES" if image in dir2_contents else "NO"
        fips_variant = has_fips_variant(image, all_dirs)  # Check for FIPS variant using all_dirs, not filtered

        if in_dir1 == "YES" and in_dir2 == "NO":
            only_in_dir1 += 1
        elif in_dir1 == "NO" and in_dir2 == "YES":
            only_in_dir2 += 1

        comparison_list.append((image, in_dir1, in_dir2, fips_variant))

    return comparison_list, only_in_dir1, only_in_dir2, len(base_images), total_fips_images

def write_csv(data, output_file='images.csv'):
    """Write the comparison data to a CSV file"""
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image", "Found in Public Images", "Found in Private Images", "FIPS Variant"])
        writer.writerows(data)

def main(dir1, dir2):
    skip_list = ['request-', 'TEMPLATE']  # Add any other patterns or specific names to skip here

    comparison_data, only_in_dir1, only_in_dir2, total_images, total_fips_images = compare_directories(dir1, dir2, skip_list)
    write_csv(comparison_data)
    print(f"Comparison CSV has been created as images.csv")
    print(f"Total images found in public but missing in private: {only_in_dir1}")
    print(f"Total images found in private but missing in public: {only_in_dir2}")
    print(f"Total unique images: {total_images}")
    print(f"Total FIPS images: {total_fips_images}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py [public directory path] [private directory path]")
    else:
        main(sys.argv[1], sys.argv[2])


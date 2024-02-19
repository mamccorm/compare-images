import os
import csv
import sys

def list_directories(path, skip_list):
    """List directories in a given path, excluding any that match the skip list."""
    all_dirs = next(os.walk(path))[1]
    return [d for d in all_dirs if all(skip_term not in d for skip_term in skip_list)]

def has_fips_variant(base_image, all_dirs):
    """Check if a base image has a corresponding '-fips' variant."""
    return "YES" if f"{base_image}-fips" in all_dirs else "NO"

def compare_directories(dir1, dir2, skip_list):
    """Compare two directories and return a list of tuples with comparison data."""
    dir1_all_dirs = list_directories(dir1, [])  # Include 'request-' and '-fips' images
    dir2_all_dirs = list_directories(dir2, [])  # Include 'request-' and '-fips' images
    
    # Total count before deduplication and filtering
    total_count_before_filtering = len(dir1_all_dirs) + len(dir2_all_dirs)

    # Count 'custom' images prefixed with 'request-' only in the private directory
    custom_images_count = sum(1 for name in dir2_all_dirs if name.startswith('request-'))

    # Apply skip_list for the comparison
    dir1_dirs = list_directories(dir1, skip_list)  # Public images
    dir2_dirs = list_directories(dir2, skip_list)  # Private images, exclude 'request-' and '-fips'

    # Sets for comparison
    dir1_contents = set(dir1_dirs)
    dir2_contents = set(dir2_dirs)

    # Base images: Exclude -fips from both sets to identify original images
    base_images = sorted(set(img for img in dir1_contents.union(dir2_contents) if "-fips" not in img))

    comparison_list = []
    total_fips_images = 0
    images_without_fips = 0  # Counter for unique images missing FIPS versions

    for base_image in base_images:
        fips_variant = f"{base_image}-fips"
        in_dir1 = "YES" if base_image in dir1_contents else "NO"
        in_dir2 = "YES" if base_image in dir2_contents else "NO"
        has_fips = "YES" if fips_variant in dir2_contents else "NO"  # Check for -fips variant only in private dir

        if has_fips == "YES":
            total_fips_images += 1
        else:
            images_without_fips += 1  # Increment if no FIPS variant found

        comparison_list.append((base_image, in_dir1, in_dir2, has_fips))

    total_without_fips = len(base_images) - total_fips_images

    return comparison_list, len(dir1_contents), len(dir2_contents), total_fips_images, total_without_fips, custom_images_count, total_count_before_filtering, images_without_fips

def write_csv(data, output_file='images.csv'):
    """Write the comparison data to a CSV file."""
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image", "Found in Public Images", "Found in Private Images", "FIPS Variant"])
        writer.writerows(data)

def main(dir1, dir2):
    skip_list = ['request-', 'TEMPLATE']

    comparison_data, total_public_dirs, total_private_dirs, total_fips_images, total_without_fips, custom_images_count, total_count_before_filtering, images_without_fips = compare_directories(dir1, dir2, skip_list)
    write_csv(comparison_data)

    print(f"\nTotal image (directory) count: {total_count_before_filtering}")
    print(f"- Total public image (directories): {total_public_dirs}")
    print(f"- Total private image (directories): {total_private_dirs}\n")
    
    print(f"Total unique images: {len(comparison_data)}")
    print(f"- FIPS images: {total_fips_images}")
    print(f"- Custom images: {custom_images_count}")
    print(f"- Unique images (minus FIPS and custom): {len(comparison_data) - total_fips_images - custom_images_count}\n")

    print(f"-----------------------------------------------------------")
    print(f"Total images found in public but missing in private: {sum(1 for _, in_dir1, in_dir2, _ in comparison_data if in_dir1 == 'YES' and in_dir2 == 'NO')}")
    print(f"Total images found in private but missing in public: {sum(1 for _, in_dir1, in_dir2, _ in comparison_data if in_dir1 == 'NO' and in_dir2 == 'YES')}")
    print(f"Total unique images missing FIPS versions: {images_without_fips}\n")
    
    print(f"**Comparison CSV has been created as images.csv**\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py [public directory path] [private directory path]")
    else:
        main(sys.argv[1], sys.argv[2])
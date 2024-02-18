# Directory Comparison Tool

## Description

This tool is designed to compare the contents of two directories, typically representing different sets of container images, and output the comparison in a CSV format. It is particularly useful for visualizing which images exist in either one or both specified directories.

## Features

- Compares two directories and lists all unique subdirectories.
- Outputs a CSV file indicating the presence of each subdirectory in each of the compared directories.
- Easy to use with command-line arguments.

## Requirements

- Python 3.x

## Installation

No installation is needed. Just ensure you have Python 3.x installed on your system.

## Usage

To use this script, navigate to the directory containing `directory_compare.py` and run:

```bash
python3 compare_images.py [public directory path] [private directory path]
```

Replace `[public directory path]` and `[private directory path]` with the actual paths of your directories.

### Arguments:

- **public directory path**: The path to the first directory (typically representing public images).
- **private directory path**: The path to the second directory (typically representing private images).

### Output:

The script will output a CSV file named `images.csv` in the same directory as the script. The CSV format is as follows:

- **Image**: The name of the image (or subdirectory).
- **Found in Public Images**: Indicates if the image is found in the first directory ("YES" or "NO").
- **Found in Private Images**: Indicates if the image is found in the second directory ("YES" or "NO").

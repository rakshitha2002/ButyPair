# ButyPair
This tool allows users to upload an image and recognize the dominant colors present in the image. Based on the colors recognized, the tool suggests pairing items with the same or complementary colors.

## Installation
1. Clone the repository to your local machine.
1. Install the necessary Python packages by running `pip install -r requirements.txt` in your command prompt or terminal.

## Usage
1. Navigate to the cloned repository.
1. Run the command `python start.py`.
1. Upload an image by clicking on the "Drag & Drop / Click to upload image" button.
1. Wait for the tool to recognize the colors present in the image.
1. The tool will suggest pairing items with the same or complementary colors.
1. You can directly navigate to e-commerce website for the recommended items. 

## Modules
This tool consists of the following modules:

- **Image Recognition**: This module uses the ImageAI Python module to recognize the objects in the uploaded image.
- **Color Recognition**: This module uses thecolorapi to recognize the dominant colors present in the uploaded image.
- **Color Matching**: This module matches the base color of the selected item with colors present in popular color schemes such as complementary, analogous, and triadic, and suggests color schemes that work well with the base color.
- **E-commerce Link Generation**: This module gets the selected item type and the color information to generate direct links to e-commerce websites where users can purchase the recommended items.

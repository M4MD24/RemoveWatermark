# RemoveWatermark

A lightweight Python tool for detecting and removing watermarks from images while protecting dark text from unnecessary modification.

## Features

- Remove detected watermarks from images.
- Protect dark text during watermark removal.
- Process a single image.
- Process images recursively inside a folder.
- Support multiple image formats.
- Preserve the original directory structure when processing folders.
- Save processed images to a separate output directory.
- Use OpenCV for image processing.

## Current Requirements

- Python 3.14

## Usage

Run the program with a file or folder path:

```bash
python main.py "C:\Images"
```

Or process a single image:

```bash
python main.py "C:\Images\image.png"
```

## How It Works

1. Detects supported image files.
2. Identifies potential watermark areas using HSV color information.
3. Detects and protects dark text.
4. Creates and cleans a mask for the detected watermark.
5. Removes the watermark using OpenCV inpainting.
6. Restores protected text from the original image.
7. Saves the processed image to the output directory.
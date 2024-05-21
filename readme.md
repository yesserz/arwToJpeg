# ARW to JPEG Converter

## Description

This program converts ARW (Sony RAW) files to JPEG format using the `rawpy` and `Pillow` libraries. The program displays the conversion progress using the `tqdm` library.

## Requirements

To run the program, you need the following components:

- Python 3.x
- Pillow library
- rawpy library
- tqdm library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yesserz/arwToJpeg.git
    ```

2. Navigate to the project directory:

    ```sh
    cd arw-to-jpeg-converter
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

The program is executed from the command line and takes two arguments: the path to the input folder containing `.arw` files and the path to the output folder for saving `.jpeg` files.

### Example Usage

```sh
python convert.py ./input ./output

# ARW to JPEG Converter

## Description

This program converts ARW (Sony RAW) files to JPEG format using the `rawpy` and `Pillow` libraries. The program displays the conversion progress using the `tqdm` library for command-line usage and a progress bar in the graphical interface. The GUI also shows detailed information about the number of files being processed, the current file, elapsed time, and estimated remaining time.

## Requirements

To run the program, you need the following components:

- Python 3.x
- Pillow library
- rawpy library
- tqdm library
- tkinter (comes with Python standard library)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yesserz/arwToJpeg.git
    ```

2. Navigate to the project directory:

    ```sh
    cd arwToJpeg
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Command Line Interface

The program can be executed from the command line and takes two arguments: the path to the input folder containing `.arw` files and the path to the output folder for saving `.jpeg` files.

#### Example Usage

```sh
python convert.py --input_folder ./input --output_folder ./output
```

where:
- `./input` is the path to the folder containing `.arw` files.
- `./output` is the path to the folder where the converted `.jpeg` files will be saved.

#### Program Output Example

```sh
$ python convert.py --input_folder ./arw_files --output_folder ./jpeg_files
Converting: 100%|██████████████████████████████████████████████████████████████████████| 10/10 [00:15<00:00,  1.50s/file]
```

### Graphical User Interface

If no command line arguments are provided, the program will launch a graphical user interface (GUI) for selecting the input and output folders. The GUI also displays the conversion progress and additional information about the files being processed.

#### Using the GUI

1. Run the program without arguments:

```sh
python convert.py
```

2. In the GUI, click "Browse" to select the input folder containing `.arw` files.
3. Click "Browse" to select the output folder where the converted `.jpeg` files will be saved.
4. Click "Start Conversion" to begin the conversion

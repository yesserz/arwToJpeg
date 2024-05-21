import argparse
import logging
import os

import rawpy
from PIL import Image
from tqdm import tqdm


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )


def convert_arw_to_jpeg(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"Input folder '{input_folder}' does not exist.")

    arw_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".arw")]
    total_files = len(arw_files)

    if total_files == 0:
        logging.warning(f"No .arw files found in '{input_folder}'")
        return

    with tqdm(total=total_files, desc="Converting", unit="file") as pbar:
        for filename in arw_files:
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + ".jpeg"
            output_path = os.path.join(output_folder, output_filename)

            try:
                with rawpy.imread(input_path) as raw:
                    rgb = raw.postprocess()
                    img = Image.fromarray(rgb)
                    img.save(output_path, "JPEG")
                pbar.update(1)
                pbar.set_postfix(file=filename)
            except Exception as e:
                logging.error(f"Error converting {filename}: {e}")
                pbar.set_postfix(file=filename, error=str(e))


def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Convert ARW files to JPEG.")
    parser.add_argument("input_folder", type=str, help="Path to the input folder containing .arw files")
    parser.add_argument("output_folder", type=str, help="Path to the output folder for .jpeg files")

    args = parser.parse_args()

    convert_arw_to_jpeg(args.input_folder, args.output_folder)


if __name__ == "__main__":
    main()

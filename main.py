from PIL import Image
import os
import rawpy
from tqdm import tqdm


def convert_arw_to_jpeg(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    arw_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".arw")]
    total_files = len(arw_files)

    with tqdm(total=total_files, desc="Converting", unit="file") as pbar:
        for filename in arw_files:
            input_path = os.path.join(input_folder, filename)

            # Generate the output file path with .jpeg extension
            output_filename = os.path.splitext(filename)[0] + ".jpeg"
            output_path = os.path.join(output_folder, output_filename)

            # Convert ARW to JPEG
            try:
                with rawpy.imread(input_path) as raw:
                    rgb = raw.postprocess()
                    img = Image.fromarray(rgb)
                    img.save(output_path, "JPEG")
                pbar.update(1)  # Update progress bar
                pbar.set_postfix(file=filename)
            except Exception as e:
                print(f"Error converting {filename}: {e}")
                pbar.set_postfix(file=filename, error=str(e))


if __name__ == "__main__":
    input_folder = "input"
    output_folder = "output"

    convert_arw_to_jpeg(input_folder, output_folder)

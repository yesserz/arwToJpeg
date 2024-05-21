import argparse
import logging
import os
import threading
import time
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, ttk, messagebox, IntVar

import rawpy
from PIL import Image
from tqdm import tqdm


class Converter:
    def __init__(self):
        self.stop_conversion = False

    @staticmethod
    def setup_logging():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )

    def convert_arw_to_jpeg(self, input_folder, output_folder, progress_callback=None, status_callback=None):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if not os.path.exists(input_folder):
            raise FileNotFoundError(f"Input folder '{input_folder}' does not exist.")

        arw_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".arw")]
        total_files = len(arw_files)

        if total_files == 0:
            logging.warning(f"No .arw files found in '{input_folder}'")
            return

        start_time = time.time()

        with tqdm(total=total_files, desc="Converting", unit="file", leave=False) as pbar:
            for idx, filename in enumerate(arw_files):
                if self.stop_conversion:
                    break

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
                    if progress_callback:
                        progress_callback(idx + 1, total_files)
                    if status_callback:
                        elapsed_time = time.time() - start_time
                        remaining_time = (elapsed_time / (idx + 1)) * (total_files - (idx + 1))
                        status_callback(idx + 1, total_files, filename, elapsed_time, remaining_time)
                except Exception as e:
                    logging.error(f"Error converting {filename}: {e}")
                    pbar.set_postfix(file=filename, error=str(e))

    def gui(self):
        def select_input_folder():
            folder = filedialog.askdirectory()
            if folder:
                input_folder_var.set(folder)

        def select_output_folder():
            folder = filedialog.askdirectory()
            if folder:
                output_folder_var.set(folder)

        def start_conversion():
            input_folder = input_folder_var.get()
            output_folder = output_folder_var.get()
            if input_folder and output_folder:
                progress_var.set(0)
                progress_bar['maximum'] = 100
                self.stop_conversion = False
                thread = threading.Thread(target=run_conversion, args=(input_folder, output_folder))
                thread.start()
            else:
                logging.error("Both input and output folders must be selected")
                messagebox.showerror("Error", "Both input and output folders must be selected")

        def run_conversion(input_folder, output_folder):
            try:
                self.convert_arw_to_jpeg(input_folder, output_folder, update_progress, update_status)
                if not self.stop_conversion:
                    messagebox.showinfo("Success", "Conversion completed successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def update_progress(current, total):
            progress_percent = int((current / total) * 100)
            progress_var.set(progress_percent)
            progress_label.config(text=f"Progress: {progress_percent}%")

        def update_status(current, total, filename, elapsed_time, remaining_time):
            file_label.config(text=f"Converting file {current}/{total}: {filename}")
            time_label.config(text=f"Elapsed time: {elapsed_time:.2f} seconds")
            remaining_label.config(text=f"Remaining time: {remaining_time:.2f} seconds")

        def on_close():
            self.stop_conversion = True
            root.destroy()

        root = Tk()
        root.title("ARW to JPEG Converter")

        input_folder_var = StringVar()
        output_folder_var = StringVar()
        progress_var = IntVar()

        Label(root, text="Input Folder:").grid(row=0, column=0, padx=10, pady=10)
        input_folder_entry = Entry(root, width=50, textvariable=input_folder_var)
        input_folder_entry.grid(row=0, column=1, padx=10, pady=10)
        Button(root, text="Browse", command=select_input_folder).grid(row=0, column=2, padx=10, pady=10)

        Label(root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10)
        output_folder_entry = Entry(root, width=50, textvariable=output_folder_var)
        output_folder_entry.grid(row=1, column=1, padx=10, pady=10)
        Button(root, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

        Button(root, text="Start Conversion", command=start_conversion).grid(row=2, columnspan=3, pady=20)

        progress_label = Label(root, text="Progress: 0%")
        progress_label.grid(row=3, columnspan=3)

        progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", variable=progress_var)
        progress_bar.grid(row=4, columnspan=3, pady=10)

        file_label = Label(root, text="Converting file: N/A")
        file_label.grid(row=5, columnspan=3)

        time_label = Label(root, text="Elapsed time: 0.00 seconds")
        time_label.grid(row=6, columnspan=3)

        remaining_label = Label(root, text="Remaining time: 0.00 seconds")
        remaining_label.grid(row=7, columnspan=3)

        root.protocol("WM_DELETE_WINDOW", on_close)
        root.mainloop()

    def main(self):
        self.setup_logging()

        parser = argparse.ArgumentParser(description="Convert ARW files to JPEG.")
        parser.add_argument("--input_folder", type=str, help="Path to the input folder containing .arw files")
        parser.add_argument("--output_folder", type=str, help="Path to the output folder for .jpeg files")

        args = parser.parse_args()

        if args.input_folder and args.output_folder:
            self.convert_arw_to_jpeg(args.input_folder, args.output_folder)
        else:
            self.gui()


if __name__ == "__main__":
    converter = Converter()
    converter.main()

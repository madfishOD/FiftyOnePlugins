import fiftyone as fo
import os
import sys

def import_images(dataset_name, folder_path):
    dataset = fo.load_dataset(dataset_name)

    valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif", ".webp"}

    image_paths = [
        os.path.join(root_dir, f)
        for root_dir, _, files in os.walk(folder_path)
        for f in files
        if os.path.splitext(f)[1].lower() in valid_exts
    ]

    if not image_paths:
        print(f"No images found in {folder_path}")
        return

    print(f"Importing {len(image_paths)} images into '{dataset_name}' ...")
    samples = [fo.Sample(filepath=p) for p in image_paths]
    dataset.add_samples(samples)
    dataset.persist()
    print(f"Done! Imported {len(samples)} images into dataset '{dataset_name}'")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python mad_import_worker.py <dataset_name> <folder_path>")
        sys.exit(1)

    dataset_name = sys.argv[1]
    folder_path = sys.argv[2]

    import_images(dataset_name, folder_path)

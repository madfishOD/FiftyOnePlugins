import fiftyone as fo
import os
import sys
import hashlib


def make_sample_id(filepath: str) -> str:
    """Generate a deterministic unique ID for each file."""
    abs_path = os.path.abspath(filepath)
    return hashlib.sha1(abs_path.encode("utf-8")).hexdigest()


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
        input("\nPress Enter to exit...")
        return

    print(f"🔍 Scanning {len(image_paths)} image files...")

    # Build a quick lookup of existing samples by filepath
    existing = {s.filepath: s.id for s in dataset.select_fields("filepath")}

    new_samples = []
    updated = 0

    for path in image_paths:
        sample_id = make_sample_id(path)
        if path in existing:
            # Update existing sample (replace)
            sample = dataset[existing[path]]
            sample.filepath = path  # redundant but explicit
            sample.save()
            updated += 1
        else:
            new_samples.append(fo.Sample(filepath=path, id=sample_id))

    if new_samples:
        print(f"➕ Adding {len(new_samples)} new samples...")
        dataset.add_samples(new_samples)

    if updated:
        print(f"♻️ Updated {updated} existing samples...")

    dataset.save()

    print(
        f"✅ Import complete: {len(new_samples)} added, {updated} updated "
        f"in dataset '{dataset_name}'."
    )

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python mad_import_worker.py <dataset_name> <folder_path>")
        input("\nPress Enter to exit...")
        sys.exit(1)

    dataset_name = sys.argv[1]
    folder_path = sys.argv[2]
    import_images(dataset_name, folder_path)

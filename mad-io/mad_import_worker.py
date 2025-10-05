import fiftyone as fo
import os
import sys
import hashlib


def make_sample_id(filepath: str) -> str:
    """Generate a deterministic unique ID for each file."""
    abs_path = os.path.abspath(filepath)
    return hashlib.sha1(abs_path.encode("utf-8")).hexdigest()


def read_caption_for_image(image_path: str) -> str | None:
    """If a .txt file with same basename exists, return its content."""
    txt_path = os.path.splitext(image_path)[0] + ".txt"
    if os.path.exists(txt_path):
        try:
            with open(txt_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
            return text if text else None
        except Exception as e:
            print(f"⚠️ Could not read caption file for {image_path}: {e}")
    return None


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

    # Lookup of existing samples by filepath
    existing = {s.filepath: s.id for s in dataset.select_fields("filepath")}

    new_samples = []
    updated = 0
    captioned = 0

    for path in image_paths:
        sample_id = make_sample_id(path)
        caption = read_caption_for_image(path)

        if path in existing:
            # Update existing sample
            sample = dataset[existing[path]]
            if caption:
                sample["caption"] = caption
                captioned += 1
            sample.filepath = path  # explicit
            sample.save()
            updated += 1
        else:
            # Create new sample
            sample = fo.Sample(filepath=path, id=sample_id)
            if caption:
                sample["caption"] = caption
                captioned += 1
            new_samples.append(sample)

    if new_samples:
        print(f"➕ Adding {len(new_samples)} new samples...")
        dataset.add_samples(new_samples)

    if updated:
        print(f"♻️ Updated {updated} existing samples...")

    dataset.save()

    print(
        f"✅ Import complete: {len(new_samples)} added, {updated} updated, "
        f"{captioned} with captions in dataset '{dataset_name}'."
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

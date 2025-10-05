import fiftyone as fo
import os
import sys
import shutil
import json


def export_dataset(dataset_name, export_dir, mode, ids_file=None):
    dataset = fo.load_dataset(dataset_name)

    # Determine which samples to export
    if ids_file and os.path.exists(ids_file):
        with open(ids_file, "r") as f:
            sample_ids = json.load(f)
        samples = dataset.select(sample_ids)
        print(f"📦 Exporting {len(samples)} samples ({mode})...")
    else:
        samples = dataset
        print(f"📦 Exporting full dataset ({len(samples)} samples)...")

    os.makedirs(export_dir, exist_ok=True)
    count = 0
    captions = 0

    for sample in samples:
        filename = os.path.basename(sample.filepath)
        dest_path = os.path.join(export_dir, filename)

        try:
            shutil.copy2(sample.filepath, dest_path)
            count += 1
        except Exception as e:
            print(f"⚠️ Failed to copy {filename}: {e}")

        if "caption" in sample and sample["caption"]:
            txt_path = os.path.splitext(dest_path)[0] + ".txt"
            try:
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(str(sample['caption']).strip())
                captions += 1
            except Exception as e:
                print(f"⚠️ Failed to write caption for {filename}: {e}")

    print(f"✅ Export complete: {count} images, {captions} captions")
    input("\nPress Enter to close...")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python mad_export_worker.py <dataset_name> <export_dir> <mode> [ids_file]")
        input("\nPress Enter to exit...")
        sys.exit(1)

    dataset_name, export_dir, mode = sys.argv[1:4]
    ids_file = sys.argv[4] if len(sys.argv) > 4 else None
    export_dataset(dataset_name, export_dir, mode, ids_file)

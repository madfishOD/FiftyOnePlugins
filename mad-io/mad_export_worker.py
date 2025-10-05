import fiftyone as fo
import os
import sys
import shutil
import json


def export_dataset(dataset_name, export_dir, mode, ids_file=None, fields_file=None):
    dataset = fo.load_dataset(dataset_name)

    # Determine samples
    if ids_file and os.path.exists(ids_file):
        with open(ids_file, "r") as f:
            sample_ids = json.load(f)
        samples = dataset.select(sample_ids)
        print(f"📦 Exporting {len(samples)} samples ({mode})...")
    else:
        samples = dataset
        print(f"📦 Exporting full dataset ({len(samples)} samples)...")

    # Determine fields to export
    fields = []
    if fields_file and os.path.exists(fields_file):
        with open(fields_file, "r") as f:
            fields = json.load(f)
    print(f"🧾 Exporting fields: {fields or '[none]'}")

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

        # export each requested field to JSON
        if fields:
            data = {}
            for f in fields:
                if f in sample:
                    data[f] = sample[f]
            if data:
                json_path = os.path.splitext(dest_path)[0] + ".json"
                try:
                    with open(json_path, "w", encoding="utf-8") as jf:
                        json.dump(data, jf, ensure_ascii=False, indent=2, default=str)
                except Exception as e:
                    print(f"⚠️ Failed to write JSON for {filename}: {e}")

        # backward compatibility: captions also go into .txt
        if "caption" in sample and sample["caption"]:
            txt_path = os.path.splitext(dest_path)[0] + ".txt"
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(str(sample["caption"]).strip())
            captions += 1

    print(f"✅ Export complete: {count} images, {captions} captions")
    input("\nPress Enter to close...")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python mad_export_worker.py <dataset_name> <export_dir> <mode> [ids_file] [fields_file]")
        input("\nPress Enter to exit...")
        sys.exit(1)

    dataset_name, export_dir, mode = sys.argv[1:4]
    ids_file = sys.argv[4] if len(sys.argv) > 4 else None
    fields_file = sys.argv[5] if len(sys.argv) > 5 else None
    export_dataset(dataset_name, export_dir, mode, ids_file, fields_file)

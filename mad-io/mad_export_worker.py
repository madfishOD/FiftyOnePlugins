import fiftyone as fo
import os
import sys
import shutil


def export_dataset(dataset_name, export_dir):
    dataset = fo.load_dataset(dataset_name)
    print(f"📦 Exporting dataset '{dataset_name}' to: {export_dir}")

    os.makedirs(export_dir, exist_ok=True)

    count = 0
    captions = 0

    for sample in dataset:
        filename = os.path.basename(sample.filepath)
        dest_path = os.path.join(export_dir, filename)

        # Copy image
        try:
            shutil.copy2(sample.filepath, dest_path)
            count += 1
        except Exception as e:
            print(f"⚠️ Failed to copy {filename}: {e}")

        # Write caption if exists
        caption = sample.get_field("caption")
        if caption:
            txt_path = os.path.splitext(dest_path)[0] + ".txt"
            try:
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(str(caption).strip())
                captions += 1
            except Exception as e:
                print(f"⚠️ Failed to write caption for {filename}: {e}")

    print(f"✅ Export complete: {count} images, {captions} captions")
    input("\nPress Enter to close...")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python mad_export_worker.py <dataset_name> <export_dir>")
        input("\nPress Enter to exit...")
        sys.exit(1)

    dataset_name = sys.argv[1]
    export_dir = sys.argv[2]
    export_dataset(dataset_name, export_dir)

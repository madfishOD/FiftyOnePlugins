import fiftyone as fo
import fiftyone.operators as foo
import fiftyone.operators.types as types
from tkinter import filedialog, Tk
import os


class MadImportSamples(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="mad_io",
            label="Import Samples",
            dynamic=False,
        )

    def execute(self, ctx):
        # Select folder
        try:
            root = Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            folder_path = filedialog.askdirectory(title="Select a folder with images")
            root.destroy()
        except Exception as e:
            raise foo.OperatorError(f"Error opening dialog: {e}")

        if not folder_path:
            return {"error": "No folder selected"}

        # Gather image files recursively
        valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif", ".webp"}
        image_paths = [
            os.path.join(root_dir, f)
            for root_dir, _, files in os.walk(folder_path)
            for f in files
            if os.path.splitext(f)[1].lower() in valid_exts
        ]

        if not image_paths:
            return {"error": "No image files found in the selected folder"}

        # Get dataset from context or create new one
        dataset = ctx.dataset
        if dataset is None:
            return {"error": "No active dataset found!"}

        # Add samples
        samples = [fo.Sample(filepath=path) for path in image_paths]
        dataset.add_samples(samples)
        dataset.persist()

        # If there is a session, reload it
        if ctx.session:
            ctx.session.dataset = dataset
            ctx.session.refresh()

        return {
            "selected_path": folder_path,
            "imported_count": len(samples),
            "dataset_name": dataset.name,
        }

    def resolve_output(self, ctx):
        outputs = types.Object()
        outputs.str("selected_path", label="Selected Folder Path")
        outputs.int("imported_count", label="Number of Images Imported")
        outputs.str("dataset_name", label="Dataset Name")
        return types.Property(outputs, view=types.View(label="Import Complete!"))


def register(p):
    p.register(MadImportSamples)
import fiftyone.operators as foo
import fiftyone.operators.types as types
from tkinter import filedialog, Tk
import subprocess
import sys
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
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        folder_path = filedialog.askdirectory(title="Select folder with images")
        root.destroy()

        if not folder_path:
            raise foo.OperatorError("No folder selected")

        dataset = ctx.dataset
        if dataset is None:
            raise foo.OperatorError("Please open or select a dataset first")

        # Path to helper script in your plugin folder
        script_path = os.path.join(os.path.dirname(__file__), "mad_import_worker.py")

        # Launch background worker process
        subprocess.Popen(
            [sys.executable, script_path, dataset.name, folder_path],
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0,
        )

        return {
            "selected_path": folder_path,
            "status": f"Import started in separate process for dataset '{dataset.name}'"
        }

    def resolve_output(self, ctx):
        outputs = types.Object()
        outputs.str("selected_path", label="Selected Folder Path")
        outputs.str("status", label="Status")
        return types.Property(outputs, view=types.View(label="Import started"))


def register(p):
    p.register(MadImportSamples)

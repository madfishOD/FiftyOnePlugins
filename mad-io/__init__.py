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
            name="mad_io_import",
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
    
class MadExportSamples(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="mad_io_export",
            label="Export Samples",
            dynamic=False,
        )
    
    def execute(self, ctx):
        """Called when the user runs the operator."""
        dataset_name = ctx.dataset.name if ctx.dataset else None
        if not dataset_name:
            return {"error": "No dataset selected"}

        # Let user pick export folder
        root = Tk()
        root.withdraw()
        export_dir = filedialog.askdirectory(title="Select Export Directory")
        root.destroy()

        if not export_dir:
            return {"error": "Export cancelled"}

        # Launch the export in a separate worker process
        script_path = os.path.join(
            os.path.dirname(__file__), "mad_export_worker.py"
        )

        subprocess.Popen(
            [
                sys.executable,
                script_path,
                dataset_name,
                export_dir,
            ],
            creationflags=subprocess.CREATE_NEW_CONSOLE
            if os.name == "nt"
            else 0,
        )

        return {"export_dir": export_dir}

    def resolve_output(self, ctx):
        outputs = types.Object()
        outputs.str("export_dir", label="Export Directory")
        header = "Mad Export Status"
        return types.Property(outputs, view=types.View(label=header))



def register(p):
    p.register(MadImportSamples)
    p.register(MadExportSamples)

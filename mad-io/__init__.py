import fiftyone.operators as foo
import fiftyone.operators.types as types
from tkinter import filedialog, Tk
import subprocess
import sys
import os
import json


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
            dynamic=True,  # now interactive
        )

    def resolve_input(self, ctx):
        inputs = types.Object()

        # --- Export scope ---
        export_mode = types.RadioGroup()
        export_mode.add_choice("DATASET", label="Full dataset")
        export_mode.add_choice("VIEW", label="Active view")
        export_mode.add_choice("SELECTION", label="Selected samples")

        inputs.enum(
            "mode",
            export_mode.values(),
            required=True,
            default="VIEW",
            view=export_mode,
        )

        # --- Field selection ---
        field_names = list(ctx.dataset.get_field_schema().keys())
        # exclude technical fields
        field_names = [f for f in field_names if f not in ("id", "filepath", "metadata")]

        inputs.list(
            "fields",
            types.String(),
            required=False,
            default=["caption"] if "caption" in field_names else [],
            view=types.View(
                label="Select fields to export",
                description="Choose which sample fields to export alongside images",
                values=field_names,
                multiple=True,
            ),
        )

        return types.Property(inputs, view=types.View(label="Export Options"))

    def execute(self, ctx):
        mode = ctx.params.get("mode", "VIEW")
        fields = ctx.params.get("fields", [])

        dataset = ctx.dataset
        if dataset is None:
            raise foo.OperatorError("Please open or select a dataset first")

        root = Tk()
        root.withdraw()
        export_dir = filedialog.askdirectory(title="Select export directory")
        root.destroy()

        if not export_dir:
            return {"error": "Export cancelled"}

        script_path = os.path.join(os.path.dirname(__file__), "mad_export_worker.py")

        sample_ids = []
        if mode == "SELECTION" and ctx.selected:
            sample_ids = ctx.selected
        elif mode == "VIEW":
            sample_ids = ctx.view.values("id")

        tmp_ids_path = os.path.join(export_dir, "_export_ids.json")
        with open(tmp_ids_path, "w") as f:
            json.dump(sample_ids, f)

        tmp_fields_path = os.path.join(export_dir, "_export_fields.json")
        with open(tmp_fields_path, "w") as f:
            json.dump(fields, f)

        subprocess.Popen(
            [sys.executable, script_path, dataset.name, export_dir, mode, tmp_ids_path, tmp_fields_path],
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0,
        )

        return {"export_dir": export_dir, "mode": mode, "fields": fields}

    def resolve_output(self, ctx):
        outputs = types.Object()
        outputs.str("export_dir", label="Export Directory")
        outputs.str("mode", label="Export Mode")
        return types.Property(outputs, view=types.View(label="Export Status"))



def register(p):
    p.register(MadImportSamples)
    p.register(MadExportSamples)

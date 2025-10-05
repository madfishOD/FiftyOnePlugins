import fiftyone.operators as foo
import fiftyone.operators.types as types
from tkinter import filedialog, Tk
import platform


class MadImportSamples(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="mad_io",
            label="Import Samples",
            dynamic=False,  # no dynamic UI since we skip inputs
        )

    # No resolve_input — the operator runs immediately

    def execute(self, ctx):
        folder_path = None

        if platform.system() == "Windows":
            try:
                root = Tk()
                root.withdraw()                 # hide main Tk window
                root.attributes("-topmost", True)  # bring dialog to front
                folder_path = filedialog.askdirectory(
                    title="Select a folder to import"
                )
                root.destroy()
            except Exception as e:
                folder_path = f"[Error: {e}]"
        else:
            folder_path = "[Folder selection supported only on Windows for now]"

        if not folder_path:
            folder_path = "[No folder selected]"

        # Return the selected folder as the output
        return {"selected_path": folder_path}

    def resolve_output(self, ctx):
        outputs = types.Object()
        outputs.str(
            "selected_path",
            label="Selected Folder Path",
            description="The folder you picked via the native file dialog",
        )
        header = "Folder Selection Result"
        return types.Property(outputs, view=types.View(label=header))


def register(p):
    p.register(MadImportSamples)

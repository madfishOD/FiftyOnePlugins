# panel.py
import fiftyone.operators.types as types
import fiftyone.plugins as fop


class HelloPanel(fop.Panel):
    @property
    def config(self):
        # Fully qualified panel name that matches plugin.yaml
        return fop.PanelConfig(
            name="@madfish/hello_python.HelloPanel",
            label="Hello Panel (Python)",
        )

    def render(self, ctx):
        # Request a handle to our operator (namespaced)
        op = ctx.request_op("@madfish/hello_python/print_me")

        # Simple UI: a label and a button that runs the operator
        return types.View(
            layout=types.Layout(
                elements=[
                    types.Label(label="Hello World!"),
                    types.Button(label="Click Me", on_click=op),
                ]
            )
        )

# __init__.py
from .operators import PrintMe
from .panel import HelloPanel

import fiftyone.operators as foo
import fiftyone.operators.types as types

class HelloPanel(foo.Panel):
    @property
    def config(self):
        return foo.PanelConfig(
            name="@madfish/hello_python.HelloPanel",
            label="Hello Panel (Python)",
            icon="smile",            # optional icon
            allow_multiple=False,    # only one instance
        )

    def on_load(self, ctx):
        # optional: initialize panel state
        ctx.panel.set_state("message", "Hello World!")

    def render(self, ctx):
        # retrieve current state
        message = ctx.panel.state.get("message", "Hello World!")

        # operator trigger
        op = ctx.request_op("@madfish/hello_python/print_me")

        # build UI
        obj = types.Object()
        obj.str("label", label=message)
        obj.button(
            "click_me",
            label="Click Me!",
            on_click=op,
        )

        # return as a Property (important!)
        return types.Property(obj, view=types.View(label="Hello Panel"))

def register(plugin):
    plugin.register(PrintMe)
    plugin.register(HelloPanel)

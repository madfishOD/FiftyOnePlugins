import fiftyone.operators as foo
import fiftyone.operators.types as types
import fiftyone.plugins as fop


class HelloPanel(fop.Panel):
    @property
    def config(self):
        return fop.PanelConfig(
            name="hello_plugin.HelloPanel",
            label="Hello Panel",
        )

    def render(self, ctx):
        op = ctx.request_op("hello_plugin.print_me")
        return types.View(
            layout=types.Layout(
                elements=[
                    types.Label(label="Hello World!"),
                    types.Button(label="Click Me", on_click=op)
                ]
            )
        )


def register(plugin):
    plugin.register(HelloPanel)

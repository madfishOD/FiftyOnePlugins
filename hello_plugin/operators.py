import fiftyone.operators as foo

class PrintMe(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="hello_plugin.print_me",
            label="Say That's Me!"
        )

    def execute(self, ctx):
        return {"message": "That's Me!"}


def register(plugin):
    plugin.register(PrintMe)

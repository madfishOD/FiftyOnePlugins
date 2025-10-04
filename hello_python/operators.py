# operators.py
import fiftyone.operators as foo
import fiftyone.operators.types as types


class PrintMe(foo.Operator):
    @property
    def config(self):
        # Important: use the namespaced operator name that matches plugin.yaml
        return foo.OperatorConfig(
            name="@madfish/hello_python/print_me",
            label="Say That's Me!",
            dynamic=False,  # simple operator, no input form
        )

    def execute(self, ctx):
        # Business logic — return values will be shown in an output modal
        return {"message": "That's Me!"}

    def resolve_output(self, ctx):
        # Define how to display the returned values in the UI
        outputs = types.Object()
        outputs.str("message", label="Response")
        return types.Property(outputs, view=types.View(label="Hello Python Operator"))

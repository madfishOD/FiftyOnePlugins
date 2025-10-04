# operators.py
import fiftyone.operators as foo
import fiftyone.operators.types as types


class PrintMe(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="@madfish/hello_python/print_me",
            label="Say That's Me!"
        )

    def execute(self, ctx):
        print("That's Me!")
        return {"message": "That's Me!"}

    def resolve_output(self, ctx):
        outputs = types.Object()
        outputs.str("message", label="Response")
        return types.Property(outputs, view=types.View(label="Hello Python Operator"))

# __init__.py
from .operators import PrintMe
from .panel import HelloPanel


def register(plugin):
    plugin.register(PrintMe)
    plugin.register(HelloPanel)

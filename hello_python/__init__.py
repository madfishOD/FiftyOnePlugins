# __init__.py
from .operators import PrintMe
from .panel import HelloPanel

def register(plugin):
    """Registers the plugins in this module."""
    plugin.register(PrintMe)
    plugin.register(HelloPanel)

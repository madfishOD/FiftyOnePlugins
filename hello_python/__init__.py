# __init__.py
from .operators import PrintMe

def register(plugin):
    """Registers backend operators."""
    plugin.register(PrintMe)

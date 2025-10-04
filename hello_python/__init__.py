# __init__.py
from .operators import PrintMe

def register(plugin):
    """Registers backend components."""
    plugin.register(PrintMe)

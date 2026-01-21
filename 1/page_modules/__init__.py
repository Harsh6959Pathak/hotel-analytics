"""
Pages package for Dubai Hotel Analytics Dashboard
Properly exports all page modules
"""

# Import existing page modules
from . import overview
from . import price_demand
from . import geographical

# The remaining_pages module contains the render functions
# These are imported in app.py directly as:
# from pages.remaining_pages import render_room_amenities_page, etc.

__all__ = [
    'overview',
    'price_demand',
    'geographical'
]
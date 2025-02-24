# -*- coding: utf-8 -*-

"""Register assets for optimizations.

   We optimize and merge assets into bundles, in order to reduce the client's connections
   from number of assets down to number of bundles.

   Register static files for those asset bundles here.

   We support the two most common and mature filters only:
        - rjsmin (for .js files)
        - rcssmin (for .css files)

   .. note::
      Paths are relative to the static directory.

   .. warning::
      * Synchronize this listing with static directory changes.
      * License get's stripped too, provide external file.
"""
# parts of flask_assets are somehow deprecated, fix later, for now there is no rcssmin checking
from flask_assets import Bundle, register_filter
from webassets.loaders import PythonLoader as PythonAssetsLoader

from src.util.RCSSMin import RCSSMin

register_filter(RCSSMin)

# Javascript bundles:
all_css = Bundle('css/semantic.min.css',
                filters='rcssmin', output='css/packed-all.css')

# Javascript bundles:
all_js = Bundle('js/semantic.min.js',
                filters='rjsmin', output='js/packed-all.js')


# Hide concrete loading method inside this module
def get_bundles():
    """Returns all registered bundles.

       . note:: Returns only bundles from the assets module, you shouldn't register them anywhere else
    """
    loader = PythonAssetsLoader(__name__)

    return loader.load_bundles()


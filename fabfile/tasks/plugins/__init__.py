import importlib
import pkgutil

plugins = [modname for importer, modname, ispkg in pkgutil.iter_modules(__path__)]


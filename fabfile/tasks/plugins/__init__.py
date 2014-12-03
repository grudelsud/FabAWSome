import pkgutil
import inspect

plugins = []
tasks = {}

_modules = pkgutil.iter_modules(__path__)


def _get_public_variables(obj):
    return [(name, value) for name, value 
            in inspect.getmembers(obj, lambda x: not callable(x))
            if not name.startswith('_')]


for loader, module_name, ispkg in _modules:
	plugins.append(module_name)
	module = __import__(module_name, locals(), [], -1)
	for cls_name, cls in inspect.getmembers(module, inspect.isclass):
		if cls_name == 'Tasks':
			tasks[module_name] = dict(_get_public_variables(cls))
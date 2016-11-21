
import os
import sys

try:
    import efesto_logger as logging
except:
    import logging

logger = logging.getLogger(__name__)


def discover_ifaces():
    '''Scans ``sys.path`` to retrieve any module starting with ``ctx_``. All
    modules found, will be stripped from the prefix and returned.

    :returns: All modules starting with ``ctx_``
    :rtype: list of str
    '''
    interfaces = []

    for path in sys.path:
        if not os.path.isdir(path):
            continue
        for module in os.listdir(path):
            if 'egg' in module or 'dist' in module:
                module = module.split('-')[0]
            module = module.split('.')[0]
            if module.startswith('ctx_'):
                module = module[4:]
                interfaces.append(module)

    logger.debug('Interfaces found %s' % interfaces)
    return interfaces


def import_module(module):
    '''Imports a module and returns it. If not found, ``None`` is returned.

    :param module: Name of the module to be imported.
    :type module: str

    :returns: A module
    :rtype: module or :py:class:`None`
    '''
    try:
        return __import__(module)
    except Exception as e:
        logger.warning('Could not import %s: %s' % (module, e))


def get_interface(name):
    '''Retrieves an interface. The interface has to be a module, it's name
    has to start with ``ctx_``, it has to be in the ``PYTHONPATH`` and it must
    contain a ``IFACE`` global variable which has to contain an uninitialized
    interface class. Raises :class:`ValueError` if not found.

    :param name: Name of the interface module to search.
    :type name: str

    :returns: Interface
    :rtype: :class:`efesto_mcontextpicker.context.ContextInterface` base class
    '''
    interfaces = discover_ifaces()
    if name not in interfaces:
        raise ValueError(
            'Interface ctx_%s could not be found in PYTHONPATH' % name
        )
    return import_module('ctx_%s' % name).IFACE

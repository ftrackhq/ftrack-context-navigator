Developing
==========


What's an interface?
--------------------

An interface is the middle man between your project structure and our plugin. The interface in this case is what will tell the software that the children of project ``Foo`` are shots ``001`` and ``002``. The interface will allow the software to be able to recognize a proper project hierarchy whether you work with ``Ftrack``, ``Shotgun``, a simple folder structure or your own management system.


How do I create a new interface?
--------------------------------


There are 3 requirements for any module to be considered a valid interface:

1. It's a python module and it's in the ``PYTHONPATH``.
2. It's name starts witn ``ctx_``. Example: ``ctx_ftrack.py``.
3. Within the module, a global variable called ``IFACE`` has been provided, pointing to the class that will be acting as the interface.

This is a very simple example of a valid interface (located at ``resources/interfaces/ctx_filesystem.py``):

.. literalinclude:: ../../resources/interfaces/ctx_filesystem.py

More information can be found at :class:`efesto_mcontextpicker.context.ContextInterface`.


How do I choose what interface to use?
--------------------------------------

This will be the most basic example of interface usage:

.. code-block:: python

    import efesto_mcontextpicker.mayactxpicker
    efesto_mcontextpicker.mayactxpicker.main()

:func:`efesto_mcontextpicker.main` has two arguments: ``main_context`` and ``iface_name``.

``iface_name`` is the name of the interface to be used. If you have created a new interface called ``ctx_shotgun.py``, ``shotgun`` should be the specified in this argument. If ``iface_name`` is not set, it will default to ``filesystem``, which means that ``ctx_filesystem.py`` will be loaded. Also, if not specified ``iface_name``, it is possible to use ``EFESTO_CONTEXT_IFACE`` environment variable to drive the interface name.

``main_context`` is the name of the starting context which the specified interface will process. If this argument is not filled, the interface will call ``get_root_context()`` to find out.

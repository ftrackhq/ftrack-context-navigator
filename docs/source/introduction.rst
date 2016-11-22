Introduction
============


What's all this about?
-----------------------


This tool aims to ease the workflow in productions where artists have to be switching from one shot/sequence/asset/task to another frequently. The main idea of this software is to be able to change context at any time in a easy and fast way, thus avoiding unnecessary and repetitive actions.

This tool attaches itself to Maya's toolbox or to a Nuke panel and provides a custom context browser as well as bookmarks for previous selected contexts.

When initialized, the tools looks like this in Maya and Nuke:

.. image:: _static/tool.png
   :align: center


Installation
------------

It is recommended to build the software first, and manually add it to ``PYTHONPATH``,
because Maya or Nuke will not add the system python path's to itself.

.. code-block:: bash

    $ python setup.py build

After this, at least one interface must be added, thus ``resources/interfaces`` should be added to ``PYTHONPATH`` as well.

If you want Maya to start with this tool, add ``resources/maya`` to both ``PYTHONPATH`` and ``MAYA_SCRIPT_PATH``.
For Nuke, NUKE_PATH should be set to ``resources/nuke``.

.. note::

    If no arguments specified when initializing the software, ``FileSystem`` interface will be picked up, and the current working directory will be the starting point, in Windows, most likely Maya's installation path. It is recommended to specify a starting point.


How do I use this?
------------------

The first button, which as the `EfestoLab <http://www.efestolab.uk/>`_ logo will server as a bookmark manager, left cliking on it, will spawn the list of bookmarks available.

The rest of the bottom buttons will be the current context. Right cliking on them will spawn a menu with their children. Clicking on any item of this menu will generate a new button, and the current context will be set. If the button has no children, it will be considered a leaf thus will be added to the bookmarks list.

.. tip::

    The names are shortened for because of the narrow space. The full names can be seen in the buttons if hovered for a bit of time.


How do I add the tool to Nuke's UI?
-----------------------------------

Right click on Nuke's side bar. Choose Split Vertical.

.. image:: _static/nuke_tool1.png
   :align: center

Right click on the new panel. Choose Windows -> Custom -> Context Picker.

.. image:: _static/nuke_tool2.png
   :align: center

The new panel can be saved as part of a workspace using Nuke's Workspace menu.


How do I decide what's the current project in Maya?
---------------------------------------------------

When calling the script trough :func:`efesto_mcontextpicker.mayactxpicker.main`, you can specify a main context, which by default will be the current working directory. By default, the script will initialize the ``FileSystem`` interface, which will basically be a folder explorer, stopping at any folder which contains a ``workspace.mel`` and setting the project to that folder if it's found.


How can I delete the saved preferences?
---------------------------------------

Preferences are handled by `QSettings <http://doc.qt.io/qt-4.8/qsettings.html>`_, in the documentation should be everything you need.


This script hides the Maya website button, why?
-----------------------------------------------

It's a pointless button, get over it.

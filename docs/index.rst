.. python-kyototycoon-binary documentation master file, created by
   sphinx-quickstart on Sat Oct 19 00:56:50 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to python-kyototycoon-binary's documentation!
=====================================================

A lightweight Python client for accessing `Kyoto Tycoon <http://fallabs.com/kyototycoon/>`_ via its binary protocol.

Installation
------------

.. code-block:: bash

    $ pip install Cython
    $ pip install python-kyototycoon-binary

Basic Usage
-----------

.. code-block:: python

    >>> from bkyototycoon import KyotoTycoonConnection
    >>> client = KyotoTycoonConnection()
    >>> client.set_bulk({'key1': 'value1', 'key2': 'value2'})
    2
    >>> client.get_bulk(['key1', 'key2', 'key3'])
    {'key2': 'value2', 'key1': 'value1'}
    >>> client.remove_bulk(['key1', 'key2'])
    1
    >>> client.get_bulk(['key1', 'key2', 'key3'])
    {'key1': 'value1'}

Contents:

.. toctree::
   :maxdepth: 2

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


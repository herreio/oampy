=====
oampy
=====

*Under Development*

``oampy`` is a Python package and command line tool that allows to access data
from the Open Access Monitor (OAM), which is run by Forschungszentrum Jülich.

Installation
============

... via SSH
~~~~~~~~~~~

.. code-block:: bash

   pip install -e git+ssh://git@github.com/herreio/oampy.git#egg=oampy

... or via HTTPS
~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -e git+https://github.com/herreio/oampy.git#egg=oampy

Usage Examples
==============

Command Line
~~~~~~~~~~~~

.. code-block:: shell

    # fetch metadata of journal given by ISSN
    oampy journal "0360-4012"
    # fetch metadata of publication given by DOI
    oampy publication "10.1007/s11263-011-0505-4"

Interpreter
~~~~~~~~~~~

.. code-block:: python

    import oampy
    # fetch metadata of journal
    journal = oampy.get_journal("0360-4012")
    # fetch metadata of publication
    publication = oampy.get_publication("10.1007/s11263-011-0505-4")

Usage Terms
===========

Open Access Monitor
~~~~~~~~~~~~~~~~~~~

    The database of the Open Access Monitor Germany is published under the Open Database License 1.0.

    The data can be reused under the following conditions:

    - Reuse of larger amounts of data and use of the API: please contact us.
    - Reuse of the data by download via the OAM application: CC BY 4.0

    https://open-access-monitor.de

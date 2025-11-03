.. Gemini Query documentation master file

Gemini Query Documentation
===========================

**Gemini Query** is an advanced command-line interface for Google Gemini AI that enables sending queries directly from the command line with intelligent browser automation, robust error handling, and comprehensive troubleshooting tools.

.. image:: https://img.shields.io/badge/version-2.0.0-blue.svg
   :target: https://github.com/gemini-query/gemini-query
   :alt: Version

.. image:: https://img.shields.io/badge/python-3.12+-green.svg
   :target: https://python.org
   :alt: Python Version

.. image:: https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg
   :target: https://github.com/gemini-query/gemini-query
   :alt: Platform Support

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   # Install uv
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Clone repository
   git clone https://github.com/gemini-query/gemini-query.git
   cd gemini-query

   # Install dependencies
   uv sync

   # Run
   uv run gemini-query "Hello, Gemini!"

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

   # Direct question
   gemini-query "What is Python?"

   # Piped input
   cat file.txt | gemini-query "Summarize this"

   # Code review
   git diff | gemini-query "Review these changes"

Features
--------

Core Functionality
~~~~~~~~~~~~~~~~~~

* **Multi-Method Data Transfer**: HTTP server, localStorage, URL parameters, and manual input fallbacks
* **Intelligent Browser Automation**: Advanced Greasemonkey script with multiple UI detection methods
* **Cross-Platform Support**: Works on Windows, macOS, and Linux
* **Flexible Input Methods**: Direct arguments, piped input, file input, and interactive prompts
* **Robust Error Handling**: Comprehensive fallback mechanisms and user-friendly error messages

Architecture
~~~~~~~~~~~~

* **Polylith Architecture**: Modular, testable, and maintainable component-based design
* **Dependency Injection**: Loose coupling with container-based dependency management
* **Type Safety**: Full type hints and static type checking with MyPy
* **Structured Logging**: Advanced logging with structlog
* **Modern Python**: Python 3.12+ with latest best practices

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   usage
   troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide

   architecture
   development
   api/index

.. toctree::
   :maxdepth: 1
   :caption: Project Information

   changelog
   contributing
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

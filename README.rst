collective.assets - Webassets for Plone
=======================================

travisbuildstatus_

.. contents::

Why webassets?
--------------

Webassets are a standardized way of proving web resources. They can be easily
dispatched through commen webservers and support minification, filter-plugins
 (like LESS, CoffeeScript, etc.) and YAML based configuration.
Collective.assets provides the glue betweeen the webassets_-library and
plone.resource. Plone.resource was choosen (instead of just dumping the
resources to the filesystem) because then it is possible to access the files
via ZServer too, which is handy for development where don't have an external
webserver running.

Usage
-----

To use *collective.assets* add it to the buildout and activate it as an addon
in the Plone control panel. This will give you another entry in the control
panel: **Assets Settings**
There you can activate the use of the webassets, change configuration and
get an overview of the asset. You will also find a button there to generate
the assets.

What versions are supported?
----------------------------

Collective.assets depend on plone.resource and should work with any recent
Plone 4. It was developed and tested with Plone 4.2 and 4.3 (trunk). For
the assets version 0.7.1 of the webassets-library was used.

Known issues
------------

- Currently only one Plone per ZODB is supported
- The sarissa.js version shipped with Plone can not be minified with jsmin.
  One workaround is to disable sarissa.js in portal_javascript another is
  to change the compression-level from *safe* to *none*.
- The product does not support all features of the resource registry
  (some of them out of intention eg. inline resources, conditial comments)

.. _webassets: http://pypi.python.org/pypi/webassets
.. _travisbuildstatus: https://travis-ci.org/tomgross/collective.assets.png

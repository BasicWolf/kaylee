.. _contrib:

Contrib
=======

.. module:: kaylee

Kaylee comes with a small ``contrib`` package which currently plays a role
of :py:class:`Controller`, :py:class:`TemporalStorage` and
:py:class:`PermanentStorage` implementation examples.

Contrib also contains Flask and Django applications which support Kaylee :ref:`default-communication`.

.. _contrib_front_ends:

Front-ends
----------

The full example of using ``kaylee.contrib.frontends`` is available in
:ref:`demo` application.

Flask
.....

Kaylee provides Flask ``blueprint`` which can be used in the following
fashion::

  from flask import Flask
  from kaylee.contrib.frontends.flask_frontend import kaylee_blueprint

  app = Flask(__name__)

  app.register_blueprint(kaylee_blueprint,
                         url_prefix = '/kaylee')


Django
......

Kaylee provides Django ``application`` which can be used in the following
fashion:

.. code-block:: python

  # Project's urls.py

  from django.conf.urls import patterns, include, url

  urlpatterns = patterns('',
      ...,
      url(r'^kaylee/', include('kaylee.contrib.frontends.django_frontend.urls'))
  )



Controllers
-----------

.. module:: kaylee.contrib

.. autoclass:: SimpleController

.. autoclass:: ResultsComparatorController


Storages
--------

.. autoclass:: MemoryTemporalStorage

.. autoclass:: MemoryPermanentStorage
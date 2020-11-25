==========================
eea.progress.workflow
==========================
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.progress.workflow/develop
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.progress.workflow/job/develop/display/redirect
  :alt: Develop
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.progress.workflow/master
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.progress.workflow/job/master/display/redirect
  :alt: Master

A Plone add-on that expose workflow progress via RestAPI

.. contents::


Main features
=============

1. RestAPI workflow progress::

    $ curl -H 'Accept: application/json' --user admin:admin -i http://localhost:8080/Plone/a-page/@workflow.progress

    or

    $ curl -H 'Accept: application/json' --user admin:admin -i http://localhost:8080/Plone/a-page?expand=workflow.progress


Install
=======

* Add eea.progress.workflow to your eggs section in your buildout and
  re-run buildout::

    [buildout]
    eggs +=
      eea.progress.workflow

* You can download a sample buildout from:

  - https://github.com/eea/eea.progress.workflow/tree/master/buildouts/plone4
  - https://github.com/eea/eea.progress.workflow/tree/master/buildouts/plone5

* Or via docker::

    $ docker run --rm -p 8080:8080 -e ADDONS="eea.progress.workflow" plone

* Install *eea.progress.workflow* within Site Setup > Add-ons


Buildout installation
=====================

- `Plone 4+ <https://github.com/eea/eea.progress.workflow/tree/master/buildouts/plone4>`_
- `Plone 5+ <https://github.com/eea/eea.progress.workflow/tree/master/buildouts/plone5>`_


Source code
===========

- `Plone 4+ on github <https://github.com/eea/eea.progress.workflow>`_
- `Plone 5+ on github <https://github.com/eea/eea.progress.workflow>`_


Eggs repository
===============

- https://pypi.python.org/pypi/eea.progress.workflow
- http://eggrepo.eea.europa.eu/simple


Plone versions
==============
It has been developed and tested for Plone 4 and 5. See buildouts section above.


How to contribute
=================
See the `contribution guidelines (CONTRIBUTING.md) <https://github.com/eea/eea.progress.workflow/blob/master/CONTRIBUTING.md>`_.

Copyright and license
=====================

eea.progress.workflow (the Original Code) is free software; you can
redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc., 59
Temple Place, Suite 330, Boston, MA 02111-1307 USA.

The Initial Owner of the Original Code is European Environment Agency (EEA).
Portions created by Eau de Web are Copyright (C) 2009 by
European Environment Agency. All Rights Reserved.


Funding
=======

EEA_ - European Environment Agency (EU)

.. _EEA: https://www.eea.europa.eu/
.. _`EEA Web Systems Training`: http://www.youtube.com/user/eeacms/videos?view=1

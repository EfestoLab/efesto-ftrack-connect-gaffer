Efesto-Ftrack-Connect-Gaffer
============================

Test project to evaluate the connection between gaffer and ftrack.

.. code-block:: bash

    # setup base paths

    # NOTE : GAFFER_INSTALL_PATH is used for the hook as well, to get where gaffer installation lives

    export GAFFER_INSTALL_PATH=/home/efesto/devel/efesto/docker-gafferDependencies/volume/gaffer-0.15.0.0/

    export EFESTO_FTRACK_CONNECT_GAFFER_PAth=/home/efesto/devel/efesto/efesto-ftrack-connect-gaffer

    export FTRACK_API_PATH=/home/efesto/devel/ftrack/python-api

    export FTRACK_CONNECT_PATH=/home/efesto/devel/ftrack/connector/ftrack-connect/build/lib.linux-x86_64-2.7

    # PYTHONPATH

    export PYTHONPATH=${PYTHONPATH}:${FTRACK_API_PATH}

    export PYTHONPATH=${PYTHONPATH}:${FTRACK_CONNECT_PATH}

    export PYTHONPATH=${PYTHONPATH}:${EFESTO_FTRACK_CONNECT_PATH_GAFFER}/source/python

    # Gaffer related ENVS

    export GAFFER_STARTUP_PATHS=${GAFFER_STARTUP_PATHS}:${EFESTO_FTRACK_CONNECT_GAFFER_PAth}/source/startup

    # Ftrack web hook

    export FTRACK_EVENT_PLUGIN_PATH=${FTRACK_EVENT_PLUGIN_PATH}:${EFESTO_FTRACK_CONNECT_GAFFER_PAth}/resource/hook


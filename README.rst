======================
SAILON Tinker Launcher
======================

Protocols for using new Tinker or Hydra with current SAIL-ON implementation


* Free software: Apache Software License 2.0
* Documentation: Compile Seperately... still in progress



Install
--------
This requires installing sail-on-client, hydra, and tinker.  If you are launching with either
hydra or tinker but not both, you only need to install one of them.

Sail-on-client install instructions here: https://gitlab.kitware.com/darpa-sail-on/sail-on-client
- Current branch: better_logging

Tinker install instructions here: https://github.com/tinker-engine/tinker-engine
- Current Branch: configuration-handling

Hydra install

`pip install hydra-core hydra_colorlog --upgrade`

For all installs, please run

.. code-block:: bash

   pip install -r requirements.txt
   pip install -e .


Ti install everything:

.. codeblock:: bash

  conda create -n sailon python=3.7 && conda activate sailon
  conda install -y numpy scipy pytorch  torchvision torchaudio cudatoolkit=10.2 -c pytorch
  python super_setup.py ensure
  python super_setup.py develop
  (cd ../evm_based_novelty_detector/timm/ && pip install -e .)

To Run
--------
From the home directory:
Tinker run command:

.. code-block:: bash

  tinker -c sailon_tinker_launcher/config.yaml sailon_tinker_launcher/tinker_launcher.py

To change to a different config, copy the file `sailon_tinker_launcher/config.yaml`
and make your changes there.  You can update the -c parameter to load you new configuration.

Ask Roni about multirun capabilities.


Hydra Run Command:

.. code-block:: bash

  python sailon_tinker_launcher/hydra_launcher.py

You can either pass the new config items by overwritting them, such as

.. code-block:: bash

  python sailon_tinker_launcher/hydra_launcher.py use_feedback=False

You can do multirun as well (look up hydra documentation: https://hydra.cc/docs/next/intro#multirun
Or you can also create a new config (copying from `sailon_tinker_launcher/config.yaml`) and reference

.. code-block:: bash

  python sailon_tinker_launcher/hydra_launcher.py --config-path <path to new config>

Note: the path to the new config is relative to the same folder as hydra_launcher.py

Configuration
-------------
The default configuration for this is shown in sailon-tinker-launcher/config.yaml.  The launching
parameters that are the minimum necessary are as follows:
- protocol: either 'ond' or 'condda' to define which protocol to run
- harness:  either 'local' or 'par' to define which harness to use
- workdir: a directory to save all the information from the run including
    - Config
    - Output of algorithm




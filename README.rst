======================
SAILON Tinker Launcher
======================

Protocols for using new Tinker or Hydra with current SAIL-ON implementation


* Free software: Apache Software License 2.0
* Documentation: Compile Seperately... still in progress

Month 18 Evaluation Instructions
--------------------------------

1. `Document Transcription <dt_m18.md>`_

.. warning::
    The documentation underneath this section is out of date please ignore it.

Step 1: Install
--------
This requires installing sail-on-client, hydra, and tinker.  If you are launching with either
hydra or tinker but not both, you only need to install one of them.


For all installs, please run

.. code-block:: bash

   pip install -r requirements.txt
   pip install -e .


This install everything:

.. code-block:: bash

   conda create -n sailon python=3.7 && conda activate sailon
   conda install -y numpy scipy pytorch  torchvision torchaudio cudatoolkit=10.2 -c pytorch
   python super_setup.py develop
   (cd ../evm_based_novelty_detector/timm/ && pip install -e .)

Note, this assumes you have ssh key from your computer to https://kwgitlab.kitware.com/ and https://gitlab.kitware.com/.
If you don't follow the instructions

-------------------
Installing Models
-------------------

Sail-on-client install instructions here for each problem: https://gitlab.kitware.com/darpa-sail-on/sail-on-client


Step 2:  Run
--------
From the home directory:
Tinker run command:

.. code-block:: bash

  tinker -c configs/problem_configs/image_classification_ond_config.yaml sailon_tinker_launcher/tinker_launcher.py


To change to a different config, copy the file `sailon_tinker_launcher/config.yaml`
and make your changes there.  You can update the -c parameter to load you new configuration.

Ask Roni about multirun capabilities.


Hydra Run Command:

.. code-block:: bash

  python hydra_launcher.py


You can either pass the new config items by overwritting them, such as

.. code-block:: bash

  python hydra_launcher.py problem.use_feedback=False


You can do multirun as well (look up hydra documentation: https://hydra.cc/docs/next/intro#multirun )

For example, if you want to run multiple tests, you can use this where you can
add to each list to run multiple in serial and separate the brackets to run in
multiple tasks (can be mixed with the last type of override as well):

.. code-block:: bash

  python hydra_launcher.py --multirun \
         problem.test_ids=["OND.54012315.0900.abc"],["OND.54012315.0900.DEF"]


Another way, if you want to run different problem configs (in `configs/problem`) if
you want to run different problem types or different protocols (probably if you have a lot of different parameters:

.. code-block:: bash

   python hydra_launcher.py --multirun \
          problem=image_classification_condda_config,image_classification_ond_config


If you want to use slurm to run it, just add `hydra/launcher=submitit_local` and
check out these docs: https://hydra.cc/docs/plugins/submitit_launcher

.. code-block:: bash

  python hydra_launcher.py  --multirun \
         problem.test_ids=["OND.54012315.0900.abc"],["OND.54012315.0900.ABC"] \
         hydra/launcher=submitit_local


You can create a config for your cluster as a new file in `configs/hydra/launcher` (see the one there for `veydrus`)

.. code-block:: bash

  python hydra_launcher.py  --multirun \
         problem.test_ids=["OND.54012315.0900.abc"],["OND.54012315.0900.ABC"]  \
         hydra/launcher=veydrus

Note:  you need --multirun to use slurm launcher (otherwise it is just local)

Step 3: Configuration for Your Run
-------------
The default configuration for this is shown in the `configs/problem` folder.  The launching
parameters that are the minimum necessary are as follows:
- protocol: either 'ond' or 'condda' to define which protocol to run
- harness:  either 'local' or 'par' to define which harness to use
- workdir: a directory to save all the information from the run including
    - Config
    - Output of algorithm





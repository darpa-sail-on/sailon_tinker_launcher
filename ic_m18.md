# Instructions for Image Classification

## Installation
1. Clone the following repositories
  ```
      git clone https://github.com/tinker-engine/tinker-engine.git
      git clone https://gitlab.kitware.com/darpa-sail-on/sail-on-api.git
      git clone https://gitlab.kitware.com/darpa-sail-on/evm_based_novelty_detector.git
      git clone https://gitlab.kitware.com/darpa-sail-on/sail-on-client.git
      git clone https://gitlab.kitware.com/darpa-sail-on/Sail_On_Evaluate.git
      git clone https://gitlab.kitware.com/darpa-sail-on/sailon_tinker_launcher.git
  ```
   This would create tinker-engine, sail-on-api, evm_based_novelty_detector,
   sailon_tinker_launcher, Sail_On_Evaluate and sail-on-client directories
   in your working directory.

2. Checkout branches from different repositories
  ```
    cd sail-on-client
    git checkout remove-algorithm-dependencies
    cd ../evm_based_novelty_detector
    git checkout add-eval-18-adapters
    cd ../sailon_tinker_launcher
    git checkout add-ond18-configs
  ```

3. Create virtual environment for sail-on-client
  ```
    cd ../sail-on-client
    pipenv install
    pipenv shell
  ```

4. Install evm_based_novelty_detector
  ```
    cd ../evm_based_novelty_detector
    pip install -r requirements.txt
    pip install -e .
  ```

5. Install sailon_tinker_launcher
  ```
    cd ../sailon_tinker_launcher
    pip install -r requirements.txt
    pip install -e .
  ```

## Running Algorithms with Multirun and Submitit

1. Download the feature extractor and evm model using
  ```
  wget https://vast.uccs.edu/~mjafarzadeh/trained_f1_umd_464.pth
  wget https://vast.uccs.edu/~mjafarzadeh/evm_cosine_F1_umd_464_tail_40000_ct_0.8_dm_0.65.pkl
  ```

2. Modify problem configs
  Set the following variables in sailon_tinker_launcher/configs/problem/ic_ond18.yaml
  and sailon_tinker_launcher/configs/problem/ic_ond18.yaml
    1. workdir: path to directory where all artifacts for the run are stored
    2. harness: Harness used for experiment (choices: local/par)
    3. test_ids: List of tests
    4. dataset_root: Root directory for images
    5. model_path (cnn_params): Path to the feature extractor model
    6. model_path (evm_params): Path to the evm model

3. Setup cluster config
  Create a configuration for the cluster that the job would execute on in
  sailon_tinker_launcher/configs/hydra/launcher. Refer to
  sailon_tinker_launcher/configs/hydra/launcher/veydrus.yaml for example.

4. Launch the configs using multirun
  ```
    python hydra_launcher.py --multirun problem=ic_without_rd_ond18,ic_ond18
  ```

5. Launch the configs using SLURM
  ```
  python hydra_launcher.py --multirun problem=ic_without_rd_ond18,ic_ond18 hydra/launcher=submitit_slurm
  ```

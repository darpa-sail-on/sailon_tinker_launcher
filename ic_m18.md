# Instructions for Image Classification

## Installation
1. Clone the following repositories
  ```
      git clone https://github.com/tinker-engine/tinker-engine.git
      git clone https://github.com/darpa-sail-on/sail-on-api.git
      git clone https://github.com/darpa-sail-on/evm_based_novelty_detector.git
      git clone https://github.com/darpa-sail-on/sail-on-client.git
      git clone https://github.com/darpa-sail-on/Sail_On_Evaluate.git
      git clone https://github.com/darpa-sail-on/sailon_tinker_launcher.git
  ```
   This would create tinker-engine, sail-on-api, evm_based_novelty_detector,
   sailon_tinker_launcher, Sail_On_Evaluate and sail-on-client directories
   in your working directory.

2. Checkout branches from different repositories
  ```
    cd sail-on-client
    git checkout update-condda
    cd ../evm_based_novelty_detector
    git checkout add-eval-18-adapters
    cd ../sailon_tinker_launcher
    git checkout add-condda-18-configs
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
    pip install -e timm
    pip install -e .
  ```
  Note: If your cuda version is different from the cuda supported by torch present
  on pypi, please uninstall torch and torchvision  and reinstall it from
  https://download.pytorch.org/whl/torch_stable.html using
  ```
    pip uninstall torch torchvision
    pip install torch==1.8.1+<cuda_version> torchvision==0.9.1+<cuda_version> -f https://download.pytorch.org/whl/torch_stable.html
  ```
  where `<cuda_version>` is the cuda version that you are using on your machine

5. Install sailon_tinker_launcher
  ```
    cd ../sailon_tinker_launcher
    pip install -r requirements.txt
    pip install -e .
  ```

## Running Algorithms with Multirun and Submitit

1. Download the feature extractor, evm model and known features using
  ```
  wget https://vast.uccs.edu/~mjafarzadeh/trained_f1_umd_464.pth
  wget https://vast.uccs.edu/~mjafarzadeh/evm_cosine_F1_umd_464_tail_40000_ct_0.8_dm_0.65.pkl
  wget https://vast.uccs.edu/~mjafarzadeh/feature_F1_umd_464_known_train.npy
  ```

2. Modify problem configs
  Set the following variables in sailon_tinker_launcher/configs/problem/ic_condda18.yaml
  and sailon_tinker_launcher/configs/problem/ic_condda18_wo_redlight.yaml
    1. workdir: path to directory where all artifacts for the run are stored
    2. harness: Harness used for experiment (choices: local/par)
    3. test_ids: List of tests
    4. dataset_root: Root directory for images
    5. model_path (cnn_params): Path to the feature extractor model
    6. model_path (evm_params): Path to the evm model
    7. feature_known_path (evm_params): Path to the known features downloaded in previous step

3. Without hydra
  ```
  tinker -c configs/problem/ic_conda18.yaml sailon_tinker_launcher/tinker_launcher.py
  tinker -c configs/problem/ic_conda18_wo_redlight.yaml sailon_tinker_launcher/tinker_launcher.py
  ```

3. Setup cluster config
  Create a configuration for the cluster that the job would execute on in
  sailon_tinker_launcher/configs/hydra/launcher. Refer to
  sailon_tinker_launcher/configs/hydra/launcher/veydrus.yaml for example.

4. Launch the configs using multirun
  ```
    python hydra_launcher.py --multirun problem=ic_conda18_wo_redlight,ic_conda18
  ```

5. Launch the configs using SLURM
  ```
  python hydra_launcher.py --multirun problem=ic_conda18_wo_redlight,ic_condda18 hydra/launcher=submitit_slurm
  ```
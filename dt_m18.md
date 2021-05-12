# Instructions for Document Transcription

## Installation
1. Clone the following repositories
  ```
      git clone https://github.com/tinker-engine/tinker-engine.git
      git clone https://github.com/darpa-sail-on/sail-on-api.git
      git clone https://github.com/darpa-sail-on/evm_based_novelty_detector.git
      git clone https://github.com/darpa-sail-on/hwr_novelty_detector.git
      git clone https://github.com/darpa-sail-on/sail-on-client.git
      git clone https://github.com/darpa-sail-on/Sail_On_Evaluate.git
      git clone https://github.com/darpa-sail-on/sailon_tinker_launcher.git
  ```
   This would create tinker-engine, sail-on-api, evm_based_novelty_detector,
   sailon_tinker_launcher, hwr_novelty_detector, Sail_On_Evaluate and sail-on-client
   directories in your working directory.

2. Checkout branches from different repositories
  ```
    cd sail-on-client
    git checkout fix-characterization
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

5. Install hwr_novelty_detector
  ```
    cd ../hwr_novelty_detector
    pip install -r requirements.txt
    pip install -e .
  ```

6. Install sailon_tinker_launcher
  ```
    cd ../sailon_tinker_launcher
    pip install -r requirements.txt
    pip install -e .
  ```

## Running Algorithms

1. Download the model from [this link](https://drive.google.com/file/d/1YJMAGS97zHC0cBkNirEcNLdJK0YhTGU0/view?usp=sharing)

2. Untar and move the folder containing the models to sailon_tinker_launcher/configs/extra_configs

3. Modify problem configs m18_hwr_nd.yaml
  Set the following variables in sailon_tinker_launcher/configs/problem/m18_hwr_nd.yaml
    1. workdir: path to directory where all artifacts for the run are stored
    2. harness: Harness used for experiment (choices: local/par)
    3. test_ids: List of tests
    4. dataset_root: Root directory for images

4. Launch the configs using
  ```
    tinker -c configs/problem/local_configs/local_hwr_nd.yaml sailon_tinker_launcher/tinker_launcher.py
  ```

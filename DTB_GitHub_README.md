# Digital Twin Brain (DTB)

## Perturbational Modelling of Transdiagnostic Network Phenotypes

------------------------------------------------------------------------

## Overview

This repository contains the codebase for constructing and perturbing
Digital Twin Brain (DTB) models used in the study:
Digital Twin Brain simulation and manipulation of a functional brain network underlying mental illness.
Authors: Xia et al.

In this work, we leverage a previously established Digital Twin Brain
framework to simulate and mechanistically perturb a transdiagnostic
cortico--subcortical network phenotype (NP factor) associated with
internalising and externalising psychopathology.

The framework enables:

-   Identification of NP factor
-   Construction of participant-specific neuronal-scale DTBs and simulation of task-evoked BOLD responses
-   Reconstruction of the NP connectivity factor
-   In silico modulation of excitatory (AMPA) and inhibitory (GABA-A) synaptic conductance in the DTBs
-   Population-scale perturbational analysis
-   Pharmacological validation mapping
-   Longitudinal symptom prediction

This repository provides the code required to reproduce the computational experiments described in the manuscript.

------------------------------------------------------------------------

## Scientific Rationale

Linking synaptic-level perturbations to distributed brain-network
dynamics remains a central challenge in computational psychiatry.

Using individualised DTBs grounded in structural and task-state
functional MRI data, we:

1.  Reconstructed a compact cortico-subcortical NP circuit phenotype\
2.  Performed controlled AMPA- and GABA-A--mediated synaptic
    perturbations\
3.  Quantified baseline-dependent, bidirectional network responses\
4.  Validated model-derived predictions against pharmacological fMRI\
5.  Predicted longitudinal symptom trajectories from simulated
    perturbational profiles

The DTB framework should be interpreted as a mechanistic perturbation
model rather than a direct pharmacodynamic simulation.

------------------------------------------------------------------------

## Repository Structure

    Identify_np_factor
    Data_preparation_for_model/
    Simulated_post_process/
    Statistical_analysis/
    Visualization/
    Data/


------------------------------------------------------------------------

## Core Components

### 1. Digital Twin Construction

-   Individual T1-weighted and DTI-derived structural features
-   Multi-population spiking neural networks
-   Leaky Integrate-and-Fire neuron dynamics
-   AMPA-mediated excitatory synapses
-   GABA-A-mediated inhibitory synapses
-   Balloon--Windkessel model for BOLD signal generation

### 2. Synaptic Perturbation

Global synaptic conductance parameters:

-   AMPA: 0.0020 -- 0.0052\
-   GABA-A: 0.0015 -- 0.0040

Parameters are constrained by:

-   Physiological firing-rate bounds
-   Network stability criteria
-   Simulated BOLD amplitude limits

These variables act as gain-control parameters governing circuit operating regimes.

### 3. NP Factor Reconstruction

The NP factor is defined as the summed strength of selected
cortico-subcortical task-state functional connections derived using
connectome-based predictive modelling.

### 4. Pharmacological Validation

Baseline--Δ functional connectivity mappings are estimated in silico and
applied to empirical placebo FC to predict ketamine- and
midazolam-induced network changes.

------------------------------------------------------------------------

## Reproducibility

-   All statistical analyses are fully scripted.
-   Raw imaging datasets are not included due to data protection
    regulations but may be requested from the respective consortia.

------------------------------------------------------------------------

## Computational Requirements

-   Python \>= 3.9
-   PyTorch
-   NumPy
-   SciPy
-   Nilearn
-   scikit-learn

Voxel-wise large-scale simulations require high-performance computing
resources.\
Regional DTBs are suitable for workstation-level replication.

------------------------------------------------------------------------

## Computational Load / Runtime Estimates

The computational requirements for running DTB simulations depend on model size, task length, and the number of repeated simulations. For large-scale models with 100 million neurons, a MID simulation typically requires 3 hours using 8 DCUs, and an SST simulation requires 5.5 hours using 8 DCUs, resulting in approximately 68 DCU-hours for baseline simulations. AMPA and GABA-A perturbations add additional runs (AMPA: 5 repetitions × 10 levels; GABA-A: 5 repetitions × 6 levels), while assimilation simulations are equivalent to 30 simulations, and resting-state parameter identification requires 5 additional runs. Taken together, a 100-million-neuron model for a single subject consumes roughly 7,820 DCU-hours. Scaling up to a model of 1 billion neurons yields an estimated 680 DCU-hours for a single simulation of MID and SST.

For regional-scale models with 3 million neurons, a MID simulation consumes about 2 DCU-hours, and an SST simulation consumes 3.5 DCU-hours. Including baseline, AMPA, and GABA-A manipulation simulations, and assimilation (equivalent to 32 simulations), each individual requires approximately 258.5 DCU-hours.

All simulations were performed on the SCINET high-performance computing platform (https://www.scnet.cn/ui/mall/#/mall/home￼). Multiple DCUs can be used in parallel to reduce wall-clock time. These estimates include all simulation and perturbational experiments required to reproduce the full computational analysis.

------------------------------------------------------------------------

## Conceptual Notes

-   AMPA and GABA-A parameters represent phenomenological gain controls.
-   DTBs are experimentally controllable computational systems, not
    biological replicas.
-   Baseline-dependent bidirectional responses arise from nonlinear
    recurrent network dynamics.

------------------------------------------------------------------------

## Citation

If you use this code, please cite.
------------------------------------------------------------------------

## License

This project is released under the MIT License.

------------------------------------------------------------------------

## Contact

Yunman Xia\
\[Fudan University\]\
\[xiayunman@outlook.com\]

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

-   Identification of np factor
-   Construction of participant-specific neuronal-scale DTBs
-   In silico modulation of excitatory (AMPA) and inhibitory (GABA-A)
    synaptic conductance
-   Simulation of task-evoked BOLD responses
-   Reconstruction and manipulation of the NP connectivity factor
-   Population-scale perturbational analysis
-   Pharmacological validation mapping
-   Longitudinal symptom prediction

This repository provides the code required to reproduce the
computational experiments described in the manuscript.

------------------------------------------------------------------------

## Scientific Rationale

Linking synaptic-level perturbations to distributed brain-network
dynamics remains a central challenge in computational psychiatry.

Using individualised DTBs grounded in structural and task-state
functional MRI data, we:

1.  Reconstructed a compact cortico--subcortical NP circuit phenotype\
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

These variables act as gain-control parameters governing circuit
operating regimes.

### 3. NP Factor Reconstruction

The NP factor is defined as the summed strength of selected
cortico--subcortical task-state functional connections derived using
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

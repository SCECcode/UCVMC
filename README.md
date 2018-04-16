# UCVMC
The Unified Community Velocity Model C-language (UCVMC) software framework is a collection of software tools designed to provide a standard interface to multiple, alternative, California velocity models. UCVMC is used in high resolution 3D wave propagation simulations for California. UCVMC development is an interdisciplinary research collaboration involving geoscientists, computer scientists, and software developers.

The Unified Community Velocity Model C-language (UCVMC) software repository contains a software codebase developed by Patrick Small, David Gill, Philip Maechling, and others at SCEC. UCVMC is released as open-source scientific software under an Apache 2 software license.

The UCVMC source code repository contains a reference implementation of the original C-language UCVM software framework. The UCVMC distribution is based on a previously released version of UCVM, which was called the UCVM v15.10 release. The UCVM v15.10 software distribution included several software features that provide great user flexibility, but that made the UCVM v15.10 software difficult to install, use, and support. This UCVMC distribution is a simplied version of the UCVM v15.10 software platform. This distribution provides a reference implementation of key UCVM feature, and provides examples that illustrate their usage and results.

# 1.0 System and Software Requirements

Testing UCVM on all possible combinations of operating sysetms and software stacks requires more software developer resources than currently available. So, we have defined a UCVM reference software stack that we use to develop and test the software. This UCVMC distrbution has been shown to work on the following reference software stack. It may work on other software stacks, also, but this is the supported software environment.

*  Linux operating system (e.g. CentOS 7 Linux) x86_64-linux 
*  GNU gcc/gfortran compilers version 4.8.5
*  Python 2.7.11 (Anaconda 4.0.0 (64-bit)
*  Autotools build software for Linux
*  Euclid Etree library: http://www.cs.cmu.edu/~euclid/ (provided during installation)
*  Proj.4 projection library: http://trac.osgeo.org/proj/ (provided during installation)

Optional Software for building MPI binaries:
*  mpich 1.2.6
*  openmpi 1.8.8

The following California velocity models packages are included as part of a standard UCVMC installation.
*  SCEC CVM-H v15.1
*  SCEC CVM-S4
*  SCEC CVM-S4.26
*  SCEC CVM-S4.26.M01
*  SCEC CCA 06, Central California
*  SCEC CS17.3
*  USGS BayArea Velocity Model 0.8.3
*  Southern California 1D Velocity Model
*  Northridge Region 1D Velocity Model

# 2.0 Installation
Once the target computer has the required software tools installed, the basic install of UCVMC is:
*  git clone https://github.com/SCECcode/UCVMC.git
*  cd UCVMC/largefiles
*  ./get_large_files.py
*  ./check_largefiles_md5.py
*  ./stage_large_files.py
*  cd ..
*  ./ucvm_setup.py

The ucvm_setup.py script runs in a terminal window and prints text questions to the user.  The user types answers to the questions in the terminal window. The install script asks the user which velocity models they would like to install from the following list: (CVM-H v15.1,CVM-S4, CVM-S4.26, CVM-S4.26.M01, and USGS CenCal). We recommend that the user installs all available models.

The script will then automatically compile, build, and install the selected models.

# 3.0 MPI Compilers and UCVM Programs

If a GNU-based MPI compiler is detected, the MPI version of several utilities are created, including ucvm2mesh_mpi, ucvm2etree_mpi, and basin_query_mpi are built. Otherwise, only the serial versions for these programs are built.

# 4.0 Configuration
The main UCVMC configuration file is ${UCVM_INSTALL_DIR}/conf/ucvm.conf. 
This file defines the paths to all configured models and maps, and it defines selected model flags, such as CVM-H USE_GTL.
The UCVM installer sets up this ucvm.conf file automatically.

In most cases, the user does not need to edit the UCVMC/conf/ucvm.conf. However, in some circumstatnces, such as if the user wants to move the UCVMC installation directory, or configure the behavior of the CVM-H model, the user  might want to edit the ucvm.conf file. Please see the User Guide for more details on how to edit the UCVMC/conf/ucvm.conf configuration file.

# 5.0 Standard Models and Maps
The CVM models available through UCVMC are assigned abbreviations, and these abbreviatioins are used to specify the models when making UCVM queries. The model abbreviations used by UCVM are defined in following tables:

Model Name | Description | UCVM Abbreviation
-----------|-------------|------------------
CVM-H      | Southern California Velocity Model developed by Harvard Structural Geology Group with optional geotechnical layer | cvmh
CVM-S4     | Southern California Velocity Model developed by SCEC, Caltech, USGS Group with geotechnical layer | cvms
CVM-S4.26  | Tomography improved version of CVM-S4 with no geotechnical layer | cvms5
CVM-S4.26.M01 | CVM-S4.26 with added geotechnical layer | cvmsi
CCA06 | Central California Velocity Model with optional geotechnical layer | cca
CS17.3 | Cypershake study 17.3 | cs173
USGS Bay Area | USGS developed San Francisco and Central California velocity model | cencal
Modified Hadley Kanamori 1D  | Southern California regional 1D model based on Hadley-Kanamori model | 1d
Northridge Region 1D | Los Angeles Region 1D model used in SCEC Broadband Platform | bbp1d

A state-wide California standard topography map is distribued with UCVMC. This is a statewide
topography map, that also includes statewide Vs30 values, combined into an etree structure.

Toopgrahy and Vs30 Map Name | Description | UCVM Abbreviation
----------------------------|-------------|------------------
USGS NED DEM and Wills-Wald Vs30 | California elevation and Vs30 data in etree format | ucvm

# 6.0 Documentation
Online UCVMC documentation is available at:
*  https://github.com/SCECcode/UCVMC/wiki

Additional documentation advanced features and previous versions of UCVM are posted at:
*  http://scec.usc.edu/scecpedia/UCVMC

# 7.0 License
UCVMC is released under the Apache 2.0 license. Please see the LICENSE file for distribution license and disclaimers.

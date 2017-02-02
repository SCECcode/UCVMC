# UCVMC
The Unified Community Velocity Model C-language (UCVMC) software framework is a collection of software tools designed to provide a standard interface to multiple, alternative, California velocity models. UCVMC is used in high resolution 3D wave propagation simulations for California. UCVMC development is an interdisciplinary research collaboration involving geoscientists, computer scientists, and software developers.

The Unified Community Velocity Model C-language (UCVMC) software repository contains a software codebase developed by Patrick Small, David Gill, Philip Maechling, and others at SCEC. UCVMC is released as open-source scientific software under an Apache 2 software license.

The UCVMC source code repository contains the reference implementation of the original UCVM software framework. The UCVMC distribution is based on an earlier publicly released version of UCVM, called the UCVM v15.10 release. The UCVM v15.10 software distribution included several software features that provide great user flexibility, but that made the UCVM v15.10 software difficult to install, use, and support. This UCVMC distribution is a simplied version of the UCVM v15.10 software platform. This distribution preserves a reference implementation for key UCVM feature and provides examples that illustrate their usage and results.

# 1.0 System and Software Requirements

The reference software version used to develop and test this version includes the following vesion. Other versions of the required software packages may work, but this is the reference collection of software:

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

The, ucvm_setup.py script runs in a terminal window and print text questions to the user.  The user types answers to the questions presented by script in the terminal window. This install script asks the users which models you would like to install (CVM-H v15.1,CVM-S4, CVM-S4.26, CVM-S4.26.M01, and USGS CenCal). We recommend that the user installs all available models.

The script will then automatically compile, build, and install the selected models.

# 3.0 Technical Notes
## 3.1 MPI Compilers

If a GNU-based MPI compiler is detected, the MPI version of several utilities are created, including ucvm2mesh_mpi, ucvm2etree_mpi, and basin_query_mpi are built. Otherwise, only the serial versions for these programs are built.

# 4.0 Configuration
The main application configuration file is ${UCVM_INSTALL_DIR}/conf/ucvm.conf. 
This is where the paths to all configured models and maps are specified, as  well as any model flags are defined. The UCVM installer sets up this ucvm.conf file automatically.

In most cases, the user does not need to edit the UCVMC/conf/ucvm.conf In some circumstatnces, such as if you move the UCVMC installation directory, or if you want to configure the behavior of the CVM-H model, you might want to edit the ucvm.conf file. Please see the User Guide for more details on how to edit the UCVM config.

# 5.0 Standard Models and Maps
The CVM models available through UCVMC are referenced with the following labels:

*  cvmh	     	   SCEC CVM-H
*  cvms	     	   SCEC CVM-S4
*  cmvs5           SCEC CVM-S4.26
*  cvmsi           SCEC CVM-S4.26.M01
*  cencal	   USGS Bay Area CenCalVM
*  1d		   Modified Hadley-Kanamori 1D Velocity Model
*  bbp1d           Northridge Region 1D Velocity Model

A state-wide California standard topography map is distribued with UCVMC. This is a statewide
topography map, that also includes statewide Vs30 values, combined into an etree structure.

*  ucvm	     USGS NED DEM and Wills-Wald Vs30 (default)

# 6.0 Documentation
Online UCVMC documentation is available at:
*  https://github.com/SCECcode/UCVMC/wiki

Additional documentation on previous version of UCVM are posted at:
*  http://scec.usc.edu/scecpedia/UCVMC

# 7.0 License
UCVMC is released under the Apache 2.0 license. Please see LICENSE for the distribution license and disclaimers.

# UCVMC
The Unified Community Velocity Model C-language (UCVMC) software framework is a collection of software tools designed to provide standard interface to multiple, alternative, California 3D velocity models. UCVMC is used in high resolution 3D wave propagation simulations for California. UCVMC development is an interdisciplinary research collaboration involving geoscientists and computer scientists.

The Unified Community Velocity Model C-language (UCVMC) software repository contains a software codebase developed by Patrick Small, David Gill, Philip Maechling, and others at SCEC. UCVMC is released as open-source scientific software under and Apache 2 software license.

The UCVMC source code repository contains the reference implementation of the original UCVM software framework. The UCVMC distribution is based on the UCVM V15.10 release. The UCVM v15.10 software distribution includes several software features that provide great user flexibility, but make the UCVM v15.10 software difficult to install, use, and support.

This UCVMC distribution is a simplied version of the C-language UCVM v15.10 software platform. This distribution preserves a reference implementation for each key UCVM feature and examples that illustrate their usage and results.

# 1.0 System and Software Requirements

The system requirements are as follows: 

- UNIX operating system (Linux and Mac OS X) 
- GNU gcc/gfortran compilers (MPI wrappers such as mpicc are OK) 
- Python 2.5+
- tar for opening the compressed files 
- Euclid Etree library: http://www.cs.cmu.edu/~euclid/
- Proj.4 projection library: http://trac.osgeo.org/proj/

Target Software Stack includes:
* OS: x86_64-redhat-linux
* Autotools build software stack for linux
* gcc version 4.8.5 20150623 (Red Hat 4.8.5-4) (GCC)
* Python 2.7.11 |Anaconda 4.0.0 (64-bit)| (default, Dec  6 2015, 18:08:32) 
* [GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux2

Optional dependencies include any of the following standard velocity models
and packages:

- Standard community velocity models: SCEC CVM-H, SCEC CVM-S4, SCEC CVM-S4.26, 
  SCEC CVM-S4.26.M01, USGS CenCalVM
- NetCDF: http://www.unidata.ucar.edu/downloads/netcdf/index.jsp

# 2.0 Installation
The basic install of UCVMC is:
% git clone https://github.com/SCECcode/UCVMC.git
$ cd UCVMC/largefiles
$ ./get_large_files.py
$ ./stage_large_files.py
$ cd ..
$ ./ucvm_setup.py

Then answer the questions presented by script in the terminal window. 
It will ask you which models you would like to install (CVM-H v15.1,CVM-S4, CVM-S4.26, CVM-S4.26.M01, and USGS CenCal).

The script will then automatically download and install the models you selected.

The default is to link dynamically. If you would like to create statically linked executables,
please use the argument -s. E.g. ./ucvm_setup.py -s

# 3.0 Technical Notes
## 3.1 MPI Compilers

If a GNU-based MPI compiler is detected, the MPI version of ucvm2etree are
built. Otherwise, the serial version is built.

## 3.2 Lustre Filesystems
The IOBUF module must be used when compiling the Etree library and UCVM for 
use on a Lustre high-performance filesystem. Please reference the Euclid Etree 
documention for instructions on how to do this for that package.

# 4.0 Configuration
The main application configuration file is ${UCVM_INSTALL_DIR}/conf/ucvm.conf. 
This is where the paths to all configured models and maps are specified, as 
well as any model flags are defined. The UCVM installer sets up this file 
automatically.

In some circumstatnces, such as if you move the UCVMC installation directory,
you might want to edit the ucvm.conf file. Please see the User Guide for more details on how to edit the UCVM config.

# 5.0 Standard Models and Maps
The CVM models available through UCVMC are referenced with the following labels:

cvmh	     	    SCEC CVM-H
cvms	     	    SCEC CVM-S4
cmvs5               SCEC CVM-S4.26
cvmsi               SCEC CVM-S4.26.M01
cencal	     	    USGS Bay Area CenCalVM
1d		    Hadley-Kanamori 1D (pre-linked)

Note that the model must be linked in at install time if it is to be queried 
through UCVM.

One standard map is distribued with UCVMC. This is a statewide
topography map, and a Vs30 map combined into an etree structure.

ucvm	     USGS NED DEM and Wills-Wald Vs30 (default)

# 6.0 Documentation
Online UCVMC documentation is available at:

http://scec.usc.edu/scecpedia/UCVMC

# 7.0 License
UCVMC is released under the Apached 2.0 license. Please see LICENSE for the distribution license and disclaimers.

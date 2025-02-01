Installation
============

Prerequisites
-------------
System Requirements:
  - gcc (GNU Compiler Collection)
  - libgfortran5 (runtime library for gfortran)
  - Python 3.6 or later

Core Package Dependencies:
  - pandas==1.5.1
  - scipy==1.9.3
  - numpy==1.23.4
  - astropy==5.1.1
  - emcee==3.1.3

See full list of dependencies in requirements.txt.  


Environment Setup
-----------------
Conda (Recommended)
~~~~~~~~~~~~~~~~~~~
1. Download the environment.yml file from:
   https://github.com/MingjieJian/SME

2. Create and activate the environment:
   
   .. code-block:: bash

       conda env create -f environment.yml
       conda activate pysme

PIP + System Package Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Install system dependencies.

   - On Ubuntu/Debian:

     .. code-block:: bash

         sudo apt-get install libgfortran5 gcc

   - On CentOS/RHEL:

     .. code-block:: bash

         sudo yum install libgfortran gcc

2. Install Python dependencies:

   .. code-block:: bash

       pip install -r requirements.txt

Alternative Pip Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For the development version:

   .. code-block:: bash

       git clone https://github.com/MingjieJian/SME.git
       cd SME
       pip install -e .

For the stable version:

   .. code-block:: bash

       pip install pysme-astro

Data Files
----------
Required data files are available at:
http://www.stsci.edu/~valenti/sme.html

Place the files in:
  - ~/.sme/atmospheres/  (files from SME/atmospheres)
  - ~/.sme/nlte_grids/   (*.grd files from SME/NLTE)

Getting Started
---------------
Example scripts are in the examples directory:
https://github.com/MingjieJian/SME/tree/master/examples

To run the minimal example:

   .. code-block:: bash
    
       python minimum.py
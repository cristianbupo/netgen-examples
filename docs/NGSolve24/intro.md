# NGSolve 24

Authors:
Schöberl, Neunteufel, Pechstein, Lederer, Lehrenfeld, Lackner, Hochsteger,
Wess, Weggler, Stocker, Gopalakrishnan, Bonetti, Zerbinati,  .... ? 


This material are updated tutorials for the 2024 NGSolve-usermeeting.

Downlaod notebooks: [NGSolve24.zip](NGSolve24.zip)


It contains

* a compressed beginner's tutorial

* advanced NGSolve tutorials for
  - solid and structural mechanics
  - computational fluid dynamics
  - electromagnetics: TEAM benchmarks

* linked tutorials for add-on packages
  - boundary element methods
  - space-time tent-pitching methods
  - Trefftz methods
  - primal/dual cell method
  - NGSolve-PETSc interface



There co-exists other tutorials and teaching material, with some overlap:

* The [NGSolve i-tutorials](https://docu.ngsolve.org/latest/i-tutorials/index.html).
They form kind of reference material for specific topics and methods. There, methods are explained on simple model cases, most often on the unit-squares.
* The [NGSolve i-FEM](https://jschoeberl.github.io/iFEM/intro.html) lecture notes.
This material is written primarily for teaching finite element methods using NGSolve.


In the NGS24 material we focus on application areas. People with a background in a certain
engineering discipline find how to formulate domain specific problems in the generic NGSolve
language, and see what kind of solvers are approriate for their problems.

Emphasis is given also to large scale problems, with scalable preconditioners and solvers.
For MPI-parallel computing we show how to solve problems using PETSc via the ngsPETSc
interface.


NGSolve Jupyter-blitz: https://ngsolve.github.io/ngs24blitz/intro.html


**Mini-tutorials**


|                         | 9:10-10:00 | 10:00 - 10:45 |
|-------------------------|------------|---------------|
| App-dev (Chris,Matthias)    |            |    Room 2     | 
| BEM (Lucy)              |  main      |               |
| CutFEM (Christoph)      |  Room 4    |               |
| DiffGeo (Michi N)       |  Room 3    |               |
| Preformance (Joachim)   |            |    main       |   
| PETSc (Umberto)         |            |    Room 4     |
| Trefftz (Paul)          |  Room 2    |               |
| Waves (Markus)          |            |    Room 3     |

**Matrial:**

BEM, Trefftz, CutFEM, Trefftz, PETSc, Waves: see add-on packages

DiffGeo: [material](diffgeo_material.zip)
Performance: [TaskManager](https://docu.ngsolve.org/latest/i-tutorials/appendix-taskmanager/taskmanager.html)  [MPI](https://jschoeberl.github.io/iFEM/MPIparallel/intro.html) [GPU](https://docu.ngsolve.org/latest/i-tutorials/unit-5.5-cuda/poisson_cuda.html)
[Lukas' NgsAMG](https://github.com/LukasKogler/NgsAMG)


## Installing Parallel NGSolve

Traditionally, NGSolve is installed using the Python package installer pip. Instructions for installing with conda are found below.

Install Python, version 3.8 or later. If you can start python3, but not python, you can set an alias: `alias -g python='python3'`



You may want to install NGSolve into a fresh [virtual environment](https://docs.python.org/3/tutorial/venv.html)

````{tab-set}
```{tab-item} Linux/MacOS

    python3 -m venv ngs24
    source ngs24/bin/activate
    
```
```{tab-item} Windows

    python -m venv ngs24
    ngs24\Scripts\activate
```
````

### Install NGSolve

It is easy to install NGSolve using

    python -m pip install numpy scipy matplotlib jupyter ipyparallel scikit-build
    python -m pip install --upgrade ngsolve webgui_jupyter_widgets

If you need latest pre-releases:

    python -m pip install --upgrade --pre ngsolve webgui_jupyter_widgets


To check the installation of NGSolve run in the console:

    python -c "import ngsolve; print(ngsolve.__version__)"

solve a first example:

    python -m ngsolve.demos.intro.poisson

solve a first example with the legacy Netgen gui:

    python -i -c "import netgen.gui; import ngsolve.demos.intro.poisson"
    

Then, open jupyter-notebook (or jupyter-lab or VS Code), create a new notebook, create and execute a cell with

    from ngsolve import *
    from ngsolve.webgui import Draw
    Draw (unit_cube.shape);


### Install MPI and mpi4py (optional)

If you have mpi installed you are certainly able to use it.


````{tab-set}

```{tab-item} Linux

  supported are openmpi4, openmpi5, mpich.
  A quick way to install mpi is using binaries from conda:

    python -m pip install -i https://pypi.anaconda.org/mpi4py/simple openmpi    

```

```{tab-item} MacOS
  install openmpi: either binaries from conda, or compile yourself:
  
    python -m pip install -i https://pypi.anaconda.org/mpi4py/simple openmpi

  installation from source: [openmpi 5.0.5](https://www.open-mpi.org//software/ompi/v5.0)

    curl  https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-5.0.5.tar.bz2 --output openmpi-5.0.5.tar.bz2
    tar -xzf openmpi-5.0.5.tar.bz2
    cd openmpi-5.0.5
    ./configure
    make all 
    sudo make all install
```

```{tab-item} Windows
  install Intel-MPI:
  
    pip install impi_rt impi-devel

  not supported is MS-MPI
```
````

Then, install mpi4py, [**version 4**](https://mpi4py.readthedocs.io/en/latest/intro.html#what-is-mpi),
many thanks to Lisandro Dalcin.

    python -m pip install --no-cache-dir "mpi4py>=4.0.0"

test it using

    mpiexec -n 2 python -c "from mpi4py import MPI; print (MPI.get_vendor()); c=MPI.COMM_WORLD; print ('I am', c.rank, 'out of', c.size)"


and then mpi-parallel NGSolve:  (NEEDS THE NEXT UPDATE)

    mpiexec -n 4 python -m ngsolve.demos.mpi.mpi_poisson


### Install PETSc (optional, needs mpi):

Support for Linux and MacOS. Windows support with WSL only.

Install PETSc as a source wheel:

    export PETSC_CONFIGURE_OPTIONS="--with-fc=0 --with-debugging=0 --download-hypre \
             COPTFLAGS=\"-O2\" CXXOPTFLAGS=\"-O2\" "
    python -m pip install --upgrade --no-deps --force-reinstall --no-cache-dir petsc petsc4py

The NGSolve-PETSc interface (U. Zerbinati, S. Zampini):

    python -m pip install git git+https://github.com/NGSolve/ngsPETSc.git
    

### Install Hypre (optional, needs mpi):

See [ngsHypre](https://github.com/NGSolve/ngsHypre)

````{tab-set}
```{tab-item} NGS-User
You are installing regular releases of NGSolve:

    python -m pip install git+https://github.com/NGSolve/ngsHypre.git
    mpiexec -np 4  python -m ngs_hypre.demos.example1

```
```{tab-item} NGS-Developer
You are using pre-releases, or compile NGSolve yourself:

    python -m pip install scikit-build-core pybind11_stubgen toml
    pip3 install --no-build-isolation git+https://github.com/NGSolve/ngsHypre.git
    mpirun -np 4  python3 -m ngs_hypre.demos.example1
```
````



### Installing using conda

(DRAFT DRAFT) The quickest path to a parallel NGSolve is using conda. Conda-forge provides binary packages for MPI and PETSc for many platforms and versions (TODO: list versions). Install anaconda (or mini-conda), and run something like

    source ~/miniconda3/bin/activate 
    conda install mpi4py petsc4py
    python -m pip install --pre --upgrade ngsolve

then, test the installation using ...

(not yet working properly)


## Known issues are
- Use pip3 instead of pip if there is no pip
- If you get an error like `externally-managed-environment`, then either use
virtual environments, or add the flag `--break-system-packages` to the pip command, see [explanation](https://veronneau.org/python-311-pip-and-breaking-system-packages.html)

- If you have conflicts with other packages, you may install NGSolve in a [virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments).

- If NGSolve compuatations are working, but you don't get the rendering: For jupyter notebook version < 7.0.0 you have to run additionally

      jupyter nbextension install --user --py webgui_jupyter_widgets
      jupyter nbextension enable --user --py webgui_jupyter_widgets
  

- **Visual Studio Code and Pylance:**
  When working in a `virtual environment` with `vscode` and `pylance` you might have some issues:

      Import "ngsolve" could not be resolved Pylance (reportMissingImports)

  To fix this access the settings of vscode and add the following lines to the `settings.json` file and add:

  ```json
  {
      "python.analysis.extraPaths": [
          "<path to the virtual environment>/lib/python3.10/site-packages",
      ]
  }
  ```

```{tableofcontents}
```

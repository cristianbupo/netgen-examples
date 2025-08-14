# NGSolve24


Instructions for authors:

* prepare notebooks in
  - SaS (Astrid + Michi)
  - CFD (Christoph + Philip)  
  be careful with notebooks + git

* support by all on geometric modeling, modern syntax, fast solvers,  MPI(Umberto), webgui 

* build with

  jupyter-book build .

  We build the book by deploying this script

      # ssh jschoebe@tensor.asc.tuwien.ac.at 'bash -s' < build.sh
      source .profile 
      git clone git@github.com:NGSolve/NGSolve24.git
      cd NGSolve24
      jupyter-book build .
      # ghp-import -n -p -f _build/html
      # copy to ngsolve-page
      cd ..
      rm -rf NGSolve24


The result is here: https://docu.ngsolve.org/ngs24/intro.html


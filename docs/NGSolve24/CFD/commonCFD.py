# VTKOUT = False
# MPI_RANKS = 4    
# MEMORY = 16      # memory in GB

# VTKOUT = False
# MPI_RANKS = 48
# MEMORY = 1024      # memory in GB

import os
MPI_RANKS = int(os.environ.get('NGS_MPI_RANKS', 4))
MEMORY = int(os.environ.get('NGS_MEMORY', 16))
VTKOUT = bool(os.environ.get('NGS_VTKOUT', False))

# print ("MPI_RANKS: ", MPI_RANKS)
# print ("MEMORY: ", MEMORY)
# print ("VTKOUT: ", VTKOUT)






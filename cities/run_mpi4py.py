import time
from mpi4py import MPI

import dist_cities as dc

# MPI settings

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()

# prepare data and determine workloads

if rank == 0:
    cities = dc.read_cities()
    coord_pairs = dc.create_coord_pairs(cities)
    npairs = len(coord_pairs)

    dn = npairs // nprocs
    if npairs % nprocs != 0:
        dn += 1

# compute via MPI
# 1. Slice coord_pairs for processes
# 2. Scatter the sliced pieces
# 3. Do computation on each process
# 4. Gather results to master process
# 5. Collect the results into one list

t0 = time.time()

if rank == 0:
    data = [coord_pairs[int(x*dn):int((x+1)*dn)] for x in range(nprocs)]
else:
    data = None
   
data = comm.scatter(data, root=0)

result = [dc.calc_dist(p) for p in data]

result = comm.gather(result, root=0)

if rank == 0:
    output = []
    for a in result:
        output += a

t1 = time.time()

if rank == 0:
    print("Maximum distance: %.0f km" % max(output))
    print("Computing time: %.3f sec" % (t1-t0))

# Using Jupyter on Tetralith

## Starting Jupyter under ThinLinc at NSC

Starting Jupyter under ThinLinc is done in a few simple steps.

### Running a notebook on a login node

- Start a terminal
- `tetralith~$ module load Python/3.6.3-anaconda-5.0.1-nsc1`
- `tetralith~$ jupyter-notebook`
- **Note:** only lightweight tasks should be performed on the login node, such as light pre- and postprocessing work and submitting jobs to the SLURM scheduler.

### Running a notebook on a compute node¶

- Start a terminal
- `tetralith~$ interactive -N 1 -t 120 -A snic2018-x-yy`
- `n1~$ module load Python/3.6.3-anaconda-5.0.1-nsc1`
- `n1~$ jupyter-notebook --no-browser --ip=n1`
- `tetralith~$ firefox`
- Copy the URL from the interactive terminal on n1 and paste it into firefox (not starting Firefox first, but just pressing Ctrl and clicking on the URL may also work)


## Starting Jupyter using an ssh tunnel

If you would rather use a browser on your local laptop/desktop, you can instead use an ssh tunnel. However, this currently only works for running notebooks on the login nodes.

Running a notebook on a login node

- `mylaptop~$ ssh -L 9988:localhost:9988 x_abcde@tetralith.nsc.liu.se`
- `tetralith~$ module load Python/3.6.3-anaconda-5.0.1-nsc1`
- `tetralith~$ jupyter-notebook --port=9988 --no-browser`
- Copy the URL displayed in the terminal into a browser running on "mylaptop".
- **Note:** only lightweight tasks should be performed on the login node, such as light pre- and postprocessing work and submitting jobs to the SLURM scheduler.

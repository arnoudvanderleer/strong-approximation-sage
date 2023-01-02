# Accompanying Sage code for Master's Thesis
This repository contains sage versions for the algorithms contained in the Master's Thesis "Strong Approximation for a Family of Quadratic Surfaces".

## Layout of the repository
First of all, the repository contains sage code in files called `Lemma x.y.ipynb` and `Theorem x.y.ipynb`. Furthermore, reusable library versions of these are contained in the file `algorithms.ipynb` (to use it, first convert it to a python file using the script `compile.sh`). Lastly, there is some common library code in the files `common.ipynb` and `algorithm_states.ipynb`.

## Running the code

To run the code, you will at least need a local install of sagemath. I believe this will also install jupyter.

The following instructions have been tested on Ubuntu 20.04.

Then, you will need to compile the pieces of sage code that are used as a library in the other sage scripts. To that end, execute

```
./compile.sh common.ipynb
./compile.sh algorithm_states.ipynb
./compile.sh algorithms.ipynb
```

Then, start a jupyter notebook environment using

```
sage -n jupyter
```

This will bring up a new tab in your browser with the jupyter environment, in which you can now execute the various notebooks.
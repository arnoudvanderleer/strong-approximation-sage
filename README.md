# strong-approximation-sage
This repository contains sage versions for the algorithms contained in the Master's Thesis "Strong Approximation for a Family of Quadratic Surfaces".

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
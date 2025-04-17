"""Calculates the scattering coefficients for a given network and data.

This module is used to calculate the scattering coefficients for a given network
and data. The scattering coefficients are calculated for each time sample and
each channel. Prior to the scattering calculation, the scattering network is
initialized with the given parameters with the notebook 02_network_design.ipynb. 

Parameters
----------
pooling : str
    The pooling method to use.
filepath_scattering_coefficients : str
    The filepath to save the scattering coefficients.
filepath_stream : str
    The filepath to the database.
filepath_model : str
    The filepath to the model.

Notes
-----

This script can be run with the following command:

python calculate_scatterings.py --pooling avg --filepath_scattering_coefficients data/scattering_2.0.pickle


(python scatterings.py \
    --pooling avg \ 
    --filepath_scattering_coefficients ../data/scattering_coefficients.pkl \ 
    --filepath_stream ../data/database.pkl \ 
    --filepath_model ../data/model.pkl)


In order to run on a cluster, the script calculate_scatterings.sh can be used.
Please have a look at the script for more information.

Made by Leonard Seydoux in January 2023.
"""

import argparse
import pickle

from multiprocessing import Pool

import numpy as np
from tqdm import tqdm

from scripts_py import loader

# Argument parser
parser = argparse.ArgumentParser(
    description="Calculate scattering coefficients."
)
# parser.add_argument(
#     "--pooling",
#     help="pooling method to use (avg, max, or med).",
#     type=str,
# )
# parser.add_argument(
#     "--filepath_scattering_coefficients",
#     help="filepath to save the scattering coefficients.",
#     type=str,
# )
# parser.add_argument(
#     "--filepath_model",
#     help="filepath to the network model.",
#     type=str,
# )

# Parse arguments
ARGUMENTS = parser.parse_args()

 # Pooling type conversion
# if ARGUMENTS.pooling == "avg" : red_type=np.mean 
# if ARGUMENTS.pooling == "med" : red_type=np.median
# if ARGUMENTS.pooling == "max" : red_type=np.max

def transform_waveform(index):
    """Transforms a waveform into scattering coefficients.

    This function transforms a waveform into scattering coefficients. The
    scattering coefficients are calculated for each time sample and each
    channel. The scattering coefficients are returned as a list of lists. The
    choice of lists to store the scattering cofficients is the ease of use with
    various versions of Python, and the uncoupling between saving and reading.
    They are later converted to xarray Datasets for ease of maniputation. The
    are later loaded in the notebooks with the help of the xarray module for
    ease of access.

    Parameters
    ----------
    index (int):
        The index of the waveform in the database.

    Returns
    -------
    list:
        The scattering coefficients for each time sample and each channel.
    """
    # Transform waveforms into scattering space
    scattering_coefficients = loader.model.transform_sample(
        loader.segments[index], reduce_type=loader.pooling
    )

    return scattering_coefficients


def main():

    # Print the number of cores used
    n_tasks = 8
    # show file name
    print(f"Data file: {loader.data_file}") 
    print(f"Number of cores: {n_tasks}")

    # Map transform_waveform to all waveforms in parallel
    with Pool(n_tasks) as pool:
        scattering_coefficients = list(
            tqdm(
                pool.imap(transform_waveform, range(len(loader.segments))),
                desc="Transforming",
                total=len(loader.segments),
            )
        )

    # Map transform_waveform to all waveforms NOT in parallel
    # for i in range(len(loader.segments)):
    #     print(f"Running transform it",i)
    #     scattering_coefficients = transform_waveform(i)
    
    # Save scattering coefficients into a pickle file
    savepath = loader.scattering_coef_path+"Scat_coef_"+loader.pooling+"_"+loader.data_file
    with open(savepath, "wb") as file:
        pickle.dump([scattering_coefficients, loader.times], file)
    print(f"Scattering coefficients saved at :",savepath)        


if __name__ == "__main__":
    main()

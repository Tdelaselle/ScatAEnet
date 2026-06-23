"""Calculates the scattering coefficients for a given network and data.

This module is used to calculate the scattering coefficients for a given network
and data. The scattering coefficients are calculated for each time sample and
each channel. Prior to the scattering calculation, the scattering network is
initialized with the given parameters with the notebook 02_network_design.ipynb. 

Made by Leonard Seydoux in January 2023.

Adapted by Théotime de la Selle in june 2024 for acoustic data analysis
"""

import pickle

from multiprocessing import Pool

import numpy as np
from tqdm import tqdm

from scripts_py import loader


def transform_waveform(index, arg_pool=False):
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
        loader.segments[index], reduce_type=loader.pooling, arg_pool=arg_pool
    )

    return scattering_coefficients


def main():

    # Print the number of cores used
    n_tasks = 6
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

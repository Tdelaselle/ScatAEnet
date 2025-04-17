"""Load data and model for the transform_waveform function."""

import glob
import pickle

import numpy as np
import obspy
import tqdm
import xarray as xr
import Analysis_param_2

# -------------------------------------------- filepaths and parameters
data_file = Analysis_param_2.data_file
DIRPATH = Analysis_param_2.DIRPATH
model_file = Analysis_param_2.model_file
param_path = Analysis_param_2.data_param
pooling = Analysis_param_2.pooling
scattering_coef_path = Analysis_param_2.Scattering_coef_path
fig_path = Analysis_param_2.fig_path
# -----------------------------------------------------------

# Load database and model. This are assigned to the global namespace to be used
# in the transform_waveform function in parallel.
print("Loading model and data")
filepath = DIRPATH+data_file
# stream = obspy.read(filepath)   # for mseed files reading
stream = pickle.load(open(filepath, "rb"))
model = pickle.load(open("model/"+model_file, "rb"))

# Loop over the entire stream
times = list()
segments = list()
segment_duration = model.bins / stream[0].stats.sampling_rate
for traces in stream.slide(segment_duration, segment_duration):

    segment = np.zeros(model.bins + 1)

    # for trace in traces.split():
        # Pre-process slides
        # trace.detrend("demean")
        # trace.filter("highpass", freq=1, corners=2)

    tmp = np.hstack([trace.data for trace in traces.split()])
    n = min(len(tmp), model.bins + 1)
    segment[:n] = tmp[:n]
    # segment[: len(tmp)] = tmp

    # Discard extra sample
    segment = segment[:-1]
    
    # Turn into a numpy array, and discard extra sample
    # segment = np.array([trace.data for trace in traces])
    # segment = segment[:, :-2]

    # Collect first timestamp and data segment
    times.append(traces[0].times("matplotlib")[0])
    segments.append(segment)


print("Done !")

def reshape_scatterings(x):
    """Get the scattering coefficients into an xarray dataset.

    Parameters
    ----------
    x : list
        The scattering coefficients.

    Returns
    -------
    xarray.Dataset
        The scattering database in the xarray.Dataset format.
    """
    # Get metadata
    channels = ["XX"]
    n_channels = len(channels)

    # Xarray attributes
    attributes = {"n_samples": model.bins}

    # Xarray dimensions
    dimensions = (
        "time",
        "channel",
        *[f"f{i + 1}" for i in range(model.depth)],
    )

    # Xarray coordinates
    coordinates = {
        f"f{i + 1}": (dimensions[2 + i], f)
        for i, f in enumerate([bank.centers for bank in model.banks])
    }
    coordinates.update(
        {
            "index": ("time", np.arange(len(segments))),
            "time": ("time", [t * 24 * 3600 for t in times]),
            "channel": ("channel", channels),
        }
    )

    # Xarray data variables
    frequencies = [bank.centers for bank in model.banks]
    n_filters = [len(centers) for centers in frequencies]
    variables = dict()
    for order in range(model.depth):

        # Initialize scattering matrix
        shape = (len(segments), n_channels, *n_filters[: order + 1])
        variable = np.zeros(shape)

        # Variable dimensions
        dimension = (
            "time",
            "channel",
            *[f"f{j + 1}" for j in range(order + 1)],
        )

        # Fill scattering matrix
        for index in range(shape[0]):
            if x[index] is not None:
                for channel in range(n_channels):
                    variable[index, channel] = x[index][order]

        # Assign scattering matrix to data variable
        variables[f"order_{order + 1}"] = (dimension, variable)

    # Assign attributes and data variables to dataset
    ds = xr.Dataset(coords=coordinates, data_vars=variables, attrs=attributes)

    return ds

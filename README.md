# ScatAEnet (still under development)

Application of a **scattering network** for **acoustic emission (AE)** data analysis — an
adapted version of [Scatseisnet](https://zenodo.org/records/15110686).

This repository provides the Python scripts and notebooks used to:

1. recompose continuous acoustic recordings from raw datastreaming files,
2. design and apply a scattering network to those recordings,
3. synchronize parametric (mechanical) data with the acoustic recording, and
4. detect and cluster acoustic emission signals in the scattering space.

> _Note: this repository only contains the pre-processing (continuous AE recordings) and
> post-processing (scattering coefficients) code. The scattering network library itself,
> `scatseisnet`, is bundled here in the [scatseisnet/](scatseisnet/) folder. See
> <https://zenodo.org/records/15110686> for the reference Scatseisnet release._

---

## Repository organisation

| Path | Content |
| --- | --- |
| [scripts_py/](scripts_py/) | Helper scripts. `AE_ASCII_Obspy.py` converts raw AE datastreaming (TXT) into an ObsPy stream; `loader.py` loads the stream + network and segments the stream for the scattering computation. |
| [analysis_bank/](analysis_bank/) | Configuration files. `Analysis_param.py` defines the file paths and parameters (data file, model file, pooling, downsampling, …) for a given analysis run. |
| [scatseisnet/](scatseisnet/) | Bundled scattering network library (`ScatteringNetwork`, filter banks, wavelets and core operations) adapted for AE data. |
| [parametric_data/](parametric_data/) | Parametric data, e.g. the synchronized parametric dataframes produced by the synchronization notebook (`.pkl`). |
| [scattering_coefficients/](scattering_coefficients/) | Output scattering coefficients computed by `calculate_scatterings.py` (`.pkl`). |
| [calculate_scatterings.py](calculate_scatterings.py) | Main script that transforms the segmented waveforms into scattering coefficients (in parallel). |
| [Network_design.ipynb](Network_design.ipynb) | Builds, visualises and saves a scattering network instance. |
| [Parametric_synchronization.ipynb](Parametric_synchronization.ipynb) | Synchronizes parametric data with the continuous AE recording and assembles parametric dataframes. |
| [AE_recording_exploration.ipynb](AE_recording_exploration.ipynb) | Detection and clustering of AE signals from the scattering coefficients (UMAP + DBSCAN), with graphics. |

Two folders are referenced by the scripts but are **not** versioned (you create them locally):

- `data/` — input ObsPy stream files (the output of `AE_ASCII_Obspy.py`).
- `model/` — saved scattering network instances (the output of `Network_design.ipynb`).

---

## Setting up the Python environment

The code targets **Python 3.10+**. Using a dedicated virtual environment is recommended.

### With `venv` (standard library)

```bash
# from the repository root
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### With `conda`

```bash
conda create -n scataenet python=3.11
conda activate scataenet
pip install -r requirements.txt
```

To use the notebooks, register the environment as a Jupyter kernel (optional) and launch
Jupyter from the repository root:

```bash
python -m ipykernel install --user --name scataenet
jupyter lab        # or: jupyter notebook
```

The bundled `scatseisnet` package is imported directly from the repository, so run the
scripts and notebooks **from the repository root** (this keeps relative imports such as
`from scatseisnet import ScatteringNetwork` and `from scripts_py import loader` working).

---

## Processing workflow

The typical pipeline runs in the following order.

### 1. Recompose the continuous recording — `scripts_py/AE_ASCII_Obspy.py`

Raw AE acquisition produces a set of TXT datastreaming files (one or several channels).
This script reads them, concatenates them per channel and builds an ObsPy `Stream`, saved
either as a serialized pickle (`.pkl`) or in MSEED format.

```bash
python3 scripts_py/AE_ASCII_Obspy.py \
    -data ./data/raw_txt/ -save ./data/ -f pkl \
    -files 0 5 -d 2023-01-01T00:00:00.000 \
    -ch 1 2 -sampling 2 5 -sensors nano30 micro200 \
    -head 13 -col 1 -n my_record
```

Key arguments (`-h` for the full list):

- `-data` / `-save`: input TXT directory / output directory.
- `-f`: export format, `pkl` or `mseed` (default `mseed`).
- `-files`: index of the first and last file to load (omit to load all).
- `-d`: stream start time, `YYYY-MM-DDTHH:mm:ss.sss`.
- `-ch`, `-sampling`, `-sensors`: channel numbers, sampling rates (MHz) and sensor
  references, one entry per channel.
- `-head`, `-col`: number of header lines and number of columns (1 or 2) in the TXT files.
- `-n`: output file name (the result is saved as `Stream_<name>.<format>`).

> The channel number must appear in each datastreaming file name in the form `_N_`.

### 2. Design the scattering network — `Network_design.ipynb`

Set the window duration, sampling rate and the filter-bank parameters (octaves,
resolution, quality for each order), instantiate `ScatteringNetwork`, optionally visualise
the filter banks, then save the network instance to `model/` (file name encodes the
parameters, e.g. `network_win_0.04_samp_2.0_1o_541_2o_1521.pkl`).

### 3. Compute the scattering coefficients — `calculate_scatterings.py`

First edit [analysis_bank/Analysis_param.py](analysis_bank/Analysis_param.py) to point to
the right input stream and network and to choose the parameters:

- `data_file`, `DIRPATH`: input stream file name and its directory (`data/` by default).
- `model_file`: network file name (looked up in `model/`).
- `pooling`: pooling method — `max` (sensitive to short transients / hits), `med` (general
  continuous clustering) or `avg`.
- `downsampling`: decimation factor applied to the stream (`1` = none).
- `arg_pool`: whether to also return the argmax of the pooling operation.
- `Scattering_coef_path`: output directory.

Then run:

```bash
python3 calculate_scatterings.py
```

The script (via `scripts_py/loader.py`) loads the stream and the network, slides over the
stream to build the segments, transforms each segment into scattering coefficients in
parallel (multiprocessing), and saves the result as
`scattering_coefficients/Scat_coef_<pooling>_<data_file>`.

### 4. Synchronize parametric data — `Parametric_synchronization.ipynb`

Reads and preprocesses the parametric (mechanical) recordings — mechanical noise / elastic
and fatigue-testing data — aligns them in time with the continuous AE stream, assembles the
per-stream parametric dataframes and saves them under `parametric_data/`.

### 5. Detect and cluster AE signals — `AE_recording_exploration.ipynb`

Loads the scattering coefficients and the synchronized parametric data, normalizes and
reshapes the scatterings, then:

- runs **UMAP** to build a low-dimensional atlas of the dataset,
- applies **DBSCAN** to separate AE signals from the acoustic background,
- clusters the detected AE signals and produces the analysis graphics (detection rate,
  cluster waveforms, cross-correlations, cyclic position, scattering spectrograms, …).

---

## About

This package was created and documented by Théotime de la Selle, based on works from
Léonard Seydoux. Contributions are very welcome.

This work was supported by the French ANR project _e-Warnings_ (ANR-19-CE42-001).

> __Copyright ©️ 2024 Théotime de la Selle__
>
> This program is free software: you can redistribute it and/or modify it under the terms
> of the GNU General Public License as published by the Free Software Foundation, either
> version 3 of the License, or (at your option) any later version.
>
> This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
> without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
> See the GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public License along with this
> program. If not, see <https://www.gnu.org/licenses/>.

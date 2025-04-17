# -------------------------------------------- filepaths and parameters
data_file = "Stream_100MPa_102_ch3.pkl"

fig_path = "/home/delaselt/Documents/Acoustic_mining/CETIM/Galling_2025/figures/100MPa_102/" # for local computing
data_param = "/home/delaselt/Documents/Acoustic_mining/CETIM/Galling_2025/parametric_data/Param_100MPa_102.pkl"     # Folder and file (without extension) containing the parametric data (for any channels)

model_file = "network_win_0.015_samp_2.5_1o_671_2o_1331.pkl"
pooling = "max" # pooling method to use (avg, max, or med). Use max for high sensibility to short attack and transient phenomena (hits detection), med for general continuous clustering 
downsampling = 2 # downsampling the data to 100kHz (True) or not (False)

DIRPATH = "/home/delaselt/Documents/Acoustic_mining/CETIM/Galling_2025/stream_data/pkl/" # for local computing
Scattering_coef_path = "/home/delaselt/Documents/Acoustic_mining/CETIM/Galling_2025/scattering_coefficients/"
# -----------------------------------------------------------
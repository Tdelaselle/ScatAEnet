# -------------------------------------------- filepaths and parameters
data_file = "Stream_7075_APT_0.1_1_211_ch1_0-100.pkl"

fig_path = "/home/delaselt/Documents/Acoustic_mining/Fatigue_INSA/7075_APT_0.1_1/UMAP_med_2-11/" # for local computing
data_param = "Parametric_data/Param_data_assembly/Param_7075_APT_0.1_1_211_0-100.pkl"     # Folder and file (without extension) containing the parametric data (for any channels)

# model_file = "network_win_0.01_samp_10.0_1o_541_2o_1311.pkl"
model_file = "network_win_0.02_samp_2.0_1o_541_2o_1311.pkl"
pooling = "max" # pooling method to use (avg, max, or med). Use max for high sensibility to short attack and transient phenomena (hits detection), med for general continuous clustering 

DIRPATH = "data/Fatigue_INSA/streams_assembly/" # for local computing
# DIRPATH = "/data/failles/delaselt/continuous_AE_data/" # for OAR computing 
Scattering_coef_path = "Scattering_coefficients/"
# -----------------------------------------------------------
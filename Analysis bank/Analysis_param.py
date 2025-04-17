# -------------------------------------------- filepaths and parameters
data_file = "Stream_Gplusplus_pions38_186MPa_0_cut.pkl"

fig_path = "/home/delaselt/Documents/Acoustic_mining/Fatigue_INSA/7075_APT_0.1_1/UMAP_max_2/"
data_param = "Parametric_data/Param_data_assembly/Param_7075_PT_0.1_2_2_0-200.pkl"     # Folder and file (without extension) containing the parametric data (for any channels)

# model_file = "network_win_0.01_samp_10.0_1o_541_2o_1311.pkl"
model_file = "network_win_0.01_samp_5.0_1o_541_2o_1311.pkl"
pooling = "med" # pooling method to use (avg, max, or med). Use max for high sensibility to short attack and transient phenomena (hits detection), med for general continuous clustering 

DIRPATH = "data/Cetim_Galling/" # for local computing
# DIRPATH = "/data/failles/delaselt/continuous_AE_data/" # for OAR computing 
Scattering_coef_path = "Scattering_coefficients/"
# -----------------------------------------------------------
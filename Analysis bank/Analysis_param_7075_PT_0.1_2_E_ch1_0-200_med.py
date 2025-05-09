# -------------------------------------------- filepaths and parameters
data_file = "Stream_7075_PT_0.1_2_E_ch1_0-200.pkl"
DIRPATH = "data/Fatigue_INSA/" # for local computing
# DIRPATH = "/data/failles/delaselt/continuous_AE_data/" # for OAR computing 
data_param = "Parametric_data/Param_data_assembly/Param_7075_APT_0.1_1_11_0-100"     # Folder and file (without extension) containing the parametric data (for any channels)
model_file = "network_win_0.02_samp_2.0_1o_541_2o_1311.pkl"
pooling = "med" # pooling method to use (avg, max, or med). Use max for high sensibility to short attack and transient phenomena (hits detection), med for general continuous clustering 
Scattering_coef_path = "Scattering_coefficients/"
# -----------------------------------------------------------
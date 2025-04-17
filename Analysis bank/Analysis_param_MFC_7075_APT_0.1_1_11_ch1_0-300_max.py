# -------------------------------------------- filepaths and parameters
data_file = "Stream_7075_APT_0.1_1_11_ch1_0-300.pkl"
DIRPATH = "data/Fatigue_INSA/" # for local computing
# DIRPATH = "/data/failles/delaselt/continuous_AE_data/" # for OAR computing 
data_param = "Parametric_data/Param_data_assembly/Param__APT_0.1_1_11_ch1_0-300"     # Folder and file (without extension)
model_file = "network_win_0.0019_samp_2.0_1o_421_2o_1035.pkl"
pooling = "max" # pooling method to use (avg, max, or med). Use max for high sensibility to short attack and transient phenomena (hits detection), med for general continuous clustering 
Scattering_coef_path = "Scattering_coefficients/"
# -----------------------------------------------------------

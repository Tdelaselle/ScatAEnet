# -------------------------------------------- filepaths and parameters
data_file = "Stream_CT_mart-H-1_N1_ch4.pkl"
DIRPATH = "data/CT_martensite_hydrogren/streams_assembly/" # for local computing
# DIRPATH = "/data/failles/delaselt/continuous_AE_data/" # for OAR computing 
data_param = "Parametric_data/MFC_7075T6-APT-1"     # Folder and file (without extension)
model_file = "network_win_0.001_samp_2.0_1o_461_2o_511.pkl"
pooling = "med" # pooling method to use (avg, max, or med). Use max for high sensibility to short attack and transient phenomena (hits detection), med for general continuous clustering 
Scattering_coef_path = "Scattering_coefficients/"
# -----------------------------------------------------------

# -------------------------------------------- filepaths and parameters
# data_file = "Stream_7075_APT_0.1_1_2_ch3_0-250.pkl" # experiment 2, record 2, ch3
# data_file = "Stream_7075_APT_0.1_1_2_ch2_0-250.pkl" # experiment 2, record 2, ch2
data_file = "Stream_7075_APT_0.1_1_2_ch1_0-250.pkl" # experiment 2, record 2, ch1
# data_file = "Stream_7075_APT_0.1_1_1_ch1_0-229.pkl" # experiment 2, record 1, ch1
# data_file = "Stream_7075_PT_0.1_2_1_ch1_0-150.pkl" # experiment 1, record 1, ch1
fig_path = ""
data_param = "parametric_data/Param_7075_APT_0.1_1_2_0-250.pkl"  # Folder and file (without extension) containing the parametric data (for any channels)

model_file = "network_win_0.04_samp_2.0_1o_541_2o_1521.pkl"
pooling = "max" # pooling method to use (avg, max, or med). Use max for high sensibility to short attack and transient phenomena (hits detection), med for general continuous clustering 
downsampling = 1 # downsampling factor for the network (default is 2, i.e. no downsampling)
arg_pool = False # if True, returns the argmax of the pooling operation)

DIRPATH = "data/" # for local computing
Scattering_coef_path = "scattering_coefficients/"
# -----------------------------------------------------------
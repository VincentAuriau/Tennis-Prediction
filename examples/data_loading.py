import os, sys

sys.path.append("../python")
sys.path.append("../")

from data.data_loader import matches_data_loader

data_df  = matches_data_loader(path_to_data="../submodules/tennis_atp",
                               path_to_cache="../cache")

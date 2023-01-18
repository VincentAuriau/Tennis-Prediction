import os, sys

sys.path.append("../python")
sys.path.append("../")

from data.data_loader import matches_data_loader

data_df = matches_data_loader(path_to_data="../submodules/tennis_atp",
                               path_to_cache="../cache",
                              flush_cache=True,
                              keep_values_from_year=2000)

print(data_df.head())
print(data_df.shape)

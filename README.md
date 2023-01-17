Tennis-Prediction Repository

The goal of this project is to predict the outcome of a tennis match using the data of both players.
The data used comes from https://github.com/JeffSackmann.

To clone the repository, with the data you need to also clone the submodules:
git clone --recurse-submodules https://github.com/VincentAuriau/Tennis-Prediction.git

You can find examples in /examples:
	- loading players statistics at match time + match outcome

		from data.data_loader import matches_data_loader
		data_df = matches_data_loader(path_to_data="submodules/tennis_atp")


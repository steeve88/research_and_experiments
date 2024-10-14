import pandas as pd
# Select the temperature variable (make sure to replace 't2m' with the correct variable name if different in your file)
temperature_var = 't2m'  # Adjust this if the variable name is different in your dataset
z = 'z'
dp_var = 'd2m'
# Latitude and longitude of interest
latitude = 47.37
longitude = 8.55


class Era5Processing():

    def get_era5_parameter(ds, parameter, latitude, longitude):

        nearest_point = ds.sel(latitude=latitude, longitude=longitude, method='nearest')

        location_timeseries = nearest_point[parameter]
        location_timeseries_df = location_timeseries.to_dataframe(name=parameter)

        if parameter == 't2m' or parameter == 'd2m':
            location_timeseries_df[parameter] = location_timeseries_df[parameter]-273.14

        location_timeseries_df.reset_index(inplace=True)
        location_timeseries_df = location_timeseries_df.apply(pd.to_numeric, errors='coerce')

        location_timeseries_df['valid_time'] = pd.to_datetime(location_timeseries_df['valid_time'])

        return location_timeseries_df










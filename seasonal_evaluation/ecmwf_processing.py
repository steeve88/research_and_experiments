import pandas as pd
import xarray as xr

class EcmwfProcessing:
    def get_meteo_parameter(file_path, parameter, latitude, longitude):

        ds = xr.open_dataset(file_path, decode_times=False)
        location_series = ds[parameter].sel(latitude=latitude, longitude=longitude, method='nearest')
        latitude = location_series.latitude.item()
        longitude = location_series.longitude.item()

        ecmwf_seasonal_series_df = location_series.to_dataframe(name=parameter)
        ecmwf_seasonal_series_df=ecmwf_seasonal_series_df.drop(['longitude', 'latitude'], axis=1)
        location_series = ds[parameter].sel(latitude=latitude, longitude=longitude, method='nearest')

        ecmwf_seasonal_series_df = location_series.to_dataframe(name=parameter).reset_index()
        
        ecmwf_seasonal_series_df['forecast_reference_time'] = pd.to_datetime(ecmwf_seasonal_series_df['forecast_reference_time'], unit='s')
        ecmwf_seasonal_series_df['forecast_period_time'] = ecmwf_seasonal_series_df['forecast_reference_time'] + pd.to_timedelta(ecmwf_seasonal_series_df['forecast_period'], unit='h')
        ecmwf_seasonal_series_df['forecast_period_time'] = pd.to_datetime(ecmwf_seasonal_series_df['forecast_period_time'])
        ecmwf_seasonal_series_df['date'] = ecmwf_seasonal_series_df['forecast_period_time'].dt.date

        if parameter == 't2m' or parameter == 'd2m':
            ecmwf_seasonal_series_df[parameter] = ecmwf_seasonal_series_df[parameter] - 273.14

        #Get the number of ensembles and the initialisation time of the run
        ensemble_members_count = ecmwf_seasonal_series_df['number'].max() - ecmwf_seasonal_series_df['number'].min() + 1
        initialisation_date = ecmwf_seasonal_series_df['forecast_reference_time'][0]

        return ecmwf_seasonal_series_df, ensemble_members_count, initialisation_date


    def get_orography(topo_path, parameter, latitude, longitude):

        ds_topo = xr.open_dataset(topo_path, decode_times=False)
        location_series_topo = ds_topo[parameter].sel(latitude=latitude, longitude=longitude, method='nearest')
        df_location_topo = location_series_topo.to_dataframe(name=parameter)

        altitude_ecmwf = df_location_topo[parameter].iloc[0] /9.81

        return altitude_ecmwf


    def ecmwf_daily_percentiles(ecmwf_seasonal_series_df):

        daily_means = ecmwf_seasonal_series_df.groupby(['date', 'number'])['t2m'].mean().reset_index()
        percentiles = [0.05, 0.20, 0.50, 0.70, 0.95]
        ecmwf_seasonal_series_df_daily = daily_means.groupby('date')['t2m'].describe(percentiles=percentiles)
        ecmwf_seasonal_series_df_daily = ecmwf_seasonal_series_df_daily.loc[:, ['50%', '5%', '20%', '70%', '95%']]
        ecmwf_seasonal_series_df_daily.columns = ['median', '5th_percentile', '20th_percentile', '70th_percentile', '95th_percentile']

        return daily_means, ecmwf_seasonal_series_df_daily
    

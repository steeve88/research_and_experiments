
import pandas as pd
import xarray as xr
import yaml

from ecmwf_seasonal_api_downloader import ECMWFDownloader
from era5_download_api_downloader import ERA5Downloader
from file_unifier import NCUnifier
from meteo_calculations import MeteoCalculations
from ecmwf_processing import EcmwfProcessing
from era5_processing import Era5Processing
from probabilistic_evaluation import ProbabilisticEvaluation
from plotter import Plotter


#Inputs from yaml
with open('inputs.yaml', 'r') as file:
    config = yaml.safe_load(file)

ecmwf_seasonal_nc_path = config['file_paths']['ecmwf_seasonal_nc_path']
ecmwf_seasonal_nc_topo_path = config['file_paths']['ecmwf_seasonal_nc_topo_path']
era5_seasonal_nc_path = config['file_paths']['era5_seasonal_nc_path']

zip_dir = config['download_paths']['zip_dir']
save_path_ecmwf_orography = config['download_paths']['save_path_ecmwf_orography']
save_path_ecmwf_zips = config['download_paths']['save_path_ecmwf_zips']
save_path_era5 = config['download_paths']['save_path_era5']

latitude = config['target_coordinates']['latitude']
longitude = config['target_coordinates']['longitude']
parameter = config['target_coordinates']['parameter']
orography_parameter = config['target_coordinates']['orography_parameter']
valid_range_brier = config['target_coordinates']['valid_range_brier']



#Downloading the data !Future work: pass the data directly to production
#ECMWFDownloader.seasonal_dowloader(save_path_ecmwf_zips)
#ECMWFDownloader.seasonal_orography_downloader(save_path_ecmwf_orography)
#NCUnifier.nc_unifier(save_path_ecmwf_zips)
#ERA5Downloader.era5_dowloader(save_path_era5)

#Reading ECMWF Data
ecmwf_seasonal_series_df, ensemble_members_count, initialisation_date = EcmwfProcessing.get_meteo_parameter(ecmwf_seasonal_nc_path, parameter, latitude, longitude)
ecmwf_altitude = EcmwfProcessing.get_orography(ecmwf_seasonal_nc_topo_path, orography_parameter, latitude, longitude)
daily_means, ecmwf_seasonal_series_df_daily = EcmwfProcessing.ecmwf_daily_percentiles(ecmwf_seasonal_series_df)

#Reading ERA5 Data
ds = xr.open_dataset(era5_seasonal_nc_path)
era5_t2m = Era5Processing.get_era5_parameter(ds, parameter, latitude, longitude)
era5_d2m = Era5Processing.get_era5_parameter(ds, 'd2m', latitude, longitude)
era5_altitude = Era5Processing.get_era5_parameter(ds, orography_parameter, latitude, longitude)
era5_altitude = era5_altitude[orography_parameter].values[0]/9.80665

#ERA5 Temperature correction on ECMWF's elevation
t_td_merged = pd.merge(era5_t2m, era5_d2m, on=['valid_time', 'number'])
t_td_merged['rh'] = t_td_merged.apply(MeteoCalculations.rh_calculation, axis=1, t2m_col=parameter, d2m_col='d2m')
t_td_merged['model_altitude'] = era5_altitude
t_td_merged['given_altitude'] = ecmwf_altitude
t_td_merged[f'{parameter}_corrected'] = t_td_merged.apply(MeteoCalculations.temperature_correction, axis=1)
era5_t2m[parameter] = t_td_merged[f'{parameter}_corrected']

#Aggregate ERA5 to daily averages and get probabilistic evaluation
era5_daily_df = era5_t2m.resample('D', on='valid_time').mean().reset_index()
brier_results_df = ProbabilisticEvaluation.brier_score(era5_daily_df, parameter, daily_means, ensemble_members_count, valid_range_brier)

#Plotting daily percentile graph and brier score
Plotter.plotter_percentiles_brier_vs_time(ecmwf_seasonal_series_df_daily, era5_daily_df, brier_results_df, latitude, longitude, ecmwf_altitude, initialisation_date, parameter, 'Temperature at 2m', '[°C]')





































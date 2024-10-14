import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator


class Plotter():
    
    def plotter_percentiles_brier_vs_time(ecmwf_seasonal_series_df_daily, era5_daily_df, brier_results_df, latitude, longitude, ecmwf_altitude, initialisation_date, parameter, parameter_name, parameter_unit):

        ecmwf_seasonal_series_df_daily.index = pd.to_datetime(ecmwf_seasonal_series_df_daily.index)
        brier_results_df['valid_time'] = pd.to_datetime(brier_results_df['valid_time'])


        plt.figure(figsize=(18, 10))
        
        #First plot
        plt.subplot(2, 1, 1)
        plt.fill_between(ecmwf_seasonal_series_df_daily.index,
                        ecmwf_seasonal_series_df_daily['5th_percentile'], 
                        ecmwf_seasonal_series_df_daily['95th_percentile'], 
                        color='lightgrey', alpha=0.5, label='5th-95th Percentile Range')

        plt.plot(ecmwf_seasonal_series_df_daily.index, ecmwf_seasonal_series_df_daily['median'], 
                color='salmon', label='Median', linewidth=2)
        plt.plot(era5_daily_df['valid_time'], era5_daily_df[parameter], 
                color='black', label='ERA5', linewidth=2)

        plt.plot(ecmwf_seasonal_series_df_daily.index, ecmwf_seasonal_series_df_daily['20th_percentile'], 
                color='grey', linestyle='--', linewidth=1)
        plt.plot(ecmwf_seasonal_series_df_daily.index, ecmwf_seasonal_series_df_daily['70th_percentile'], 
                color='grey', linestyle='--', linewidth=1)

        plt.plot([], [], color='grey', linestyle='--', linewidth=1, label='20th-70th Percentile')

        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
        plt.gca().xaxis.set_minor_formatter(plt.NullFormatter())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

        x_min = ecmwf_seasonal_series_df_daily.index.min() - pd.Timedelta(days=0.5)
        x_max = ecmwf_seasonal_series_df_daily.index.max() + pd.Timedelta(days=0.5)

        plt.xlim(x_min, x_max)

        plt.gca().yaxis.set_minor_locator(MultipleLocator(2.5))
        plt.tick_params(axis='y', which='minor', length=4, color='grey')

        plt.grid(which='major', linestyle='-', linewidth=0.7)
        plt.grid(which='minor', linestyle='--', linewidth=0.7)

        plt.gca().set_xticklabels([])

        plt.title(f'ECMWF Seasonal Forecast | Initialised at: {initialisation_date} | Latitude: {latitude}°, Longitude: {longitude}° {parameter_name} Elevation: {ecmwf_altitude} \n {parameter_name} - Daily Means and Percentiles')
        plt.ylabel(f'{parameter_name} {parameter_unit}')

        plt.legend()



        #Second plot
        plt.subplot(2, 1, 2)

        plt.plot(brier_results_df['valid_time'], brier_results_df['brier_score'], color='blue', linewidth=2)
        plt.xlim(x_min, x_max)

        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
        plt.gca().xaxis.set_minor_formatter(plt.NullFormatter())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        
        plt.xticks(rotation=45, ha='right')

        plt.title(f'Daily {parameter_name} - Brier Score')
        plt.ylabel('Brier Score')

        plt.grid(which='major', linestyle='-', linewidth=0.7)
        plt.grid(which='minor', linestyle='--', linewidth=0.7)

        plt.tight_layout()
        plt.savefig('seasonal_ensemble_evaluation_plot.png')
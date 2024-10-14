import os
import zipfile
import xarray as xr
import glob
import numpy as np

class NCUnifier():
    def merge_datasets(datasets):
        merged = datasets[0]
        for ds in datasets[1:]:
            merged = xr.merge([merged, ds], compat='override')
        return merged
    
    def nc_unifier(zip_dir):

        #Unzip files
        for file in os.listdir(zip_dir):
            if file.endswith('.zip'):
                with zipfile.ZipFile(os.path.join(zip_dir, file), 'r') as zip_ref:
                    zip_ref.extractall(os.path.join(zip_dir, file[:-4]))
                os.remove(os.path.join(zip_dir, file))

        #Merge NetCDF files
        for folder in os.listdir(zip_dir):
            folder_path = os.path.join(zip_dir, folder)
            if os.path.isdir(folder_path):
                nc_files = glob.glob(os.path.join(folder_path, '*.nc'))
                if nc_files:
                    datasets = [xr.open_dataset(nc_file) for nc_file in nc_files]
                    merged_ds = NCUnifier.merge_datasets(datasets)

                    if 'forecast_reference_time' in merged_ds.variables:
                        forecast_reference_time = merged_ds['forecast_reference_time'].values[0]

                        if isinstance(forecast_reference_time, np.datetime64):
                            forecast_reference_time = forecast_reference_time.astype('datetime64[D]').item()

                        output_filename = f"{forecast_reference_time}.nc"
                        output_path = os.path.join(folder_path, output_filename)

                        merged_ds.to_netcdf(output_path)

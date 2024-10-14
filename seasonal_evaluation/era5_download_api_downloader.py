import cdsapi

class ERA5Downloader():
    def era5_dowloader(save_path):
        dataset = "reanalysis-era5-single-levels"
        request = {
            "product_type": ["reanalysis"],
            "variable": [
                "2m_temperature",
                "geopotential",
                "2m_dewpoint_temperature"
            ],
            "year": ["2024"],
            "month": [
                "04", "05", "06",
                "07", "08", "09",
                "10"
            ],
            "day": [
                "01", "02", "03",
                "04", "05", "06",
                "07", "08", "09",
                "10", "11", "12",
                "13", "14", "15",
                "16", "17", "18",
                "19", "20", "21",
                "22", "23", "24",
                "25", "26", "27",
                "28", "29", "30",
                "31"
            ],
            "time": [
                "00:00", "06:00", "12:00",
                "18:00"
            ],
            "data_format": "netcdf",
            "download_format": "unarchived",
            "area": [48, 5, 45, 10]
        }

        client = cdsapi.Client()
        client.retrieve(dataset, request).download(save_path)
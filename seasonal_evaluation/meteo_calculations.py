import numpy as np


class MeteoCalculations:

    def rh_calculation(row, t2m_col, d2m_col):
        """Calculates relative humidity from t2m and d2m components.

            Columns "t2m" and "d2m" should be present in the provided dataframe.

        Args:
        ----
            row (pd.Series): A pd.Series object containing columns "t2m" (temperature in K) and "d2m" (dew point in K)

        Returns:
        -------
            float: the calculated relative humidity [in %]
        """

        A = 17.625
        B = 243.04
        t = row[t2m_col]
        td = row[d2m_col]

        numerator = 100 * np.exp((td * A * B) / ((B + t) * (td + B)))
        denominator = np.exp((B * A * t) / ((B + t) * (td + B)))
        return numerator / denominator


    def temperature_correction(row):
        """Calculates relative humidity from t2m and rh components.

            Columns "t2m" and "rh" should be present in the provided dataframe.

        Args:
        ----
            row (pd.Series): A pd.Series object containing columns "t2m" (temperature in K) and "rh" (rh in %)

        Returns:
        -------
            float: the calculated corrected to the altitude temperature [in K]
        """

        #Temperature lapse rates depending on the profile of the atmosphere
        #e.g. https://www.researchgate.net/figure/Dry-98-C-km-and-moist-59-C-km-adiabatic-lapse-rates-give-the-expected-cooling_fig1_284749471
        dry_lapse_rate = -0.0098
        wet_lapse_rate = -0.0059
        mean_lapse_rate = -0.0065

        t = row['t2m']
        RH = row['rh']
        altitude = row['model_altitude']
        given_altitude = row['given_altitude']

        if RH > 90:
            return t + (given_altitude - altitude) * wet_lapse_rate
        elif RH < 30:
            return t + (given_altitude - altitude) * dry_lapse_rate
        else:
            return t + (given_altitude - altitude) * mean_lapse_rate
import pandas as pd

class ProbabilisticEvaluation():
    def brier_score(era5_daily_df, parameter, daily_means, ensemble_members_count, valid_range_brier):

        results = []

        #Counting the percentage of ensembles per day that predicted temperature correctly
        for index, row in era5_daily_df.iterrows():
            valid_time = pd.to_datetime(row['valid_time']).strftime('%Y-%m-%d')
            t2m_value = row[parameter]
            
            lower_bound = t2m_value - valid_range_brier
            upper_bound = t2m_value + valid_range_brier
            
            daily_means['date'] = pd.to_datetime(daily_means['date'])

            daily_means_for_date = daily_means[daily_means['date'] == valid_time]
            
            count_in_range = daily_means_for_date[(daily_means_for_date[parameter] >= lower_bound) &
                                                (daily_means_for_date[parameter] <= upper_bound)]
            
            results.append({'valid_time': valid_time, 'count_in_range': len(count_in_range)})

        results_df = pd.DataFrame(results)
        results_df['precentage_in_range'] = results_df['count_in_range']/ensemble_members_count

        results_df['brier_score'] = (results_df['precentage_in_range'] - 1) ** 2

        return results_df
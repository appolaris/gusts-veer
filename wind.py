import pandas as pd
import numpy as np
import scipy.stats as stats

print("Correlation between changes in speed and direction")
for minspeed in [2]:
    print("Dropping windspeeds below %s" % minspeed)
    for step in [1, 2, 5]:
        print("  %s minute interval:" % step)

        df = pd.read_csv("minute_weather.csv")

        df['delta_id'] = df['rowID'].diff(step)
        df['delta_speed'] = df['avg_wind_speed'].diff(step)
        df['delta_direction'] = df['avg_wind_direction'].diff(step)
        df['delta_direction'] = (df['delta_direction'] + 180) % 360 - 180
        df['same_direction'] = (df['delta_speed']>0) == (df['delta_direction']>0)

        df = df.dropna()

        # exlcude low windspeed observations (in low wind direction may be random)
        df = df[df['min_wind_speed'] >= minspeed]

        # exlcude non-consequtive rows
        df = df[df['delta_id'] == step]

        hitPercent = df['same_direction'].mean() * 100
        correlation = np.corrcoef(df['delta_speed'], df['delta_direction'])[0, 1]
        correlation2, p_value = stats.spearmanr(df['delta_speed'], df['delta_direction'])
        print("    Pearson: ", correlation)
        print("    Spearman: ", correlation2)
        print("    % when Coriolis worked: ", hitPercent)
        del df

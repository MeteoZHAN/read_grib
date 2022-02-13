import xarray as xr
import cfgrib
import meteva.base as meb
import numpy as np
import pandas as pd

if __name__ == '__main__':
    filename = 'adaptor.grib'
    ds = xr.open_dataset(filename, engine='cfgrib')
    print(ds)
    lat = ds['latitude'].data
    lon = ds['longitude'].data
    t = ds['time'].data
    u10 = ds['u10'].data
    v10 = ds['v10'].data
    mlon, mlat = np.meshgrid(lon, lat)
    r = 0
    u_csv = np.zeros([63 * 2160, 8])
    for i, date in enumerate(t):
        u, v = u10[i, :, :], v10[i, :, :]
        year = meb.all_type_time_to_datetime(date).year
        month = meb.all_type_time_to_datetime(date).month
        day = meb.all_type_time_to_datetime(date).day
        hour = meb.all_type_time_to_datetime(date).hour
        for j in range(7):
            for k in range(9):
                u_csv[r, 0], u_csv[r, 1], u_csv[r, 2], u_csv[r, 3], u_csv[r, 4], u_csv[r, 5], u_csv[
                    r, 6], u_csv[r, 7] = year, month, day, hour, mlon[j, k], mlat[j, k], u[j, k], v[j, k]
                r += 1
    df = pd.DataFrame(u_csv, columns=['year', 'month', 'day', 'hour', 'lon', 'lat', 'u10', 'v10'])
    df.to_csv('wind.csv')

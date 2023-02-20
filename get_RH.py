import xarray as xr 
import numpy as np

'''
Calculates relative humidity from temperature 
and dewpoint temperature
RH = e/es * 100
'''

### Calculate saturation vapor pressure
def svp(var):
    svp = 6.112*(np.exp(17.67 * (var - 273.15) / (var - 29.65)))
    return(svp)

### Calculate relative humidity
def get_rh(T,Td):
    e = svp(Td)
    e_s = svp(T)
    return ((e/e_s)*100)

### Derive relative humidity from ERA 2m temperature and
### dewpoint temperature
ds_2t = xr.open_dataset('2t/1950/2t_era5-land_oper_sfc_19500101-19500131.nc')
ds_2d = xr.open_dataset('2d/1950/2d_era5-land_oper_sfc_19500101-19500131.nc')

rh = get_rh(ds_2t['t2m'].values,ds_2d['d2m'].values)

### Convert numpy array to xarray Array
time = ds_2t.time
lat = ds_2t.latitude
lon = ds_2t.longitude

da_rh = xr.DataArray(rh, 
                     dims=ds_2t['t2m'].dims, 
                     coords=ds_2t['t2m'].coords, 
                     attrs={'units': '%', 
                            'long_name' : '2 metre relative humidity'})


### Convert DataArray to DataSet
ds_rh = da_rh.to_dataset(name='rh')

### Sort attributes
ds_rh.time.encoding = {'units': 'hours since 1900-01-01', 
                       'calendar': 'gregorian',
                       'long_name' : 'time'}

### Sort latitude and longitude
ds_rh['latitude'].attrs={'units':'degrees_north', 
                         'long_name':'latitude'}
ds_rh['longitude'].attrs={'units':'degrees_east', 
                          'long_name':'longitude'}

### Save as netCDF
ds_rh.to_netcdf('test.nc',
                encoding={'time':{'dtype': 'double'},
                          'latitude':{'dtype': 'double'},
                          'longitude':{'dtype': 'double'},
                          'rh':{'dtype': 'float32'}})

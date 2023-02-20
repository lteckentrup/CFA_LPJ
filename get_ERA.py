import xarray as xr
import numpy as np
import pandas as pd

### Define leap years, months with 31 and months with 30 days
leap_years = ['1956','1952','1960','1964','1968','1972','1976', 
              '1980','1984','1988','1992','1996','2000','2004',
              '2008','2012','2016','2020']
months_31day = ['01','03','05','07','08','10','12']
months_30day = ['04','06','09','11']

pathwayIN='/g/data/zz93/era5-land/reanalysis/'

def readin_file(var,year,month):
    ### Very clunky sorry
    if month in months_31day:
        suffix = '31.nc'
    elif month in months_30day:
        suffix = '30.nc'
    elif month == '02':
        if year in leap_years:
            suffix = '29.nc'
        else:
            suffix = '28.nc'

    ### Filename
    fileIN = pathwayIN+var+'/'+year+'/'+var+'_era5-land_oper_sfc_'+year+month+'01-'+year+month+suffix
    fileOUT = var+'/'+year+'/'+var+'_era5-land_oper_sfc_'+year+month+'01-'+year+month+suffix
    ds = xr.open_dataset(fileIN, mask_and_scale = True).sel(latitude=slice(-34,-39.5),
                                                            longitude=slice(141,150))
    
    
    ds.to_netcdf(fileOUT)

### Years
years = np.arange(1950,2022,1).astype(str)

### Months
months = np.arange(1,13,1).astype(str)

### Add leading zero
for i in range(0,10):
    months[i] = months[i].zfill(2)

var = 'u10'

### Loop through years and months
for year in years:
    print(year)
    for month in months:
        print(month)
        readin_file(var,year,month)

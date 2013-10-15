# ==============================================================================     
#  HW3: function to call the RGB colomap data from http://geography.uoregon.edu, 
#       and return the number of color (leng) & a colormap dictionary (cdict) 
# ==============================================================================     
#  by InOk Jun
#  OCNG 658, Fall 2013
# ==============================================================================  

# import statement
import netCDF4
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta
from mpl_toolkits.basemap import Basemap


# import netCDF file 
nc_1 = netCDF4.Dataset('Korea_temp.nc')
nc_2 = netCDF4.Dataset('Korea_temp_dt.nc')


#-------------------------------------------------------------------------------
# 1) Make a plan-view in lat-lon using Basemap
#-------------------------------------------------------------------------------
# get the lon-lat-temp data in netCDF (nc_1)
lon   = nc_1.variables['LON'][:]
lat   = nc_1.variables['LAT'][:]
temp  = nc_1.variables['TEMP'][0,0,:,:]

# get the range of map
l_lon = np.min(lon)
u_lon = np.max(lon)
l_lat = np.min(lat)
u_lat = np.max(lat)

# make a plan-view plot using Basemap
m = Basemap(llcrnrlon=l_lon,llcrnrlat=l_lat,urcrnrlon=u_lon,urcrnrlat=u_lat,\
            projection='merc')                
lon, lat = np.meshgrid(lon, lat)            
x, y = m(lon, lat)

# plot and show the result of mapping
fig = plt.figure()
m.fillcontinents()
m.drawcoastlines()
m.drawcountries()
plt.contourf(x, y, temp, np.arange(-5,30,.5), cmap=plt.cm.RdBu_r)
cb = plt.colorbar()
cb.set_label('Temperature (deg C)')
plt.title('Temp Distribution around Korea on 1993/01/01')
plt.show()

# save the figure1
plt.savefig('HW3_by_Jun_netCDF.png', dpi = 600)


#-------------------------------------------------------------------------------
# 2) Make timeseires using Pandas
#-------------------------------------------------------------------------------
# get the temp-time data in netCDF (nc_2)
temp = nc_2.variables['TEMP'][:]
time = nc_2.variables['TIME'][:]
lon  = nc_2.variables['LON1_1'][:]
lat  = nc_2.variables['LAT1_1'][:]

# create the timeseries of data
do = date(1993, 1, 1)
dt = timedelta(days = 1)
dates = np.array([do + n*dt for n in range(len(time))])
temps = np.array([float(temp[n]) for n in range(len(time))])

# make the timeseires using pandas
data = pd.Series(temps, index=dates)
	
# plot the timeseires result
fig, ax = plt.subplots()
ax.plot(data.index, data, 'c')
plt.title('Timeseries of Temperature from NetCDF \n at (lat, lon) = '\
           + '(' + str(float(lat)) + 'N, '+ str(float(lon)) + 'E)')
plt.xlabel('Dates (year)')
plt.ylabel('Temperature (deg C)')
plt.show()

# save the figure2
plt.savefig('HW3_by_Jun_pandas.png', dpi = 600)
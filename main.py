import numpy as np
from netCDF4 import Dataset
import os


output_file = 'avg_data/sgpmetavgE13.b1.20180101.000000.cdf'
n_mins = 5      # number of minutes to average

# variable names change between input and output
old_names = ['atmos_pressure','rh_mean','temp_mean']
new_names = ['atmospheric_pressure','relative_humidity','mean_temperature']


# create new dataset
d_new = Dataset(output_file,'w',format="NETCDF3_CLASSIC")
d_new.createDimension('time')


# initialize variables and copy metadata
print('Copying metadata...')
d_old = Dataset('./input_data/sgpmetE13.b1.20180101.000000.cdf')
for old_name, new_name in zip(old_names,new_names):
    v_old = d_old.variables[old_name]
    v_new = d_new.createVariable(new_name, v_old.datatype, ('time',))
    v_new.setncatts({k: v_old.getncattr(k) for k in v_old.ncattrs()})


# averaging
def get_time_avg(arr,mins=n_mins):
    return np.array([np.average(arr[n:n + mins]) for n in range(0, len(arr), mins)])

# use dummy arrays to store averages before putting into cdf
dummy_arr_dict = {x:np.array([]) for x in new_names}

# loop files
for f in os.listdir('./input_data'):
    if not f.endswith('.cdf'): continue
    print('Computing time-average for '+f)
    f = os.path.join('input_data', f)
    d_old = Dataset(f)
    # loop variables
    for old_name, new_name in zip(old_names,new_names):
        v_old = d_old.variables[old_name][:]
        if len(dummy_arr_dict[new_name]) == 0:
            dummy_arr_dict[new_name] = get_time_avg(v_old)
        else:
            dummy_arr_dict[new_name] += get_time_avg(v_old)

# average over files and assign to Dataset
print('Averaging over files...')
nfiles = 5
for new_name in new_names:
    d_new[new_name][:] = dummy_arr_dict[new_name]/nfiles


d_new.close()

print('Done.')

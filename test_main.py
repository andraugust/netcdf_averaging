import main
import numpy as np
from netCDF4 import Dataset


# check the averaging function
def test_get_time_avg():
    test_arr = np.array([1,1,1,1,1,2,2,2,2,2])
    expected_output = np.array([1,2])
    actual_output = main.get_time_avg(test_arr)
    assert np.array_equal(expected_output,actual_output)

def test_solution():
    # check averaging
    old_name = 'atmos_pressure'
    new_name = 'atmospheric_pressure'

    # compute averages by hand
    x = (main.get_time_avg(Dataset('./input_data/sgpmetE13.b1.20180101.000000.cdf')[old_name][:]) +
         main.get_time_avg(Dataset('./input_data/sgpmetE13.b1.20180102.000000.cdf')[old_name][:]) +
         main.get_time_avg(Dataset('./input_data/sgpmetE13.b1.20180103.000000.cdf')[old_name][:]) +
         main.get_time_avg(Dataset('./input_data/sgpmetE13.b1.20180104.000000.cdf')[old_name][:]) +
         main.get_time_avg(Dataset('./input_data/sgpmetE13.b1.20180105.000000.cdf')[old_name][:]))/5

    # load averages from output file
    y = Dataset('avg_data/sgpmetavgE13.b1.20180101.000000.cdf')[new_name][:]

    # compare
    assert np.array_equal(x,y)

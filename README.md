# Description
This project contains a script for time-averaging data in netcdf files.  Averaging is performed on each netcdf file in `data/` and then the individual file-averages are averaged, creating a final result that's saved in `avg_data/`.

# Requirements
- For running: `netCDF4`
- For testing: `pytest`

# Usage
- Run: `$ python3 main.py`
- Test: `$ python3 -m pytest test_main.py`

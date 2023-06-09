from module import Module
from weather import Weather
from simulate import Simulate


def main():
    # Settings
    day = 365  # Day of the year 1-365 -> 135
    latitude = 53.41  # N 53.38 (Sheffield)
    longitude = -2.96  # E -1.47 (Sheffield)
    module_tilt = 45  # 0 (degrees) = Flat
    module_azimuth = 180  # 0 (degrees) = North, 180 = South
    weather = Weather(cloud_cover=0)  # Cloud cover (0 - 1.0) | 0 = clear, 1.0 = fully overcast

    module = Module(latitude, longitude, module_tilt, module_azimuth)  # Init solar module
    
    # Do simulation
    Simulate.sim_day(day, module, weather)
    Simulate.sim_year(module, weather)
    #Simulate.overcast_vs_sunny(day, module)


if __name__ == '__main__':
    main()

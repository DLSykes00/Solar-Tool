import output
import numpy as np
from weather import Weather


class Simulate:

    @staticmethod
    def sim_day(day, module, weather, plot=True, save=False):  # Simulate energy produced in a day
        assert 1 <= day <= 365, "Day must be 1 - 365"
        print("\n-----------------\nSimulating Day ({0}/365)\n-----------------".format(day))

        cumulative_energy = 0
        minutes_list = []
        module_intensity_list = []

        # Simulate day
        for current_time in range(1, 1441):
            module.calculate_intensity(day, current_time, weather)

            minutes_list.append(current_time)
            module_intensity_list.append(module.intensity)
            cumulative_energy += module.intensity * 60

        print("Theoretical Energy: {:.3g} kJ".format(cumulative_energy))

        if save:
            output.write_to_file("irradiance.csv", minutes_list, module_intensity_list)
        if plot:
            output.plot_2d(module, minutes_list, module_intensity_list)

    @staticmethod
    def sim_year(module, weather, plot=True):  # Simulate energy produced in a full year
        print("\n-----------------\nSimulating Year\n-----------------")
        start_day = 1
        end_day = 365
        no_days = (end_day - start_day) + 1

        cumulative_energy = 0
        minutes_list = np.zeros(1440)
        days_list = np.zeros(no_days)
        module_intensity_list = np.zeros(1440)
        module_intensity_list_2D = np.zeros((no_days, 1440))

        for current_day in range(start_day, end_day + 1):
            days_list[current_day - start_day] = current_day

            for current_time in range(1, 1441):
                module.calculate_intensity(current_day, current_time, weather)

                minutes_list[current_time - 1] = current_time
                module_intensity_list[current_time - 1] = module.intensity
                cumulative_energy += module.intensity * 60

            module_intensity_list_2D[current_day - start_day] = module_intensity_list

        print("Theoretical Energy (Year): {:.3g} kJ".format(cumulative_energy))

        # Show plot
        if plot:
            output.plot_3d(module, minutes_list, days_list, module_intensity_list_2D)

    @staticmethod
    def overcast_vs_sunny(day, module):
        assert 1 <= day <= 365, "Day should be 1 - 365"
        print("\n-----------------\nOvercast vs Sunny\n-----------------")

        # Clear
        weather = Weather(cloud_cover=0)
        cumulative_energy = 0
        minutes_list = []
        module_intensity_list_clear = []
        module_intensity_list_cloudy = []

        for current_time in range(1, 1441):
            module.calculate_intensity(day, current_time, weather)

            minutes_list.append(current_time)
            module_intensity_list_clear.append(module.intensity)
            cumulative_energy += module.intensity * 60

        print("Theoretical Energy (Clear): {:.3g} kJ".format(cumulative_energy))

        # Cloudy
        weather.cloud_cover = 1
        cumulative_energy = 0
        minutes_list = []

        for current_time in range(1, 1441):
            module.calculate_intensity(day, current_time, weather)

            minutes_list.append(current_time)
            module_intensity_list_cloudy.append(module.intensity)
            cumulative_energy += module.intensity * 60

        print("Theoretical Energy (Cloudy): {:.3g} kJ".format(cumulative_energy))
        output.plot_2d(module, minutes_list, [module_intensity_list_clear, module_intensity_list_cloudy],
                       ["Clear", "Cloudy"])

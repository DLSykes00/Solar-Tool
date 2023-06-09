import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def write_to_file(file, x_data, y_data):
    np.savetxt(file, np.transpose([x_data, np.multiply(y_data, 1000)]), delimiter=",", fmt='%i %.1f')


def plot_2d(module, mins, intensity, label=""):
    if isinstance(intensity[0], list):
        assert len(intensity) == len(label), "Must provide a label for each intensity data set"
        for i in range(len(intensity)):
            plt.plot(mins, intensity[i], label=label[i])
    else:
        plt.plot(mins, intensity, label=label)

    plt.xlabel('Time (Hour - UTC)')
    plt.ylabel('Module Intensity (kW/m²)')
    plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
               [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24])
    title_string = "Module Intensity\n\nModule Tilt, Azimuth: {}°, {}°\nLatitude, Longitude: {}, {}".format(
        module.tilt, module.azimuth, module.latitude, module.longitude)
    plt.title(title_string)
    if label != "":
        plt.legend()

    plt.show()


def plot_3d(module, mins_list, days_list, intensity_list_2d):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    X = mins_list
    Y = days_list
    X, Y = np.meshgrid(X, Y)
    Z = intensity_list_2d

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=True)

    # Add a color bar which maps values to colors.
    # fig.colorbar(surf, shrink=0.5, aspect=5)

    # Axis labels
    ax.set_xlabel('Time (Hour - UTC)')
    ax.set_ylabel('Day of Year')
    ax.set_zlabel('Module Intensity (kW/m²)')
    title_string = "Module Intensity Across the Year Under Clear Conditions\n\nModule Tilt, Azimuth: {}°, {}°\nLatitude, Longitude: {}, {}".format(
        module.tilt, module.azimuth, module.latitude, module.longitude)
    ax.title.set_text(title_string)
    plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
               [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24])

    plt.show()

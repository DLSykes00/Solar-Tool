import math
from sun import Sun
from trig import sin_d, cos_d


class Module:
    def __init__(self, latitude, longitude, tilt, azimuth, tracking=0):
        assert -90 <= latitude <= 90, "Latitude must be -90° - 90°"
        assert -180 <= longitude <= 180, "Longitude must be -180° - 180°"
        assert 0 <= tilt <= 90, "Tilt must be 0° - 90°"
        assert 0 <= azimuth <= 360, "Azimuth must be 0° - 360°"
        assert 0 <= tracking <= 2, "Tracking must be 0 (none), 1 (tilt and azimuth), or 2 (azimuth only)"

        self.tracking = tracking  # 0 = no tracking, 1 = dual-axis tracking, 2 = azimuth only
        self.tilt = tilt
        self.azimuth = azimuth
        self.latitude = latitude
        self.longitude = longitude
        self.time_zone = 0  # Using GMT (zulu time)

        self.overcast = 0
        self.cloud_opacity = 0.25
        self.air_mass = 1
        self.albedo = 0.2  # Albedo of ground

        self.direct_irradiance = 0
        self.diffuse_irradiance = 0
        self.cloud_irradiance = 0
        self.reflected_irradiance = 0

        self.intensity = 0  # kW/m², intensity of light incident on solar module

        self.sun = Sun()

    # Find the total intensity of light on the module for given parameters
    def calculate_intensity(self, day, time, weather):
        self.overcast = weather.check_weather()
        self.update_irradiance(day, time)

        if self.tracking == 1:
            self.tilt = self.sun.zenith
            self.azimuth = self.sun.azimuth
        elif self.tracking == 2:
            self.azimuth = self.sun.azimuth

        direct_irradiance_module = self.direct_irradiance * (
                sin_d(self.sun.zenith) * sin_d(self.tilt) * cos_d(self.azimuth - self.sun.azimuth) +
                cos_d(self.sun.zenith) * cos_d(self.tilt))  # Convert to dot product?
        if direct_irradiance_module < 0:  # module intensity may be negative if sun is behind solar panel
            direct_irradiance_module = 0
        diffuse_irradiance_module = self.diffuse_irradiance * ((1 + cos_d(self.tilt)) / 2)
        cloud_irradiance_module = self.cloud_irradiance * ((1 + cos_d(self.tilt)) / 2)
        reflected_irradiance_module = self.reflected_irradiance * ((1 - cos_d(self.tilt)) / 2)

        # Combine module irradiance components
        if self.overcast:
            self.intensity = cloud_irradiance_module * 1 + reflected_irradiance_module
        else:
            self.intensity = direct_irradiance_module + diffuse_irradiance_module + reflected_irradiance_module

    # Calculates the intensity of light for given day/time
    def update_irradiance(self, day, time):
        self.sun.calculate_solar_irradiance(day)
        self.sun.calculate_solar_position(day, time, self.latitude, self.longitude)

        self.calculate_direct_irradiance(self.sun.zenith, self.sun.irradiance)
        self.calculate_diffuse_irradiance()
        self.calculate_cloud_irradiance(self.sun.zenith)
        self.calculate_reflected_irradiance(self.sun.zenith)

    # Calculates direct irradiance on a horizontal plane at the earth's surface
    def calculate_direct_irradiance(self, sun_zenith, solar_irradiance):
        if sun_zenith < 90:
            # approximation for air mass that
            # takes into account curvature of atmosphere
            self.air_mass = 1 / (cos_d(sun_zenith) + 0.50572 * math.pow(96.07995 - sun_zenith, -1.6364))
            self.direct_irradiance = solar_irradiance * math.pow(0.7, math.pow(self.air_mass, 0.678))
        else:
            self.direct_irradiance = 0

    # Estimation of diffuse irradiance on horizontal plane at the earth's surface
    def calculate_diffuse_irradiance(self):
        self.diffuse_irradiance = 0.1 * self.direct_irradiance

    # Estimation of cloud irradiance on horizontal plane (if overcast) at the earth's surface
    def calculate_cloud_irradiance(self, sun_zenith):
        if self.overcast:
            self.cloud_irradiance = self.cloud_opacity * (
                        self.diffuse_irradiance + self.direct_irradiance * cos_d(sun_zenith))
        else:
            self.cloud_irradiance = 0

    # Estimation of reflected irradiance (from the surface of the earth)
    def calculate_reflected_irradiance(self, sun_zenith):
        if self.overcast:
            self.reflected_irradiance = self.albedo * self.cloud_irradiance
        else:
            self.reflected_irradiance = self.albedo * (
                        self.direct_irradiance * cos_d(sun_zenith) + self.diffuse_irradiance)

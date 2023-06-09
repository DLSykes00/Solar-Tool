from trig import sin_d, cos_d, asin_d, acos_d


class Sun:
    def __init__(self):
        self.solar_constant = 1.353  # kW/m², average solar intensity at edge of earth's atmosphere

        # Sun position
        self.elevation = 0.0
        self.zenith = 90.0 - self.elevation  # zenith = 90 - elevation
        self.azimuth = 0.0

        # Irradiance (kW/m²), intensity at the edge of earth's atmosphere taking into account elliptical orbit
        self.irradiance = 0.0

    def calculate_solar_position(self, day, time, latitude, longitude, time_zone=0):
        lstm = 15 * time_zone  # deg
        b = ((360.0 / 365.0) * (day - 81))  # (deg)
        eot = (9.87 * sin_d(2 * b) - 7.53 * cos_d(b) - 1.5 * sin_d(
            b))  # Corrects for orbit eccentricity and axial tilt. (accurate to within 0.5min) (mins)
        tc = ((4.0 * (longitude - lstm)) + eot)  # Time Correction Factor, accounts for longitudinal variations (mins)
        lst = time + tc  # Local Solar Time (12:00 LST = noon)  (mins)
        hra = 15.0 * ((lst / 60.0) - 12)  # Hour angle (deg)
        declination = -23.45 * cos_d((360.0 / 365.0) * (day + 10))  # Declination Angle (deg)
        elevation = asin_d(sin_d(declination) * sin_d(latitude) + cos_d(declination) * cos_d(latitude) * cos_d(hra))
        azimuth = acos_d(
            (sin_d(declination) * cos_d(latitude) - cos_d(declination) * sin_d(latitude) * cos_d(hra)) / (
                cos_d(elevation)))

        self.elevation = elevation
        self.zenith = 90 - elevation
        self.azimuth = azimuth

    def calculate_solar_irradiance(self, day):
        # Calculate solar irradiance (at edge of atmosphere) taking into account elliptical orbit of earth.
        self.irradiance = self.solar_constant * (1 + 0.033 * cos_d((360 * (day - 2)) / 365.0))

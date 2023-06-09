import random
# Not completely accurate for low cloud_cover as diffuse_intensity is currently
# reduced by cloud opacity even coming from areas without cloud cover


class Weather:
    def __init__(self, cloud_cover, cloud_opacity=0.25):
        assert 0 <= cloud_cover <= 1, "Cloud cover must be 0 - 1"
        assert 0 <= cloud_opacity <= 1, "Cloud opacity must be 0 - 1"

        self.cloud_cover = cloud_cover
        self.cloud_opacity = cloud_opacity
        self.air_mass = 1

        rand = random.uniform(0, 1)
        if rand < self.cloud_cover:
            self.overcast = 1
        else:
            self.overcast = 0

    def check_weather(self):  # Flip between overcast and clear according to cloud_cover.
        rand1 = random.uniform(0, 1)
        rand2 = random.uniform(0, 1)  # Used to make it more likely to stay cloudy/clear if it's already cloudy/clear.

        if self.overcast == 1:
            if rand1 > self.cloud_cover and rand2 > 0.5:
                self.overcast = 0
        else:
            if rand1 < self.cloud_cover and rand2 > 0.5:
                self.overcast = 1

        return self.overcast

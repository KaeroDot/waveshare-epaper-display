import logging
from weather_providers.base_provider import BaseWeatherProvider


class MetNo(BaseWeatherProvider):
    def __init__(self, metno_self_id, location_lat, location_long, units):
        self.metno_self_id = metno_self_id
        self.location_lat = location_lat
        self.location_long = location_long
        self.units = units

    # Map Met.no icons to local icons
    # Reference: https://api.met.no/weatherapi/weathericon/2.0/documentation
    def get_icon_from_metno_weathercode(self, weathercode, is_daytime):

        icon_dict = {
                        "clearsky": "clear_sky_day" if is_daytime else "clearnight",
                        "cloudy": "mostly_cloudy" if is_daytime else "mostly_cloudy_night",
                        "fair": "scattered_clouds" if is_daytime else "partlycloudynight",
                        "fog": "climacell_fog",
                        "heavyrain": "climacell_rain_heavy" if is_daytime else "rain_night_heavy",
                        "heavyrainandthunder": "thundershower_rain",
                        "heavyrainshowers": "climacell_rain_heavy" if is_daytime else "rain_night_heavy",
                        "heavyrainshowersandthunder": "thundershower_rain",
                        "heavysleet": "sleet",
                        "heavysleetandthunder": "sleet",
                        "heavysleetshowers": "sleet",
                        "heavysleetshowersandthunder": "sleet",
                        "heavysnow": "snow",
                        "heavysnowandthunder": "snow",
                        "heavysnowshowers": "snow",
                        "heavysnowshowersandthunder": "snow",
                        "lightrain": "climacell_rain_light" if is_daytime else "rain_night_light",
                        "lightrainandthunder": "climacell_rain_light" if is_daytime else "rain_night_light",
                        "lightrainshowers": "climacell_rain_light" if is_daytime else "rain_night_light",
                        "lightrainshowersandthunder": "climacell_rain_light" if is_daytime else "rain_night_light",
                        "lightsleet": "sleet",
                        "lightsleetandthunder": "sleet",
                        "lightsleetshowers": "sleet",
                        "lightsnow": "climacell_snow_light",
                        "lightsnowandthunder": "climacell_snow_light",
                        "lightsnowshowers": "climacell_snow_light",
                        "lightssleetshowersandthunder": "climacell_snow_light",
                        "lightssnowshowersandthunder": "climacell_snow_light",
                        "partlycloudy": "few_clouds" if is_daytime else "partlycloudynight",
                        "rain": "climacell_rain" if is_daytime else "rain_night",
                        "rainandthunder": "thundershower_rain",
                        "rainshowers": "climacell_rain" if is_daytime else "rain_night",
                        "rainshowersandthunder": "thundershower_rain",
                        "sleet": "sleet",
                        "sleetandthunder": "thundershower_rain",
                        "sleetshowers": "sleet",
                        "sleetshowersandthunder": "thundershower_rain",
                        "snow": "snow",
                        "snowandthunder": "snow",
                        "snowshowers": "snow",
                        "snowshowersandthunder": "snow"
                    }

        icon = icon_dict[weathercode]
        logging.debug(
            "get_icon_by_weathercode({}, {}) - {}"
            .format(weathercode, is_daytime, icon))

        return icon

    def get_description_from_metno_weathercode(self, weathercode):
        description_dict = {
                            #  "clearsky":	"Clear sky",
                            "clearsky":	"jasno",
                            #  "cloudy":	"Cloudy",
                            "cloudy":	"oblačno",
                            #  "fair":	"Fair",
                            "fair":	"skoro jasno",
                            #  "fog":	"Fog",
                            "fog":	"mlha",
                            #  "heavyrain":	"Heavy rain",
                            "heavyrain":	"silný déšť",
                            # "heavyrainandthunder":	"Heavy rain and thunder",
                            "heavyrainandthunder":	"silný déšť, bouřka",
                            # "heavyrainshowers":	"Heavy rain showers",
                            "heavyrainshowers":	"silný déšť, přeháňky",
                            # "heavyrainshowersandthunder":	"Heavy rain showers and thunder",
                            "heavyrainshowersandthunder":	"silný déšť, přeháňky, bouřka",
                            # "heavysleet":	"Heavy sleet",
                            "heavysleet":	"silné mrholení",
                            # "heavysleetandthunder":	"Heavy sleet and thunder",
                            "heavysleetandthunder":	"silné mrholení, bouřka",
                            # "heavysleetshowers":	"Heavy sleet showers",
                            "heavysleetshowers":	"silné mrholení, přeháňky",
                            # "heavysleetshowersandthunder":	"Heavy sleet showers and thunder",
                            "heavysleetshowersandthunder":	"silné mrholení, přeháňky, bouřka",
                            # "heavysnow":	"Heavy snow",
                            "heavysnow":	"silné sněžení",
                            # "heavysnowandthunder":	"Heavy snow and thunder",
                            "heavysnowandthunder":	"silné sněžení, bouřka",
                            # "heavysnowshowers":	"Heavy snow showers",
                            "heavysnowshowers":	"silné sněžení, přeháňky",
                            # "heavysnowshowersandthunder":	"Heavy snow showers and thunder",
                            "heavysnowshowersandthunder":	"silné sněžení, přeháňky, bouřka",
                            # "lightrain":	"Light rain",
                            "lightrain":	"lehký déšť",
                            # "lightrainandthunder":	"Light rain and thunder",
                            "lightrainandthunder":	"lehký déšť, bouřka",
                            # "lightrainshowers":	"Light rain showers",
                            "lightrainshowers":	"lehký déšť, přeháňky",
                            # "lightrainshowersandthunder":	"Light rain showers and thunder",
                            "lightrainshowersandthunder":	"lehký déšť, přeháňky, bouřka",
                            # "lightsleet":	"Light sleet",
                            "lightsleet":	"lehké mrholení",
                            # "lightsleetandthunder":	"Light sleet and thunder",
                            "lightsleetandthunder":	"lehké mrholení, bouřka",
                            # "lightsleetshowers":	"Light sleet showers",
                            "lightsleetshowers":	"lehké mrholení, přeháňky",
                            # "lightsnow":	"Light snow",
                            "lightsnow":	"lehké sněžení",
                            # "lightsnowandthunder":	"Light snow and thunder",
                            "lightsnowandthunder":	"lehké sněžení, bouřka",
                            # "lightsnowshowers":	"Light snow showers",
                            "lightsnowshowers":	"lehké sněžení, přeháňky",
                            # "lightssleetshowersandthunder":	"Light sleet showers and thunder",
                            "lightssleetshowersandthunder":	"lehké mrholení, přeháňky, bouřka",
                            # "lightssnowshowersandthunder":	"Light snow showers and thunder",
                            "lightssnowshowersandthunder":	"lehké sněžení, přeháňky, bouřka",
                            # "partlycloudy":	"Partly cloudy",
                            "partlycloudy":	"polojasno",
                            # "rain":	"Rain",
                            "rain":	"déšť",
                            # "rainandthunder":	"Rain and thunder",
                            "rainandthunder":	"déšť, bouřka",
                            # "rainshowers":	"Rain showers",
                            "rainshowers":	"přeháňky",
                            # "rainshowersandthunder":	"Rain showers and thunder",
                            "rainshowersandthunder":	"přeháňky, bouřka",
                            # "sleet":	"Sleet",
                            "sleet":	"mrholení",
                            # "sleetandthunder":	"Sleet and thunder",
                            "sleetandthunder":	"mrholení, bouřka",
                            # "sleetshowers":	"Sleet showers",
                            "sleetshowers":	"mrholení, přeháňky",
                            # "sleetshowersandthunder":	"Sleet showers and thunder",
                            "sleetshowersandthunder":	"mrholení, přeháňky, bouřka",
                            # "snow":	"Snow",
                            "snow":	"sněžení",
                            # "snowandthunder":	"Snow and thunder",
                            "snowandthunder":	"sněžení, bouřka",
                            # "snowshowers":	"Snow showers",
                            "snowshowers":	"sněhové přeháňky",
                            # "snowshowersandthunder":	"Snow showers and thunder",
                            "snowshowersandthunder":	"sněhové přeháňky, bouřka",
                        }

        description = description_dict[weathercode]

        logging.debug(
            "get_description_by_weathercode({}) - {}"
            .format(weathercode, description))

        return description

    # Get weather from Met.no API
    # https://api.met.no/weatherapi/locationforecast/2.0/documentation#!/data/get_complete
    # Met.no API only provides min/max temperatures and codes in 6 hour slots.
    # It would take more complex logic to walk through the forecast and get the weather code, min and max for the day.
    def get_weather(self):

        url = ("https://api.met.no/weatherapi/locationforecast/2.0/complete.json?lat={}&lon={}"
               .format(self.location_lat, self.location_long))

        headers = {"User-Agent": self.metno_self_id}

        response_data = self.get_response_json(url, headers=headers)
        logging.debug(response_data)
        weather_data = response_data["properties"]["timeseries"][0]["data"]
        logging.debug("get_weather() - {}".format(weather_data))

        # Remove the _night or _day suffix from Met.no symbol code, so we can do some mapping.
        weather_code = weather_data["next_6_hours"]["summary"]["symbol_code"].replace("_day", "").replace("_night", "")
        daytime = self.is_daytime(self.location_lat, self.location_long)

        # { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
        weather = {}
        weather["temperatureMin"] = weather_data["next_6_hours"]["details"]["air_temperature_min"]
        weather["temperatureMax"] = weather_data["next_6_hours"]["details"]["air_temperature_max"]
        weather["temperatureInstant"] = weather_data["instant"]["details"]["air_temperature"]
        weather["humidityInstant"] = weather_data["instant"]["details"]["relative_humidity"]
        weather["pressureInstant"] = weather_data["instant"]["details"]["air_pressure_at_sea_level"]
        weather["precipitation"] = weather_data["next_6_hours"]["details"]["precipitation_amount"]
        weather["icon"] = self.get_icon_from_metno_weathercode(weather_code, daytime)
        weather["description"] = self.get_description_from_metno_weathercode(weather_code)
        logging.debug(weather)
        return weather

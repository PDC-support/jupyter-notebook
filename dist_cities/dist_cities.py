import math

# Class for city/population center

class City(object):

    """The City class contains information of city, including name, latitude
    and longitude"""

    def __init__(self, name, latitude, longitude):

        """Initialize a city with name, latitude and longitude"""

        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):

        """String representation of a city"""

        return "%-20s %8.2f %8.2f" \
                % (self.name, self.latitude, self.longitude)

# Function for computing distance between geographic coordinates
# Arguments: latitudes (lat) and longitudes (lon)

def dist(city_1, city_2):

    """Calculate the distance between two cities"""

    p1 = city_1.latitude / 180.0 * math.pi
    p2 = city_2.latitude / 180.0 * math.pi

    cp1 = math.cos(p1)
    cp2 = math.cos(p2)

    dp = p2 - p1

    dL = (city_2.longitude - city_1.longitude) / 180.0 * math.pi

    a = math.sin(dp/2) **2 + cp1 * cp2 * math.sin(dL/2) **2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    R = 6371 # radius of Earth in km

    return R*c

# Function for reading geographic coordinates of cities/population centers
# Geographic coordinates taken from wikipedia
# https://en.wikipedia.org/wiki/List_of_population_centers_by_latitude

def read_data():

    """Read city data (name, latitude, longitude) from file"""

    f_txt = open("cities.txt", 'r')

    cities = []

    for line in f_txt:

        content = line.split()

        latitude = float(content[0])
        longitude = float(content[1])
        name = " ".join(content[2:])

        cities.append(City(name, latitude, longitude))

    f_txt.close()

    return cities

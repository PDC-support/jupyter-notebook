import math

class City(object):

    """The City class holds information of city, including name, latitude and
    longitude"""

    def __init__(self, name, latitude, longitude):

        """Initialize a city object with name, latitude and longitude"""

        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):

        """String representation of a city"""

        return "% 16s %8.2f %8.2f" \
                % (self.name, self.latitude, self.longitude)

def read_cities():

    """Read city data (name, latitude, longitude) and return a list of
    cities"""

    # Geographic coordinates taken from wikipedia
    # https://en.wikipedia.org/wiki/List_of_population_centers_by_latitude

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

def create_coord_pairs(cities):

    """Create a list of coordinate pairs from a list of cities"""

    coord_pairs = []

    for a in range(len(cities)):
        for b in range(a+1, len(cities)):
            coord_pairs.append((cities[a].latitude, cities[b].latitude,
                                cities[a].longitude, cities[b].longitude))

    return coord_pairs

def calc_dist(coord_pair):

    """Calculate the distance from a coordinate pair (latitude_1, latitude_2,
    longitude_1, longitude_2)"""

    p1 = coord_pair[0] / 180.0 * math.pi
    p2 = coord_pair[1] / 180.0 * math.pi

    cp1 = math.cos(p1)
    cp2 = math.cos(p2)

    dp = p2 - p1

    dL = (coord_pair[2] - coord_pair[3]) / 180.0 * math.pi

    a = math.sin(dp/2) **2 + cp1 * cp2 * math.sin(dL/2) **2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    R = 6371 # radius of Earth in km

    return R*c

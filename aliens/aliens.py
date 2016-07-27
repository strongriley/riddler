# coding=utf8
# %matplotlib inline

import matplotlib.pyplot as plt
from math import acos, sin, cos, pi, atan2, sqrt, pow
from numpy.random import rand

SIMULATIONS_PER_RATIO = 100000 # make this smaller to run faster, larger to be more precise.

# Formulae derived from
# https://en.wikipedia.org/wiki/Great-circle_distance
# and http://www.movable-type.co.uk/scripts/latlong.html

class Point(object):
    # Both defined in radians
    lat = 0  # latitude, swing up and down. theta
    lon = 0  # longitudinal angle, swing around. lambda

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        
    def central_angle_to(self, point):
        """
        Returns the size of the angle between this
        point and the given point.
        """
        return acos(
            sin(self.lat)*sin(point.lat)+
            cos(self.lat)*cos(point.lat)*cos(abs(self.lon-point.lon)))
    
    def midpoint(self, point):
        """
        Returns Point() that sits equally between this
        point and the given point in radians.
        """
        bx = cos(point.lat)*cos(abs(self.lon-point.lon))
        by = cos(point.lat)*sin(abs(self.lon-point.lon))
        lat_midpoint = atan2(
            sin(self.lat)+sin(point.lat),
            sqrt(pow(cos(self.lat+bx), 2) + pow(by, 2)))
        lon_midpoint = self.lon + atan2(by, cos(self.lat)+bx)
        return Point(lat_midpoint, lon_midpoint)
    
    def get_lat_pi(self):
        return "%sπ" % (self.lat / pi)
    
    def get_lon_pi(self):
        return "%sπ" % (self.lon / pi)
    
    def __repr__(self):
        return "lat: %s, lon: %s" % (self.get_lat_pi(), self.get_lon_pi())
    
def trial(ratio):
    """
    Runs one trial of aliens randomly landing
    and randomly placed patrol.
    Returns True = planet saved, or False, planet not saved.
    """
    def two_random_angles():
        # angles can be from 0 to 2π
        return [i * pi for i in rand(2)]

    alien1 = Point(*two_random_angles())
    alien2 = Point(*two_random_angles())
    patrol = Point(*two_random_angles())
    midpoint = alien1.midpoint(alien2)
    
    # If the distance the patrol car has to travel is less than
    # [ratio] times the distance each alien will travel to the midpoint,
    # then we're saved!
    alien_distance = alien1.central_angle_to(midpoint)
    patrol_distance = patrol.central_angle_to(midpoint)
    return patrol_distance / ratio < alien_distance


def simulation(ratio):
    wins = 0.0
    total = SIMULATIONS_PER_RATIO
    for i in range(total):
        if trial(ratio):
            wins += 1
    return wins / total

ratios = []
percentages = []
for ratio in xrange(1, 21):
    ratios.append(ratio)
    percentages.append(simulation(ratio) * 100)
print percentages[-1]
plt.bar(ratios, percentages, 0.5, color="blue")
plt.show()

def test():
    """
    Used to ensure midpoint & central angle equations are right.
    """
    print "test:"
    zero = Point(0, 0)
    other_side = Point(0, pi)
    dist = zero.central_angle_to(other_side)
    print "distance between: %s pi " % (dist / pi)
    assert(dist == 1*pi)
    midpoint = zero.midpoint(other_side)
    print "midpoint: %s" % midpoint
    assert(midpoint.lat == 0)
    assert(midpoint.lon == 0.5*pi)

    print "test2:"
    top = Point(pi / 2, 0)
    dist = zero.central_angle_to(top)
    print "dist: %sπ" % (dist / pi)
    assert (dist == pi / 2)
    midpoint = zero.midpoint(top)
    print "midpoint: %s" % midpoint
    assert(midpoint.lat == pi / 4)
    assert(midpoint.lon == 0)

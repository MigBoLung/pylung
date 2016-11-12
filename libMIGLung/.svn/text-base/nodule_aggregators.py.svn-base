#nodule_aggregators hierarchy
#nodule_aggregator classes handle the various ways one can choose to test if two nodule classes refer to the same real nodule

import math
    
import lung_nodule

DEFAULT_AGGREGATOR = "CentroidInsideSecondNoduleAggregator()"


class NoduleAggregator(object):
    def __init__(self):
        raise TypeError("You should use a subclass instead")
    
    def areTheSame(self,nodule_a, nodule_b):
        #TODO: checks
        pass

	#TODO: check for an idiom!
    @staticmethod
    def getDefault():
        return getattr(DEFAULT_AGGREGATOR)



#helper functions
def _euclidean_dist3(a,b):
    sumsq = 0
    for i in (0,1,2):
        sumsq += (a[i]-b[i])**2
        distance = math.sqrt(sumsq)
    return distance



#TODO unfinished
#class OverlapNoduleAggregator(NoduleAggregator):
#    #ratio_a and ratio_b are applied to region diameters before overlap
#    #overlap_ratio is based on the second element volume
#    def __init__(self, overlap_ratio, ratio_a = 1., ratio_b = 1.):
#        self.overlap_ratio = overlap_ratio
#        self.ratio_a = ratio_a
#        self.ratio_b = ratio_b
#    
#    #formula from Wolfram's website:
#    #http://mathworld.wolfram.com/Sphere-SphereIntersection.html
#    def areTheSame(self, nodule_a, nodule_b):
#        vol_b = 4/3 * math.pi * ( nodule_b.max_diam * 0.5 ) ** 3
#        
#       
#    #alternatively, do it using bboxes



class FixedDistanceNoduleAggregator(NoduleAggregator):
    def __init__(self, distance, distance_func = _euclidean_dist3):
        self.distance = distance
        self.distance_func = distance_func
    
    def areTheSame(self, nodule_a, nodule_b):
        return self.distance_func(
            nodule_a.centroid_zpos(), nodule_b.centroid_zpos()) < self.distance
    
#Bad name, but i want to make shure we check if the centroid of the first nodule is
#inside the second nodule    
class CentroidInsideSecondNoduleAggregator(NoduleAggregator):
    def __init__(self, pad = 0, ratio = 1., distance_func = _euclidean_dist3):
        self.pad = pad
        self.ratio = ratio
        self.distance_func = distance_func

    def areTheSame(self,nodule_a, nodule_b):
        distance = self.distance_func(nodule_a.centroid_zpos(), nodule_b.centroid_zpos())
        return (distance < (nodule_b.get_max_diameter() * 0.5 * self.ratio + self.pad))






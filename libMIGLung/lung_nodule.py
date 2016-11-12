# Nodule class library: handles nodule informations, and TAG I/O
#
#
# support for LIDC characteristics is included
#
# Author: Gianluca Ferri <g.ferri@unibo.it>
# 2010


##########################################################
# CLASS DEFINITIONS
##########################################################
class NoduleTag(object):
    def __init__(self,
                 centroid_x = 0,
                 centroid_y = 0,
                 scan_idx = 0,
                 zpos = 0,
                 min_diameter = 0,
                 max_diameter = 0):
        self.centroid_x = int(centroid_x)
        self.centroid_y = int(centroid_y)
        self.scan_idx = int(scan_idx)
        self.zpos = float(zpos)
        self.min_diameter = float(min_diameter)
        self.max_diameter = float(max_diameter)

    def __repr__(self):
        outstr = "<NoduleTag centroid_x = %d, centroid_y = %d, " + \
                  "scan_idx = %d, zpos = %f, min_diameter = %f, " + \
                  "max_diameter = %f>"
        return outstr % \
                (self.centroid_x,
                self.centroid_y,
                self.scan_idx,
                self.zpos,
                self.min_diameter,
                self.max_diameter)                
        



########## NODULE BASE CLASS ##########
#
# handles 2d tag list as centroid,diameter 
# and a 3d tag, which can be set or computed from
# the 2d tags
#
# TODO: add creation of 2d tags from a set 3d tag


class Nodule(object):
    def __init__(self):
        self.__tags = []
        self.__3dtag = []
  
    def addTag(self, tag):
        self.__tags.append(tag)

    def replaceTags(self, tags):
        self.__tags = tags

    def popTags(self):
        ret = self.__tags
        self.__tags = []
        return ret

    def set3DTag(self,tag):
        self.__3dtag = tag

    def compute3DTagFrom2DTags(self):

        self.__3dtag = NoduleTag()
        
        if len(self.__tags) == 0:
            return
            
        tags = self.__tags
        (x,y,idx_z,zpos) = (0.,0.,0.,0.)
        (min_diam,max_diam) = (0.,0.)
        i = 0
        for tag in tags:
            i +=1
            x += tag.centroid_x
            y += tag.centroid_y
            idx_z += tag.scan_idx
            zpos += tag.zpos
            if tag.min_diameter > min_diam:
                min_diam = tag.min_diameter
            if tag.max_diameter > max_diam:
                max_diam = tag.max_diameter

        self.__3dtag.centroid_x = int(round(x / i))
        self.__3dtag.centroid_y = int(round(y / i))
        self.__3dtag.scan_idx = int(round(idx_z / i))
        self.__3dtag.zpos = zpos / i

        self.__3dtag.min_diameter = min_diam
        self.__3dtag.max_diameter = max_diam
       
    def print2DTags(self):
        outstr = ""
        for tag in self.__tags:
            outstr = outstr + str(tag) + "\n"
        return outstr

    def MIGTAGString(self):
        outstr = ""
        sortedtags = sorted(self.__tags, self._compareby_scan_idx)
        for tag in sortedtags:
            newrow = "%d %d %d %f %f \n" % (tag.scan_idx, tag.centroid_x, tag.centroid_y, tag.min_diameter, tag.max_diameter)
            outstr = outstr + newrow
        return outstr
    
    #returns coords of 3d centroid with zpos as z coord
    def centroid_zpos(self):
        return (self.__3dtag.centroid_x,self.__3dtag.centroid_y, self.__3dtag.zpos)

    #returns coords of 3d centroid with scan_idx as z coord
    def centroid_scanidx(self):
        return (self.__3dtag.centroid_x,self.__3dtag.centroid_y, self.__3dtag.scan_idx)
    
    def get_max_diameter(self):
        return (self.__3dtag.max_diameter)

    def update_z_idx(self,scan_lookup):
        for tag in self.__tags:
            z_multiplied = int(round(tag.zpos * 100));
            tag.scan_idx = scan_lookup[z_multiplied]
        
    def n2DTags(self):
        return len(self.__tags)
    

    def isTheSameAs(self, nodb, noduleAggregator = None):
        if not noduleAggregator:
            noduleAggregator = NoduleAggregator.getDefault()

        return noduleAggregator.areTheSame(self,nodb)

    #local functions
    @classmethod
    def _compareby_scan_idx(cls,a,b):
        return a.scan_idx - b.scan_idx       
    

    def __repr__(self):
        return "<Nodule: %s>" % self.__3dtag


##########################################################################

########## LIDC Nodule ###############
# adds informations from LIDC XML
#
# TODO: add infos on boundaries
# TODO: handle nonnodules
# TODO: handle little nodules
# TODO: handle agreement levels
######################################

class LIDCNodule(Nodule):
    
    CHARACTERISTICS_FIELDS = ["texture","malignancy","subtlety","internalStructure","calcification","sphericity","margin","lobulation","spiculation"];
    
    def __init__(self):
        Nodule.__init__()

        self.characteristics = {};
        #these fields contain LIDC nodule evaluation statistics
        for characteristic in CHARACTERISTICS_FIELDS:
            self.characteristics[characteristic] = None    
        
    #join extract mean values from all readers dicts
    def joindicts(self, nodlist):
        countdict = {}
        valuedict = nodlist[0].characteristics
        for (key,value) in valuedict.items():
            if value:
                countdict[key] = 1
        for nod in nodlist[1:]:
            thisdict = nod.characteristics
            for (key,value) in thisdict.items():
                if value:
                    if (key in valuedict) & valuedict[key]:
                        countdict[key] += 1
                        valuedict[key] += value
                    else: 
                        countdict[key] = 1
                        valuedict[key] = value
        
        #now compute means
        for (key,value) in valuedict.items():
            if value:
                valuedict[key] = float(value) / countdict[key]

        #finally assign dict
        self.characteristics = valuedict

    def characteristics_string(self):
        return repr(self.characteristics) + "\n"

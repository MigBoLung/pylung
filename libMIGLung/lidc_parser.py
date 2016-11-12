# LIDC xml file parser
#
#
# Author: Gianluca Ferri <g.ferri@unibo.it>
# 2010

import lung_nodule
from xml.etree.ElementTree import ElementTree

LIDC_NS = "{http://www.nih.gov}"


########################################################################
#   READ XML: find lists of nodules
# returns a tuple containing  (nodules_osl,nodules_usl,nonnodules)
# nodules_osl: nodules with edge maps (diam > 3mm)
# nodules_usl: nodules without edge maps (diam < 3mm)
# nonnodules: nonnodules
########################################################################

def read_xml(in_fname):
    tree = ElementTree()
    tree.parse(in_fname)

    readdata = []

    readingSessions = tree.getiterator(LIDC_NS + "readingSession")  # Returns list of all readingSessions
    for reader in readingSessions: # Iterates through all found readingSessions
        nonnodules = reader.findall( LIDC_NS + "nonNodule")
        allnodules = reader.getiterator(LIDC_NS + "unblindedReadNodule")
        nodules_usl = [];
        nodules_osl = [];
        for nodule in allnodules:
            edgemaps = nodule.findall(LIDC_NS + "roi/" + LIDC_NS + "edgeMap")
            if len(edgemaps) <= 1: #only one edgemap => nodule < 3mm
                nodules_usl.append(nodule)
            else:
                nodules_osl.append(nodule)

        #now we have 3 lists for: nodules >3mm, nodules<3mm, nonnodules
        if VERBOSE:        
            for nodule in nodules_usl:
                print nodule
            print "------------------------------------------------------"
            for nodule in nodules_osl:
                print nodule
            print "------------------------------------------------------"
            for nodule in nonnodules:
                print nodule

        readdata.append((nodules_osl,nodules_usl,nonnodules))
    return readdata




#############################################################################
#    
#  CALCULATION OF CENTROIDS AND DIAMETERS FOR EACH NODULE
#  EXTRACTION OF CHARACTERISTICS
#
#############################################################################

def extract_infos_from_readxml (readdata):        
    allcompnodules = []
    for (nodules_osl, nodules_usl, nonnodules) in readdata:
        compnodules = []
        for nodule in nodules_osl:
            compnodule = lung_nodule.LIDCNodule()
            rois = nodule.getiterator(LIDC_NS + "roi")
            nodule_zposlist = []
            for roi in rois:
                #take only inclusion tags
                if roi.find(LIDC_NS + "inclusion").text == "FALSE":
                    continue

                #GET Z position        
                zpos = float(roi.find(LIDC_NS + "imageZposition").text)
                zpos_multi = int(round(zpos * 100))

                #get only the first included roi for each z position
                #TODO: find a better strategy, it would be better to add xelems and yelems instead
                if zpos_multi in nodule_zposlist:
                    continue
                else:
                    nodule_zposlist.append(zpos_multi)

                
                #compute centroids
                xelems = roi.findall(LIDC_NS + "edgeMap/" + LIDC_NS + "xCoord")
                int_xelems = [int(elem.text) for elem in xelems]
                cen_x = int(round(cen_func(int_xelems))) + START_IDX

                yelems = roi.findall(LIDC_NS + "edgeMap/" + LIDC_NS + "yCoord")
                int_yelems = [int(elem.text) for elem in yelems]
                cen_y = int(round(cen_func(int_yelems))) + START_IDX
                
                # DIAMETER BASED ON BOUNDING BOX #TODO: try better strategies
                min_x = min(int_xelems)
                max_x = max(int_xelems)
                diam_x = max_x - min_x
                min_y = min(int_yelems)
                max_y = max(int_yelems)
                diam_y = max_y - min_y
                diam = max(diam_x,diam_y)
                
                newTag = NoduleTag(cen_x, cen_y, 0, zpos, diam, diam)
                
                compnodule.addTag(newTag)

            compnodule.compute3DTagFrom2DTags()           
            
            #enter in characteristics and fill in compnodule with LIDC stats
            characteristicselem = nodule.find(LIDC_NS + "characteristics")
            if characteristicselem:
                for characteristic in compnodule.characteristics.keys():
                    try:
                         temp = int(characteristicselem.find(LIDC_NS + characteristic).text)
                    except:
                        temp = None
                    finally:
                        compnodule.characteristics[characteristic] = temp


            compnodules.append(compnodule)
        allcompnodules.append(compnodules)
    return allcompnodules

#!/usr/bin/env python

# LIDC IMPORTER SCRIPT
#
# Converts LIDC-style annotation in simple MIG GT Tag form
# It also extracts LIDC characteristics
#
# Author: Gianluca Ferri <g.ferri@unibo.it>
#

#TODO: handle command line

############### IMPORTS ########################
import math
import dicom
import os
import numpy
import sys

############## PARAMS ###########################

DIRLIST_PATH = "dirlist"

OUT_DIR = "GT_computed_new"
OUT_DIR_CHARACTERISTICS = "GT_computed_new_characteristics"

#centroid calculation params
cen_func = numpy.median  #function to use to compute centroids

#reader joining params
MIN_DIST = 10
MIN_INSTANCES = 4

# coordinate starting number (whether to use tags in matlab (1) or C (0)
START_IDX = 1


#resize params
RESIZE = True
RESIZE_MM = 0.6

VERBOSE = False

out_fname_postfix = ".txt"


### local imports ####
from libMIGlung import lung_nodule, lidc_parser

############## FUNCTIONS #################################################

#############################################################
#JOIN THE LISTS for 4 readers based on distance
##############################################################

def euclidean_dist3(a,b):
    sumsq = 0
    for i in (0,1,2):
        sumsq += (a[i]-b[i])**2
        distance = math.sqrt(sumsq)
    return distance

def join_lists (allcompnodules, min_dist, dist3):

    joinedcompnodules = []
    all_list = []
    for compnodules in allcompnodules:
        for compnodule in compnodules:
            all_list.append(compnodule)
            
    while len(all_list) > 0:
        nod_a = all_list.pop()
        count = 1
        morituri = []
        for nod_b in all_list:
            if dist3(nod_a.centroid_zpos(), nod_b.centroid_zpos()) < min_dist:
                count +=1
                morituri.append(nod_b)
        
        #extract mean values from all dicts
        allneighbors = [nod_a]
        allneighbors.extend(morituri)        
        nod_a.joindicts(allneighbors)        
        
        for item in morituri:
            all_list.remove(item)
        if count >= MIN_INSTANCES:
            joinedcompnodules.append(nod_a)

    return joinedcompnodules


###############################################################
#compute z_index
#compute z_res and z indexes lookup 
###############################################################
def compute_z_idx(dicom_dir, start_idx):
    zposlist = []
    instance_lookup = {}
    
    for dicomfile in os.listdir(dicom_dir):
        filepath = os.path.join(dicom_dir,dicomfile)
        try:
            scan = dicom.read_file(filepath,"50")
        except:
            #print "skipped " + dicomfile
            continue
        dicom_z_pos = scan.ImagePositionPatient[2]
        zposlist.append(dicom_z_pos)

        dicom_z_pos_multi = int(round(dicom_z_pos * 100)) #MULTIPLIED BY 100!

        instance_lookup[scan.InstanceNumber] = dicom_z_pos_multi

    scan_lookup = {}
    for index, instance_number in enumerate(sorted(instance_lookup.keys())):
        scan_lookup[instance_lookup[instance_number]] = index + start_idx
    
    zetas = sorted(zposlist)
    z_min = zetas[0]
    z_max = zetas[-1]
    z_length = z_max - z_min
    differences = [zetas[i+1] - zetas[i] for i in range(len(zetas)-1)]
    min_diff_z = min(differences)
    max_diff_z = max(differences)
    orig_z_res = numpy.median(differences)
    if VERBOSE:
        print "computed orig_z_res = %f" % orig_z_res

    return (scan_lookup, orig_z_res, z_length, z_min, z_max)


###############################################################
#ADJUST VALUES WITH RESIZE
###############################################################
def adjust_resize(joinedcompnodules, scan_lookup, orig_z_res, z_length, z_min, z_max, resize_mm):

    margin_mm = orig_z_res / 2 ;
    #marginslices = max(int(round(margin_mm)) - 1,0)

    #TODO:HERE IT WOULD BE SAFER TO USE THE NUMBER OF SCANS IN THE RESIZED DIRECTORY
    nscans = int(round(z_length / resize_mm))
    #check order of instances 
    keys = scan_lookup.keys() 
    if scan_lookup[min(keys)] < scan_lookup[max(keys)]:
        z_list = [i * resize_mm + z_min for i in range(nscans)];
    else:
        z_list = [z_max - i * resize_mm for i in range(nscans)];

    #create resized nodules
    resizednodules = joinedcompnodules[:]
    for nodule in resizednodules:
        oldtags = nodule.popTags()
        oldtagzetas = sorted([tag.zpos for tag in oldtags])

                             
        for idx_newz in range(len(z_list)):
            newz = z_list[idx_newz]
            if newz >= (oldtagzetas[0]-margin_mm) and newz <= (oldtagzetas[-1]+margin_mm):
                #take the nearest tag with the current z and current index
                #TODO: linear interpolation has a lot more sense
                tag_to_use = None
                min_value = 1000              
                for tag in oldtags:
                    zdiff = abs(tag.zpos - newz)
                    if zdiff < min_value:
                        tag_to_use = tag
                        min_value = zdiff
                    
                newtag = lung_nodule.NoduleTag(tag_to_use.centroid_x, tag_to_use.centroid_y,
                                   idx_newz + START_IDX, newz,
                                   tag_to_use.min_diameter, tag_to_use.max_diameter)                   
                nodule.addTag(newtag)


###########################################################
#         WRITE TAGS
###########################################################

    ##NB: nodules with 0 tags already handled  TODO: where?
def write_MIG_tags(fname, joinedcompnodules):    
    outfile = open(fname,'w+')
    outfile.write(str(len(joinedcompnodules))+"\n")
    i = 0
    if len(joinedcompnodules) > 0:
        for nodule in joinedcompnodules:
            i += 1
            outfile.write(str(i)+"\n")
            outfile.write(str(nodule.n2DTags())+"\n")
            outfile.write(nodule.MIGTAGString())

    outfile.close()

def write_LIDC_characteristics(fname, joinedcompnodules):
    out_fullpath = os.path.join(OUT_DIR_CHARACTERISTICS, out_fname)
    outfile = open(out_fullpath,'w+')
    outfile.write(str(len(joinedcompnodules))+"\n")
    i = 0
    if len(joinedcompnodules) > 0:
        for nodule in joinedcompnodules:
            i += 1
            outfile.write(str(i)+"\n")
            #outfile.write("%d %d %d\n" % nodule.centroid_scanidx)
            outfile.write(nodule.characteristics_string())
    outfile.close()


########################## MAIN PROGRAM #################################


# LOOP THROUGH DIRECTORIES IN DIRLIST

if os.path.exists(OUT_DIR):
    print("WARNING: output directory exists, script will overwrite old GTs")
else:
    os.mkdir(OUT_DIR)

if os.path.exists(OUT_DIR_CHARACTERISTICS):
    print("WARNING: characteristics output directory exists, script will overwrite old files")
else:
    os.mkdir(OUT_DIR_CHARACTERISTICS)



#TODO: evitare di doversi creare prima dirlist
#creata da fuori con
# $ls -d 1.3*/*/* > dirlist
    
dirlist_file = open(DIRLIST_PATH)
idir = 0
for line in dirlist_file:
    #dicom_dir = line[:-2]
    idir+=1
    dicom_dir = line.strip()
    print "processing dir %03d : %s" % (idir,dicom_dir)
    filenames = os.listdir(dicom_dir)
    try:
        in_fname = os.path.join(dicom_dir,
		[a for a in filenames if a.endswith(".xml")][0])
    except:
        print "unable to load xml file for dir: %s\n" % dicom_dir
        continue
    
    try:
        #   READ XML
        readdata = lidc_parser.read_xml(in_fname)
       
        #  CALCULATION OF CENTROIDS AND DIAMETERS FOR EACH NODULE, AND ADD FIELDS
        allcompnodules = lidc_parser.extract_infos_from_read_xml(readdata)

        # join the lists
        dist3 = euclidean_dist3
        joinedcompnodules = join_lists (allcompnodules, MIN_DIST, dist3)

        (scan_lookup, orig_z_res, z_length, z_min, z_max) = compute_z_idx(dicom_dir,START_IDX)
    
        if not RESIZE:
            for nodule in joinedcompnodules:
                nodule.update_z_idx(scan_lookup)

        else:
            adjust_resize(joinedcompnodules, scan_lookup, orig_z_res, z_length, z_min, z_max, RESIZE_MM)
    except:
        print "error: ",sys.exc_info() 
        print "writing empty file for dir:  %s\n" % dicom_dir
        joinedcompnodules = []
    

    #load dicom
    for dicomfile in os.listdir(dicom_dir):
        filepath = os.path.join(dicom_dir,dicomfile)
        try:
            scan = dicom.read_file(filepath,"50")
            break
        except:
            #print "skipped " + dicomfile
            pass 
    
    #write tags
    out_fname = '_'.join([scan.PatientID,scan.StudyInstanceUID,scan.SeriesInstanceUID])
    out_fname += out_fname_postfix
    
    out_fullpath = os.path.join(OUT_DIR, out_fname);
    write_MIG_tags(out_fullpath, joinedcompnodules);

    out_fullpath = os.path.join(OUT_DIR_CHARACTERISTICS, out_fname);
    write_LIDC_characteristics (out_fullpath, joinedcompnodules);    

#cleanup and exit
dirlist_file.close()

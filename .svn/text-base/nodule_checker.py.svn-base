#!/usr/bin/env python

# Takes CAD tags and GTs and checks for statistics
# TODO: per adesso facciamo che prende i file tag, poi ci aggiungiamo l'handling dei lidc
#
#
# Author: Gianluca Ferri <g.ferri@unibo.it>
#


#TODO: portare dentro la lib in modo che poi dando dir diverse possiamo chiamare questo come
#funzione in un programma piu' ampio

#TODO: handle non isotropic data


import sys,os

### local imports ####
import libMIGLung.lung_nodule as lung_nodule
import libMIGLung.tagfile_reader as tagfile_reader
import libMIGLung.nodule_aggregators as nodule_aggregators

verbose = True

def usage():
    print "usage: nodule_checker.py cad_output_dir gt_dir [fnames_list]"


if (len(sys.argv) < 3 or len(sys.argv) > 4):
    usage()
    sys.exit(-1)

#cad_output_dir = "/media/PACKARDBELL/MIG/trabajo/data/results_fold2_testweight_1to8/results_fold2_fpr2_testweight/w0_0_147/"
#gt_dir = "/media/DATI/data_cad2d/LIDC_NEW/firstgroup_20091001/GT_all_noresize/GT_min4/"
cad_output_dir = sys.argv[1]
gt_dir = sys.argv[2]

if len(sys.argv) == 4:
    fnames_list_fname = sys.argv[3]
else:
    fnames_list_fname = "";

#se viene data una lista di file esegue il check solo su quelli, altrimenti lo fa su tutti
if fnames_list_fname:
    fnames_file = open(fnames_list_fname)
    fnames = fnames_file.read(fnames_file).splitlines()
else:
    fnames = os.listdir(gt_dir)


taken_gt_nodules_dict = {}
false_positives_dict = {}
positives_CAD_regs_dict = {}

TP = 0;
FP = 0;
n_GT_nodules = 0;
npat = 0

cadfnames = os.listdir(cad_output_dir)
gtfnames  = os.listdir(gt_dir)

for fname_base in fnames:
    
    #parse tagfiles 

    #remove extensions if any TODO: find a better way to extract extension (unfortunately we must cope with dots inside filename)
    fname_base = fname_base[:-4]

    #Read tagfiles
    try:
        fname = [name for name in cadfnames if (
            name.startswith(fname_base) and name.endswith(".tag")
            and (name.find("_res.tag") == -1))]
        if (len(fname) == 0):
            continue
        fname = fname[0]
        cadnodules = tagfile_reader.parse(os.path.join(cad_output_dir, fname))
    except IOError:
        print "Error reading CAD output tag file: " + fname
        continue
    try:
        fname = [name for name in fnames if name.startswith(fname_base)][0]
        gtnodules = tagfile_reader.parse(os.path.join(gt_dir, fname))
    except IOError:
        print "Error reading GT tag file: " + fname
        continue

    npat +=1
    nnodules_curpat= len(gtnodules)
    n_GT_nodules += nnodules_curpat
    
    
    if verbose:
        print "\nChecking file: %s" % fname
        print "Nodules in this patient: %d" % nnodules_curpat
    
    #set inclusion policy (optional, by default it uses CentroidInsideSecondNoduleAggregator())
    #nodule_aggregator = nodule_aggregators.FixedDistanceNoduleAggregator(4)
    nodule_aggregator = nodule_aggregators.CentroidInsideSecondNoduleAggregator()
    #check
    not_matched_nodules = cadnodules[:]
    taken_gt_nodules = []
    true_positives = []

    for gtnod in gtnodules:
        alreadymatched = False
        for cadnod in cadnodules:
            if cadnod.isTheSameAs(gtnod, nodule_aggregator):
                if (not alreadymatched):
				    taken_gt_nodules.append(gtnod)
				    true_positives.append(cadnod)
				    alreadymatched = True
                try:
                    not_matched_nodules.remove(cadnod)
                except:
                    print "WARNING: trying to remove already removed element in not_matched_nodules"
    
    #update dictionaries and sums
    taken_gt_nodules_dict[fname] = taken_gt_nodules
    false_positives_dict[fname] = not_matched_nodules
    positives_CAD_regs_dict[fname] = true_positives

    if verbose and len(taken_gt_nodules) > 0:
        print "Matched %d nodules!" % len (taken_gt_nodules)
        print "GT DATA:"
        print taken_gt_nodules
        print "CAD_DATA:"
        print true_positives

    localTP = len(taken_gt_nodules)
    if nnodules_curpat:
        localTPF = float(localTP) / nnodules_curpat
    #print localTPF

    TP += localTP
    
    FP += len(not_matched_nodules)

#obtain overall performance rating
TPF = float(TP) / n_GT_nodules
FPperPat = float(FP) / npat

print "\nNODULE CHECK RESULTS"
print "nodules in GT = %d; npat = %d; TP = %d;  TPF = %f; FP/Pat %f;" \
        % (n_GT_nodules, npat, TP, TPF, FPperPat)


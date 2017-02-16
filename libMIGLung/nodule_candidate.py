##################################################### 
# Nodule candidate handling
#
# Author: Gianluca Ferri <glferri@gmail.com>
# 2017

from lung_nodule import NoduleTag

class NoduleCandidate3d:

    def __init__(self, noduletag, features ):
        self.noduletag = noduletag 
        self.features = features

    def __repr__(self):
        return "<NoduleCandidate3d: %s>" % self.noduleTag

class SeriesCandidates:
    def __init__(self, info, patient_id, series_id, feature_names):
        self.info = info
        self.patient_id = patient_id
        self.series_id = series_id
        self.feature_names = feature_names
        self.candidates = []


    def addCandidate(self, nodulecandidate):
        self.candidates.append(nodulecandidate)
   
    
        

class SeriesCandidatesWithLabels:
    def __init__(self, info, patient_id, series_id), feature_names:
        SeriesCandidates.__init__(info, patient_id, series_id, feature_names)
        self.labels = []

    def addCandidate(self, nodulecandidate, label):
        addCandidate(self, nodulecandidate)
        self.labels.append(label)


def writeCandidatesToCSV(series_candidates, output_file):
    bool has_labels = type(series_candidates) is SeriesCandidatesWithLabels 
    with open(fname,'w+') as outfile:
        outfile.write("info: %s\n" % (series_candidates.info))
        outfile.write("patient_id: %s\n" % (series_candidates.patient_id))
        outfile.write("series_id: %s\n\n" % (series_candidates.series_id))
        head = "scan_idx,centroid_x,centroid_y,min_diameter,max_diameter,"
        head += self.feature_names.join(',')
        if has_labels:
            head += ",label"
        head += "\n"    
        outfile.write(head)
        for idx,candidate in enumerate(series_candidates):
            nt = candidate.nodultag
            outfile.write((nt.scan_idx, nt.centroid_x, nt.centroid_y,
                nt.min_diameter, nt.max_diameter).join(',') + ',')
            outfile.write(candidate.features.join(','))
            
            if has_labels:
                outfile.write(',' + series_candidates.labels[idx])

            oufile.write('\n')

def parseCandidatesCSV(input_file):
    bool has_labels = False
    with open(fname, 'r') as infile:
        line = infile.readline()
        if(!line.startswith("info:")):
            raise ValueError("incorrect file format")
        info = line.split(": ")[1]
        line = infile.readline()
        patient_id = line.split(": ")[1]
        line = infile.readline()
        series_id = line.split(": ")[1]
        head = infile.readline()
        
        series_candidates = None
        allfeatnames = head.split(",");

        if head.endswith("label"):
            has_labels = True
            series_candidates = SeriesCandidatesWithLabels(info, patient_id, series_id, allfeatnames[5:-1])
        else:
            series_candidates = SeriesCandidates(info, patient_id,series_id, allfeatnames[5:])
        

        while (line = infile.read()):
            if line.strip() == "":
                continue
            row = line.split(",");
            noduletag = NoduleTag(row[1],row[2],row[0], 0,row[3],row[4])
            if has_labels:
                nodulecandidate = NoduleCandidate3d( noduletag , row[5:-1])
                series_candidates.addCandidate(nodulecandidate, row[-1])
            else:
                series_candidates.addCandidate(nodulecandidate)

        return series_candidates


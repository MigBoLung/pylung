# MIG CAD tag reader
#
#
# Author: Gianluca Ferri <g.ferri@unibo.it>
# 2010

#TODO: anche questo farlo come gerarchia, prendi un file, tira fuori una lista di nodules
#possiamo sfruttare comunque il duck typing
import lung_nodule

def parse(in_fname):
    tagfile = open(in_fname)
    nnodules = 0;
    inod = 0;
    ntags = 0;
    itag = 0;

    nodules = []
    #state machine like reading
    
    state = 0 #initial state
    
    for line in tagfile:
        if line.startswith('#'):
            pass
        try:
            if (state == 0): #number of nodules
                nnodules = int(line.strip())
                state = 1;
            elif (state == 1): #nodule index
                inod = int(line.strip())
                if inod > nnodules:
                    raise IOError("Number of nodules is not consistent in file " + in_fname)
                state = 2;
            elif (state == 2): #number of tags
                ntags = int(line.strip());
                itag = 0;
                nodule = lung_nodule.Nodule()
                state = 3;
            elif (state == 3): #tag list
                if itag < ntags:
                    
                    splitted = line.strip().split()
                    #noduletag constructor handles casting
                    #TODO:CONSIDER ZPOS AND IDX!
                    noduletag = lung_nodule.NoduleTag(
                        splitted[1], splitted[2],
                        splitted[0], splitted[0], splitted[3], splitted[4])
                    nodule.addTag(noduletag)

                    itag += 1
                    
                    if itag == ntags:                   
                        nodule.compute3DTagFrom2DTags() #we do that here, maybe it's better to leave it outside
                        nodules.append(nodule)
                        state = 1
            else:
                raise IOError("State error in file " + in_fname)
        except:
            raise IOError("Unknown error in file " + in_fname)

    tagfile.close()
    return nodules




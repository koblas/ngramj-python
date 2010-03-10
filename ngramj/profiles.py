import sys, math, os, codecs
from .ranker import Ranker
from .profile import NGramProfile

class NGramProfiles(object) :
    LOW_STAT_SAFETY = 0.8

    def __init__(self, mode = 1) :
        self.mode      = mode
        self.profiles  = []
        self.allNGrams = set()
        self.myTrie    = None
        self.maxlen    = -1

        self.loadProfile()

    def loadProfile(self, names=None) :
        # load all of the .ngp files for the list of lanuages
        # for every npg file hash into a set the ngrams
        dir = os.path.join(os.path.dirname(__file__), 'languages')
        for file in os.listdir(dir) :
            if file[-4:] != '.ngp' :
                continue
            path = os.path.join(dir, file) 
            with codecs.open(path,'r','utf-8') as fd :
                np = NGramProfile(file[0:-4], fd)
                for ng in np.get_sorted() :
                    self.maxlen = max(self.maxlen, len(ng))
                    self.allNGrams.add(ng)
                self.profiles.append(np)
        self.myTrie = None

    def get_ranker(self) :
        ofd = codecs.open('/dev/stdout','w','utf-8')
        if not self.myTrie :
            ngs = sorted([ng.reversed() for ng in self.allNGrams])
            #self.myTrie = dict([(ng, i) for ng, i in ngs])
            #for n in ngs_r : print >>ofd,"u'%s'" % n
            from chartrie import createTrie
            self.myTrie = createTrie(ngs)
            ngs = [ng[::-1] for ng in ngs]

            vals = []
            for i in range(0, len(ngs)) :
                vals.append([0] * len(self.profiles))
            for k, ngp in enumerate(self.profiles) :
                norm  = [0.0] * (self.maxlen + 1)
                count = [0]   * (self.maxlen + 1)
                for i, ngi in enumerate(ngs) :
                    ng = ngp.get(ngi, None)
                    if ng and ng.count > self.LOW_STAT_SAFETY :
                        ngl = len(ng)
                        raw1 = float(ng.count) - self.LOW_STAT_SAFETY
                        count[ngl] += 1
                        norm[ngl]  += raw1
                        vals[i][k] = raw1
                        #print "INNER vals[%d][%d] = %f" % (i,k,vals[i][k])
                for i in range(1, self.maxlen+1) :
                    #norm[i] = (norm[i] * (1.0 + float(count[i])) / float(count[i])) + 1.0
                    if count[i] != 0 :
                        norm[i] = (norm[i] * (1.0 + count[i]) / count[i]) + 1.0
                    else :
                        norm[i] = float('nan')
                    #print "NORM[%d] = %r" % (i, norm[i])
                #print '[0][0]',norm
                for i, ngi in enumerate(ngs) :
                    ng = ngp.get(ngi, None)
                    if ng and ng.count > 0 :
                        #print "PRE   norm[%d] = %r   vals[%d][%d] = %f" % (len(ng), norm[len(ng)],i,k,vals[i][k])
                        vals[i][k] /= norm[len(ng)]
                        #print "OUTER norm[%d] = %r   vals[%d][%d] = %f" % (len(ng), norm[len(ng)],i,k,vals[i][k])

            # Horizontal additive zero sum + nonlinear weighting
            for i in range(0, len(ngs)) :
                s = 0.0
                for k in range(0, len(self.profiles)) :
                    #print "vals[%d][%d] = %f" % (i,k,vals[i][k])
                    s += vals[i][k]
                #print "S = ",s
                av = s / len(self.profiles)

                # Assume minimum amount of score for significance.
                # XXX Heuristics for the following contant:
                #    Higher means faster and less noise
                #    Lower means better adaption to mixed language test
                # n = self.mode_trans(av, len(ngs[i])) / av / 100.0 * (-math.log(av))
                #print "AV = ",av
                n = self.mode_trans(av, len(ngs[i])) / av / 40.0
                for k in range(0, len(self.profiles)) :
                    vals[i][k] = (vals[i][k] - av) * n

        return Ranker(self.profiles, self.myTrie, vals)

    def mode_trans(self, x, l) :
        mode = self.mode

        if mode == 10 :
            if l == 1 :
                return x
            f = 1.0 / (l+1)
            return math.pow(x/f, f)
        if mode == 9 or mode == 8:
            f = 1.0 / (l+1)
            return math.pow(x, f) / math.sqrt(f)
        if mode == 7 :
            f = 1.0 / (l+1)
            return math.pow(x, f) / f
        if mode == 6 :
            f = 1.0 / l
            return math.pow(x, f) / math.sqrt(f)
        if mode == 5 :
            f = 1.0 / l
            return math.pow(x, f) / f
        if mode == 4 :
            f = 1.0 / l
            return math.pow(x*f, f)
        if mode == 3 :
            f = 1.0 / l
            return math.pow(x, f)
        if mode == 2 or mode == 1 :
            f = 1.0 / l
            return math.pow(x/f, f)
        return x

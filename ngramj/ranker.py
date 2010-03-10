import math
from .chartrie import BaseTrie

class SimpleRankResult(object) :
    def __init__(self, profiles, scores, inverse=True) :
        self.remain = 0
        self.scores = scores[:]
        self.profs  = [None] * len(scores)
        self.profiles = profiles

        remain = 1.0
        for i in range(0, len(self.scores)) :
            prof = self.profiles[i]
            m = self.scores[i]
            remain -= m
            j = i - 1
            while j >= 0 and inverse ^ (m < self.scores[j]) :
                self.scores[j+1] = self.scores[j]
                self.profs[j+1]  = self.profs[j]
                j -= 1
            self.scores[j+1] = m
            self.profs[j+1]  = prof
        
    def get_profiles(self) :
        return self.profiles

    def get_score(self, pos) :
        if pos == len(self.profs) :
            return self.NOLANGNAME
        if pos < 0 : 
            pos += len(self.profs)
        return self.profs[pos].name

    def results(self) :
        return [(self.profs[i], s) for i, s in enumerate(self.scores)]
            

class Ranker(object) :
    def __init__(self, profiles, myTrie, vals) :
        self.profiles = profiles
        self.myTrie   = myTrie
        self.vals     = vals

        self.reset()
        
    def get_rank_result(self) :
        self.flush()

        s = sum(self.rscore)
        return SimpleRankResult(self.profiles, [v / s for v in self.rscore[0:-1]])

    def reset(self) :
        self.score  = [0.0] * (len(self.profiles) + 1)
        self.rscore = [0.0] * (len(self.profiles) + 1)
        self.rscore[-1] = 0.5

        self.flushed = False

    def flush(self) :
        if self.flushed :
            return
        self.flushed = True

        #print "S:",self.score
        maxval = max(self.score)
        limit  = maxval / 2.0
        #print "score ... ", self.score
        #print "flush = ", maxval, limit
        #f = 1.0 / (float(maxval) - float(limit))
        f = 2.0 / maxval
        for i, v in enumerate(self.score) :
            delta = v - limit
            if delta > 0.0 :
                self.rscore[i] += delta * f
            # We do not reset to zero, this makes classification contextual
            # -aka the next document scored will assume some relation ship to this document
            self.score[i] /= 2.0
        #print "SS:",self.score
        #print "RS:",self.rscore

    def account(self, fd) :
        for line in fd :
            #print line
            for i in range(0, len(line)) :
                self._account(line, i)

    def _account(self, seq, pos) :
        currentNode = self.myTrie
        p2 = pos

        isSeperator = lambda ch : (ch <= ' ' or ch.isspace() or ch.isdigit() or ch in ".!?:,;")

        while currentNode :
            if p2 == -1 :
                ch = ' '
            else :
                ch = seq[p2].lower()
                if isSeperator(ch) :
                    ch = ' '
            t2 = currentNode.subtrie(ch)
            #print "T2 = ", ch, t2
            if t2 is None :
                break
            id = t2.id
            if id != BaseTrie.NO_INDEX :
                self.flushed = False
                for i in range(0, len(self.profiles)) :
                    self.score[i] += self.vals[id][i]
            if p2 == -1 :
                break
            p2 -= 1
            currentNode = t2

        startChar = seq[pos]
        #print "CHAR:",startChar,isSeperator(startChar), self.score

        if isSeperator(startChar) and max(self.score) > 1.0 :
            #print "CALLING FLUSH"
            self.flush()

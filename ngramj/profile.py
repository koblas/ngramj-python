from collections import defaultdict
from .ngram import NGram

class NGramProfile(dict) :
    DEFAULT_MIN_LENGTH = 1
    DEFAULT_MAX_LENGTH = 5
    SEPARATOR = u'_'
    FINISHREAD_STR = u"#END"
    NORMALIZATION_STR = u"ngram_count"

    MODE_NOSINGLEBLANK = 0
    MODE_NOBLANK = 1
    MODE_BLANK = 2

    def __init__(self, name, fd = None) :
        self.name = name
        self.minlen = self.DEFAULT_MIN_LENGTH
        self.maxlen = self.DEFAULT_MAX_LENGTH

        self.clear()

        if fd :
            self.load(fd)

    def set_restricted(self, restricted) :
        self.restricted = restricted

    def analyze(self, text) :
        word = self.SEPARATOR
        for c in text :
            if c.isalpha() :
                word += c
            else :
                self.add_analyzer(word)
                word = word[0:1]
        self.add_analyzer(word)

    def add_analyzer(self, word) :
        word += self.SEPARATOR
        self.add_ngrams(word)

    def clear(self) :   
        super(NGramProfile,self).clear()
        self.normalization = 0
        self._ordered = None
        self._sorted = None

    def get_normalization(self) :
        return self.normalization

    def add_ngrams(self, word) :
        for n in range(self.minlen, self.maxlen) :
            self._add_ngrams(word, n)

    def _add_ngrams(self, word, n) :
        for i in range(0, len(word) - n) :
            cs = word[i:i + n]
            if cs not in nge :
                if self.restricted and nge in self.restricted :
                    continue
                nge = NGram(cs)
                self[cs] = nge
            else :
                nge = self[cs]
            nge.inc()
            self.normalization += 1
        self._sorted = None

    def get_sorted(self) :
        if self._sorted is None :
            self._sorted = sorted(self.values())
        return self._sorted

    #
    #
    #
    def load(self, fd, mode=MODE_NOSINGLEBLANK) :
        self.clear()

        eliminators = u""
        discards = 0
        storeCount = -1
        self.normalzation = 0

        for line in fd :
            line = line.strip()
            if len(line) < 2 :
                continue
            if line[0] == '-' :
                eliminators += line[1]
            elif line.find(self.FINISHREAD_STR) == 0 :
                break
            elif line[0] == '#' :
                continue

            ngram, count = line.split(' ', 1)
            ngram = ngram.replace('_', ' ')
            if mode == self.MODE_NOSINGLEBLANK and ngram == u' ' :
                # Single spaces are so paar as n-grams (1-grams), that we throw them away!!
                continue
            if mode == self.MODE_NOBLANK and ngram.find(' ') != -1 :
                continue
            count = int(count.strip())
            if line.find(self.NORMALIZATION_STR) == 0 :
                storeCount = count
            elif len(ngram) < self.minlen or len(ngram) > self.maxlen :
                continue
            # TODO - eliminiators
            nge = NGram(ngram, count)
            self[ngram] = nge
            self.normalization += count
        if storeCount != -1 and storeCount != self.normalization :
            # ERROR - " WARNING storeCount (%d) != normalzation (%d)" % (storeCount, self.normalization)
            pass
            
    def save(self, fd) :
        fd.write("# NgramProfile generated at ... for Language Identification\n")
        fd.write("%s %s\n" % (self.NORMALIZATION_STR, self.normalization))
        for ng in self.get_sorted() :
            fd.write("%s %d\n" % (ng, ng.get_count()))

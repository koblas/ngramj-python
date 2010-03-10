import sys, codecs
from .profiles import NGramProfiles

def lang2(files) :
    nps = NGramProfiles()
    ranker = nps.get_ranker()
    for textfile in files :
        ranker.reset()
        ranker.account(codecs.open(textfile,'r','utf-8'))
        res = ranker.get_rank_result()
        sys.stdout.write("FILE: %s -- " % textfile)
        for p, s in res.results() :
            sys.stdout.write("%s:%f " % (p.name, s))
        sys.stdout.write("\n")

if __name__ == '__main__' :
    lang2(sys.argv[1:])

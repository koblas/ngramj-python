#
#
#
import codecs
ofd = codecs.open('/dev/stdout','w','utf-8')

class BaseTrie(object) :
    END_CHAR = 0
    NO_INDEX = -1

    def __init__(self) :
        self.left   = None
        self.right  = None
        self.center = None

    def subtrie(self, str) :
        current = self.center
        #print "STR = ", str
        for ch in str :
            #print "CH = ", ch
            if current is None :
                break
            while current :
                splitChar = current.split
                if ch < splitChar :
                    current = current.left
                elif ch > splitChar :
                    current = current.right
                else :
                    # Current is this char...
                    break
        return current

    def get_id(self) :
        return self.NO_INDEX
    id = property(get_id)

    def get_split(self) :
        return self.END_CHAR
    split = property(get_split)

    def dump(self, indent="", w=32767, seq=None) :
        if w < 0 :
            return
        w -= 1
        if self.split == self.END_CHAR :
            print >>ofd, "%s<%s> - %d [%s]" % (indent, self.split, self.id, seq)
        else :
            print >>ofd, "%s<%s> - %d" % (indent, self.split, self.id)
            if self.left   : self.left.dump(indent+"l", w-1, seq)
            if self.center : self.center.dump(indent+" c", w-1, seq)
            if self.right  : self.right.dump(indent+"r", w-1, seq)

#
#
#
class ForwardTree(BaseTrie) :
    def __init__(self, id, split, center) :
        super(ForwardTree, self).__init__()
        self._id     = id
        self._split  = split
        self.center  = center

    def get_id(self) :
        return self._id
    id = property(get_id)

    def get_split(self) :
        return self._split
    split = property(get_split)

#
#
#
class FullTree(ForwardTree) :
    def __init__(self, id, split, left, center, right) :
        super(FullTree, self).__init__(id, split, center)
        self.left  = left
        self.right = right

#
#
#
def createTrie(seqs, pos=0, start=0, end=None) :
    return ForwardTree(BaseTrie.NO_INDEX, BaseTrie.END_CHAR, createTrieInternal(seqs, pos, start, end))

def createTrieInternal(seqs, pos=0, start=0, end=None) :
    if end is None :
        end = len(seqs)
    if start >= end :
        return None
    mid = (start + end) / 2
    #print "CTI ", start, end, mid, pos, seqs[mid][pos]
    split = seqs[mid][pos]
    goRight = mid
    while goRight < end and seqs[goRight][pos] == split :
        goRight += 1
    goLeft = mid
    while goLeft > start and seqs[goLeft-1][pos] == split :
        goLeft -= 1
    goLeft2 = goLeft

    id = BaseTrie.NO_INDEX
    if len(seqs[goLeft]) == pos + 1 :
        id = goLeft
        goLeft2 += 1
    if start < goLeft or goRight < end :
        return FullTree(id, split,
                        createTrieInternal(seqs, pos, start, goLeft),
                        createTrieInternal(seqs, pos+1, goLeft2, goRight),
                        createTrieInternal(seqs, pos, goRight, end))
    return ForwardTree(start, split, createTrieInternal(seqs, pos + 1, goLeft2, goRight))

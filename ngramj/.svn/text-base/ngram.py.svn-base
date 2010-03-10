
class NGram(object) :
    def __init__(self, seq, count=0) :
        self._chars    = u"" or seq
        self._hashCode = None
        self._count    = count

    def _calcHashCode(self) :
        hashCode = 42 + len(self._chars)
        for ch in self._chars :
            hashCode = hashCode * 0x110001 + ord(ch) + 1
        self._hashCode = hashCode

    def __hash__(self) :
        if self._hashCode is None :
            self._calcHashCode()
        return self._hashCode

    def __eq__(self, other) :
        return self._chars == other._chars
    
    def __ne__(self, other) :
        return self._chars != other._chars

    def __str__(self) :
        return self._chars

    def __len__(self) :
        return len(self._chars)

    def __cmp__(self, other) :
        d = other.count - self.count
        if d != 0 :
            return d
        if self._chars == other._chars :
            return 0
        if self._chars < other._chars :
            return -1
        return 1

    def __getitem__(self, key) :
        return NGram(self._chars[key.start:key.stop:key.step])

    def get_count(self) :
        return self._count

    def set_count(self, value) :
        self._count = value

    count = property(get_count, set_count)

    def inc(self) :
        self._count += 1

    def reversed(self) :
        return self._chars[::-1]

if __name__ == '__main__' :
    v = NGram("testing")

    print v[2:4]
    v.inc()

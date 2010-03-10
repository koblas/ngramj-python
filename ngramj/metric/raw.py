def diff(p1, p2) :
    """
      * Raw (Delta-count) based difference between profiles.
      * Calculate a score how well NGramProfiles match each other.
    """

    sum = 0.0

    norm1 = p1.get_normalization()
    norm2 = p2.get_normalization()

    # Treat all NGrams contained in p1
    for ng1 in p1.get_sorted() :
        c1 = float(ng1.getCount()) / norm1
        ng2 = p2.get(ng1, None)
        if ng2 :
            c2 = float(ng2.getCount()) / norm2
            sum += abs(c1 - c2)
        else :
            sum += c1 

    # Treat NGrams contained ONLY in p2
    for ng2 in p2.get_sorted() :
        if ng2 not in p1 :
            c2 = float(ng2.getCount()) / norm2
            sum += c2

    return sum

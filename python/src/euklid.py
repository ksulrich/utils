# http://de.wikipedia.org/wiki/Gr%C3%B6%C3%9Fter_gemeinsamer_Teiler

def euklid(a, b):
    while b != 0:
        a, b = b, a % b
    return a

if __name__ == "__main__":
    import sys
    
    if (len(sys.argv) != 3):
        print("Usage: " + sys.argv[0] + " <number_1> <number_2>")
        print("see http://de.wikipedia.org/wiki/Gr%C3%B6%C3%9Fter_gemeinsamer_Teiler")
        sys.exit(1)

    one = int(sys.argv[1])
    two = int(sys.argv[2])
    print "ggT(%d,%d)=%d" % (one, two, euklid(one, two))
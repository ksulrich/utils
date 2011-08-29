# workaround for HTMLDoc which doesn't like my curly apostrophes
import sys

inputfile = open(sys.argv[1], 'rb')
data = inputfile.read()
inputfile.close()
data = data.replace("&#8217;", "'")
outputfile = open(sys.argv[1], 'wb')
outputfile.write(data)
outputfile.close()

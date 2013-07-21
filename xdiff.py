from optparse import OptionParser
from xdiff_core import Xmldiff


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-o", "--one", dest="file_one")
    parser.add_option("-t", "--two", dest="file_two")

    (options, args) = parser.parse_args()

    xd = Xmldiff()
    xd.readxml(options.file_one, options.file_two)
    xd.xdiff()

from Inquiry import Inquiry
import sys

if __name__ == '__main__':
    try:
        if len(sys.argv) == 7 and sys.argv[1] == '-y' and sys.argv[3] == '-m' and sys.argv[5] == '-d':
                result = Inquiry.get_results_for_day(int(sys.argv[2]), int(sys.argv[4]), int(sys.argv[6]))
                Inquiry.print_result(result)
        elif len(sys.argv) == 5 and sys.argv[1] == '-y' and sys.argv[3] == '-m':
                result = Inquiry.get_results_for_month(int(sys.argv[2]), int(sys.argv[4]))
                Inquiry.print_result(result)
        else:
            print "Usage: Inquiry.py -y year -m month [-d day]"
            sys.exit(0)
    except KeyError or ValueError:
        print "Usage: cli_print_result.py -y year -m month [-d day]"
        sys.exit(0)

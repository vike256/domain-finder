import subprocess
import argparse

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def parse_arguments():
    parser = argparse.ArgumentParser(
         prog='Domain Finder by vike256',
         description='Finds available domains'
    )
    parser.add_argument('-tld', nargs='+', required=False, help='Checks domain availability for TLDs listed')
    parser.add_argument('-name', nargs='+', required=False, help='Checks availability for names listed')
    parser.add_argument('-namefile', nargs=1, required=False, help='Checks availability for names listed in a file')
    parser.add_argument('-tld-max', nargs=1, required=False, help='Defines max length of the TLD')
    parser.print_help()
    return parser.parse_args()
     

def is_domain_available(domain):
      whois = subprocess.run(['whois', domain], stdout=subprocess.PIPE).stdout.decode('utf-8')
      if 'Domain not found' in whois:
            return True
      return False

def main():
    args = parse_arguments()


if __name__ == '__main__':
    main()
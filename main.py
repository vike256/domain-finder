import subprocess
import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='Domain Finder by vike256',
        description='Finds available domains'
    )
    parser.add_argument('-tld', nargs='+', required=False, help='Checks domain availability for TLDs listed')
    parser.add_argument('-name', nargs='+', required=False, help='Checks availability for names listed')
    parser.add_argument('-namefile', nargs=1, required=False, help='Checks availability for names listed in a file')
    parser.add_argument('-tld-max', nargs=1, required=False, help='Defines max length of the TLD')
    return parser.parse_args()
     

def is_domain_available(domain):
    whois = subprocess.run(['whois', domain], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if 'Domain not found' in whois:
        return True
    return False

def main():
    args = parse_arguments()
    names = []
    tlds = []

    if not args.name and not args.namefile:
        print('Please provide -name or -namefile') 
        sys.exit()
    
    if args.name:
        names.extend(args.name)
    
    if args.tld:
        tlds.extend(args.tld)
    else:
        with open('TLDs.txt', 'r') as tlds_file:
            tld_list = tlds_file.read()
            tld_list = tld_list.split()
            for tld in tld_list:
                if args.tld_max:
                    if len(tld) <= args.tld_max:
                        tlds.append(tld)
                else:
                    tlds.append(tld)

    with open('available_domains.txt', 'w') as output_file:
        for name in names:
            for tld in tlds:
                domain = f'{name}.{tld}'
                if is_domain_available(domain):
                    print(f'{domain} is available')
                    output_file.write(f'{domain}\n')
                else:
                    print(f'{domain} is not available')
        print('All available domains saved in available_domains.txt')




if __name__ == '__main__':
    main()
import subprocess
import argparse
import sys
import concurrent.futures
from time import time

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='Domain Finder by vike256',
        description='Finds available domains'
    )
    parser.add_argument('-tld', nargs='+', required=False, help='Checks domain availability for TLDs listed')
    parser.add_argument('-name', nargs='+', required=False, help='Checks availability for names listed')
    parser.add_argument('-namefile', nargs=1, required=False, help='Checks availability for names listed in a file')
    parser.add_argument('-tld-max', nargs=1, required=False, help='Defines max length of the TLD. Doesn\'t affect TLDs added with -tld')
    return parser.parse_args()
     

def is_domain_available(domain):
    whois = subprocess.run(['whois', domain], stdout=subprocess.PIPE).stdout.decode('utf-8').lower()
    if 'not found' in whois:
        return domain, True
    return domain, False


def process_namefile(path):
    try:
        with open(path, 'r') as file:
            namelist = file.read()
            namelist = namelist.split()
            return namelist
    except Exception as e:
        print(f'Error while processing namefile: {e}')
        sys.exit()
        return []


def main():
    start_time = time()
    args = parse_arguments()
    names = []
    tlds = []
    available = []
    checked_count = 0

    if not args.name and not args.namefile:
        print('Please provide -name or -namefile') 
        print('-h for help')
        sys.exit()
    
    if args.name:
        names.extend(args.name)
    
    if args.namefile:
        names.extend(process_namefile(args.namefile[0]))
    
    if args.tld:
        tlds.extend(args.tld)
    else:
        with open('TLDs.txt', 'r') as tlds_file:
            tld_list = tlds_file.read()
            tld_list = tld_list.split()
            for tld in tld_list:
                if args.tld_max:
                    if len(tld) <= int(args.tld_max[0]):
                        tlds.append(tld)
                else:
                    tlds.append(tld)

    with open('available_domains.txt', 'w') as output_file:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for name in names:
                for tld in tlds:
                    futures.append(executor.submit(is_domain_available, f'{name}.{tld}'))
            
            for future in concurrent.futures.as_completed(futures):
                result_domain, result = future.result()
                if result:
                    available.append(result_domain)
                    print(f'{result_domain}, AVAILABLE')
                else:
                    print(f'{result_domain}, not available')
                checked_count += 1
        available.sort()
        output_string = ''.join(f'{d}\n' for d in available)
        output_file.write(output_string)
        found = len(available)
        print(f'Finished in {time() - start_time:.2f} seconds')
        print(f'Checked {checked_count} domains')
        print(f'{found} were available')
        print(f'{checked_count - found} were not available')
        print('All available domains saved in available_domains.txt')


if __name__ == '__main__':
    main()
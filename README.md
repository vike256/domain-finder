A terminal program to check for available domains.  

Loops through a list of domain names and TLDs and sends a whois-request to each domain. The program lists the domain as available if the whois-response contains "not found". A simple but powerful tool. 

Help: `python main.py -h`  
Example: `python main.py -name coolguy catpics -tld com net soy zip`  

import requests
import sys
from urlpath import URL

HEADER = """
  _____       _           _        _____ _               _
 |  __ \     | |         | |      / ____| |             | |
 | |__) |___ | |__   ___ | |_ ___| |    | |__   ___  ___| | _____ _ __
 |  _  // _ \| '_ \ / _ \| __/ __| |    | '_ \ / _ \/ __| |/ / _ \ '__|
 | | \ \ (_) | |_) | (_) | |_\__ \ |____| | | |  __/ (__|   <  __/ |
 |_|  \_\___/|_.__/ \___/ \__|___/\_____|_| |_|\___|\___|_|\_\___|_|
"""

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def url_retriever(base_url):
    robots_path = URL(base_url, "/robots.txt")
    r = requests.get(robots_path)

    subparts = set()
    for line in r.text.splitlines():
        if line.startswith(("Disallow","Allow")):
            subparts.add(line.split(":")[1].strip())
    
    return subparts

def url_checker(base_url, subparts):
    for part in subparts:
        check_url = URL(base_url, part)
        r = requests.get(check_url)
        if r.status_code == 200:
            print(bcolors.OKGREEN ,r.status_code, check_url, bcolors.ENDC)
        elif r.status_code == 404:
            print(bcolors.FAIL ,r.status_code, check_url,  bcolors.ENDC)
        else:
            print(bcolors.WARNING  ,r.status_code, check_url,  bcolors.ENDC)

    pass



if __name__ == "__main__":
    print(HEADER)
    if len(sys.argv) == 2:
        subparts = url_retriever(sys.argv[1])
        url_checker(sys.argv[1], subparts)
    else: 
        print("Usage: robots-checker.py <url>")
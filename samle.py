#!/usr/bin/env python
from colorama import init ,Fore, Back, Style
init()
import signal
import sys
import thread
from onelogin.saml2.utils import OneLogin_Saml2_Utils
try:
    from urllib.parse import urlparse ,parse_qs
except ImportError:
     from urlparse import urlparse ,parse_qs
import requests 
import xml.etree.ElementTree as ET
import sys
import argparse

import signal
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os

def signal_handler(signal, frame):
        try:
            thread.interrupt_main()
        except KeyboardInterrupt:
            print (Fore.YELLOW + 'Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
        quit()

signal.signal(signal.SIGINT, signal_handler)
def banner():
    print(Fore.RED + '''
        _____ ___    __  _____       ______     __                  __ 
       / ___//   |  /  |/  / /      / ____/  __/ /__________ ______/ /_
       \__ \/ /| | / /|_/ / /      / __/ | |/_/ __/ ___/ __ `/ ___/ __/
      ___/ / ___ |/ /  / / /___   / /____>  </ /_/ /  / /_/ / /__/ /_  
     /____/_/  |_/_/  /_/_____/  /_____/_/|_|\__/_/   \__,_/\___/\__/
     ''')
    print(Fore.CYAN + "                ###  A tool By Fady Othman - @fady_osman  ###")
    print(Fore.CYAN + "                ###        Follow the White Rabbit        ###")
    print("")

def parserError(err):
    banner()
    
    print(Fore.GREEN + "Usage:" + Fore.YELLOW + " python " + sys.argv[0] + " [Options]")
    print(Fore.GREEN + "Use -h or --help for help.")
    print("")
    print(Fore.RED + "Error: " + err)
    exit(0)

def parseArgs():
    parser = argparse.ArgumentParser(description="Tool for discovring callback urls for SAML login pages. You can enter the login page directly or the redirection url to parse directly.")
    parser.error = parserError
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u','--url',help="The login URL for the application.")
    group.add_argument('-U','--url_list',help="A file containing a list of urls for testing.")
    group.add_argument('-r','--redirect_url',help="The url that you get redirected to from the login page.")
    group.add_argument('-R','--redirect_list',help='A file containing a list of redirect urls for testing.')
    parser.add_argument('-p','--parameter', help="The parameter name containing the bas64 deflated data.",default="SAMLRequest")
    return parser.parse_args()

def main():
    args = parseArgs()
    
    if(args.redirect_url != None):
        banner()
        print(Fore.YELLOW + "[*] Analyzing one url.")
        print(Fore.GREEN + extract(args.redirect_url,args.parameter))
    
    if(args.url != None):
        banner()
        print(Fore.YELLOW + "[*] Analyzing one url.")
        redirects = findRedirect(args.url)
        for redirect in redirects:
            if(redirect != None):
                extracted = extract(redirect.url,args.parameter)
                if (extracted != None):
                    print(Fore.GREEN + extracted)


    if(args.url_list != None):
        banner()
        print(Fore.YELLOW + "[*] Analyzing list of urls.")
        with open(args.url_list) as urlList:
            for url in urlList:
                redirects = findRedirect(url.strip())
                if redirects != None:
                    for redirect in redirects:
                        if(redirect != None):
                            extracted = extract(redirect.url,args.parameter)
                            if (extracted != None):
                                print(Fore.GREEN + extracted)
                                break
        
    if(args.redirect_list != None):
        banner()
        print(Fore.YELLOW + "[*] Analyzing list of urls.")
        with open(args.redirect_list) as urlList:
            for url in urlList:
                extracted = extract(url.strip(),args.parameter)
                if (extracted != None):
                    print(Fore.GREEN + extracted)

def findRedirect(url):
    try:
        #Sending the request. 
        request = requests.get(url, allow_redirects=True,verify=False)
        return request.history
    except:
        print(Fore.RED + "[X] Error : Can't connect to '" + url + "'")
        return None

def extract(url,parameterName):
    #Extracting the saml request parameter.
    parsedUrl = urlparse(url)

    if(parameterName in parse_qs(parsedUrl.query)):
        #Decoding the parameter.
        parameter = parse_qs(parsedUrl.query)[parameterName][0]
        data = OneLogin_Saml2_Utils.decode_base64_and_inflate(parameter)
        try:
            root = ET.fromstring(data)
        except:
            print(Fore.RED + "[X] Error : can't parse response as XML for: '" + url + "'")
            return None
        assertUrl = root.get("AssertionConsumerServiceURL")
        if(assertUrl != None):
            return assertUrl
        else:
            print(Fore.RED + "[X] Error : Can't find the 'AssertionConsumerServiceURL' element for '" + url + "'")
            return None
    else:
        #print(Fore.RED + "[X] Error : Parameter '" + parameterName+ "' doesn't exist in URL:'" + url + "'")
        return None

if __name__ == "__main__":
    main()

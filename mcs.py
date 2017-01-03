
#!/usr/bin/env python
# Do not Share Out Side MCS !!!
# 3/01/2017
# MRX (github.com/rone8989)
# official mallu_sec
# GNU GPL <3.0>
# You can report me for bugs

from mcs import mallusearch
import os
import sys
import re
import urllib2
import random
from urlparse import urlparse
import time


isBanner = True 
user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19'
    ]
vuln_urls = []


def banner():
    print """\033[1;31;40m  
    __  ___        __ __          ______        __                   _____         __     __ _                  
   /  |/  /____ _ / // /__  __   / ____/__  __ / /_   ___   _____   / ___/ ____   / /____/ /(_)___   _____ _____
  / /|_/ // __ `// // // / / /  / /    / / / // __ \ / _ \ / ___/   \__ \ / __ \ / // __  // // _ \ / ___// ___/
 / /  / // /_/ // // // /_/ /  / /___ / /_/ // /_/ //  __// /      ___/ // /_/ // // /_/ // //  __// /   (__  ) 
/_/  /_/ \__,_//_//_/ \__,_/   \____/ \__, //_.___/ \___//_/      /____/ \____//_/ \__,_//_/ \___//_/   /____/  
                                     /____/                                                                     
\033[0;31;40m \n                                      Version: 1.0  \n"""


class options:
    

    def __init__(self):
        global readfile
        print """\033[1;34;40m       You Can Scan By 2 Options
        
                                    There are two options for scanning process
        [1] Scan the websites given from text file
        [2] Scan random vulnerable website by giving Google dork \033[0;34;40m \n"""
        option = raw_input("Choose option [1/2]: ")

        if option == '1':
            print
            os.system('pwd')
            print "This is your files in current directory."
            os.system('ls')

            try:
                filename = raw_input("\nPlease Enter file name: ")
                openfile = open(filename, 'r')
                readfile = openfile.read()
                openfile.close()

            except KeyboardInterrupt:
                print "\n\n[!] Process Interrupted."
                sys.exit()

            except:
                print "\n[!] File does not exist."
                sys.exit()

        elif option == '2':
            mallusearch.main()
            openfile = open("sites.txt", 'r')
            readfile = openfile.read()
            print readfile
            openfile.close()

        else:
            print "Not valid option"
            sys.exit()


class main:
    def __init__(self):
        self.urlreq(self.readfile())
        self.printvuln()

    def readfile(self):
        filelist = readfile.split('\n')
        
        if '' in filelist:
            filelist.pop(filelist.index(''))
        os.system('clear')
        return filelist

    def urlreq(self, urlList):
        for site in urlList:
            parsed = urlparse(site)

           
            if len(parsed.scheme) == 0:
                pass
            elif len(parsed.path) == 0:
                pass
            elif len(parsed.query) == 0:
                pass

            
            url = parsed.scheme + "://" + parsed.netloc

            os.system('clear')
            print " Website Information"
            print " Domain Name : " + parsed.netloc
            print " Protocol    : " + parsed.scheme
            print " Path        : " + parsed.path
            print " Query[s]    : " + parsed.query + "\n"

            self.upordown(url)
            self.scanurl(site)

    def printvuln(self):
       
        vulns = list(set(vuln_urls))
        os.system('clear')
        if len(vulns) != 0:
           
            print "[!] Vulnerable URLs"
            vulnwrite = open("vulnerables.txt", 'w')
            for item in vulns:
                print item
                vulnwrite.write(item + "\n")
            vulnwrite.close()
            print "\nVulnerables saved into vulnerables.txt."
        else:
            print "\nNo Vulnerable URLs found."
        print "Process complete."

    def upordown(self, url):
        header = {'User-Agent': random.choice(user_agents)}
        request = urllib2.Request(url, None, header)

        print "Checking the Website whether it's up or down."
        try:
            urllib2.urlopen(request)
            print "[+] Connected, URL is valid.\n"

        except urllib2.HTTPError, e:
            print e.code
            sys.exit()

        except urllib2.URLError, e:
            print e.reason
            sys.exit()

    def verify(self, url):
        global vuln_urls
        try:
            header = {'User-Agent': random.choice(user_agents)}
            request = urllib2.Request(url, None, header)
            http_request = urllib2.urlopen(request)
            sourcecode = http_request.read()

          
            error_msg = {
                "mysql_error_1": "You have an error in your SQL syntax",
                "mysql_error_2": "supplied argument is not a valid MySQL result resource",
                "mysql_error_3": "check the manual that corresponds to your MySQL",
                "mysql_error_4": "mysql_fetch_array(): supplied argument is not a valid MySQL",
                "mysql_error_5": "function fetch_row()",
                "mssql_error_1": "Microsoft OLE DB Provider for ODBC Drivers error"
                }

            result = {
                "mysql_error1": re.search(error_msg["mysql_error_1"], sourcecode),
                "mysql_error2": re.search(error_msg["mysql_error_2"], sourcecode),
                "mysql_error3": re.search(error_msg["mysql_error_3"], sourcecode),
                "mysql_error4": re.search(error_msg["mysql_error_4"], sourcecode),
                "mysql_error5": re.search(error_msg["mysql_error_5"], sourcecode),
                "mssql_error1": re.search(error_msg["mssql_error_1"], sourcecode)
                }

            for key, resp in result.iteritems():
                try:
                    resp.group()
                    print "[+] SQL error found."
                    time.sleep(1)
                    vuln_urls.append(url)
                except:
                    pass

        except urllib2.HTTPError, e:
            print 'We failed with error code - %s.' % e.code

    def scanurl(self, url):
        trigger_1 = "'"

        parsed_url = urlparse(url)
       

        try:
            parms = dict([item.split("=") for item in parsed_url[4].split("&")])
            parm_keys = parms.keys()

           
            if len(parms) == 1:
                vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + trigger_1
                print "[!] Testing: " + vuln_test
                self.verify(vuln_test)

            elif len(parms) == 2:
                vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + trigger_1 + "&" + parm_keys[1] + "=" + parms[parm_keys[1]]
                print "[!] Testing: " + vuln_test
                self.verify(vuln_test)

                vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + trigger_1
                print "[!] Testing: " + vuln_test
                self.verify(vuln_test)

            elif len(parms) == 3:

                vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + trigger_1 + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + "&" + parm_keys[2] + "=" + parms[parm_keys[2]]
                print "[!] Testing:" + vuln_test
                self.verify(vuln_test)

                vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + trigger_1 + "&" + parm_keys[2] + "=" + parms[parm_keys[2]]
                print "[!] Testing: " + vuln_test
                self.verify(vuln_test)

                vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + "&" + parm_keys[2] + "=" + parms[parm_keys[2]] + trigger_1
                print "[!] Testing: " + vuln_test
                self.verify(vuln_test)
        except IndexError, ValueError:
            print "[-] Query Not Found"


if __name__ == "__main__":
  
    try:
        if isBanner:
            banner()
        options()
        main()

    except KeyboardInterrupt:
        os.system('clear')
        print "[!] User interrupted the process."

        lastask = raw_input("Do you want to save scanned results [y/n] ")
        if lastask == 'y':
            print "Saving the scanned result into vulnerables.txt....."
            
            vulns = list(set(vuln_urls))
            vulnwrite = open("vulnerables.txt", 'w')

            for item in vulns:
                vulnwrite.write(item + "\n")
            vulnwrite.close() 
            print "Done"
            sys.exit()

        else:
            print "Scanned results will not be saved"
            sys.exit()

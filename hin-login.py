#!/usr/bin/env python
# -*- coding: utf-8
#
# Originally written by Svein-Erik Larsen <feinom@gmail.com> to be used at UiA.
# Modified by Øyvind Øvergaard <oyvind.overgaard@gmail.com> for use at HiN.
# Modified by Ali Kaafarani <kaafarani.ali@gmail.com> for general use.
#

"""Use the authentication on HPs wireless network from the command line."""

import urllib2, getpass, sys
from optparse import OptionParser

# the domain to the HP login service, including the final slash, excluding the "logon" resource
AUTH_SITE="https://hp740.grm.hia.no/"

def getlogonstatus():
    """Check if we're logged in or not. Returns "OFF" if not logged on, or the username of the logged on user if logged on"""
    site = urllib2.urlopen(AUTH_SITE).read()

    if site.rfind("You are not logged on") > 0:
        return "OFF"
    else:
        # assuming that we are logged on. not sure if we might get an "expired" warning here instead.
        split_site = site.split()
        return split_site[71].partition("</b>")[0]

def logonstatus():
    """Uses the getlogonstatus function and prints out a user friendly
    message"""
    site = urllib2.urlopen(AUTH_SITE)
    the_page = site.read()
    print getlogonstatus(the_page)
    sys.exit()


def find_value(pagesplit, fieldname):
    """Tries to find the 'secret' and 'vernier' fields"""
    # location of field. The value is +2 fields relative to this.
    loc_field = pagesplit.index('name=' + fieldname) 
    loc_value = loc_field + 2

    return pagesplit[loc_value].lstrip('value="').rstrip('">')

def log_in():
    """Logs the user in"""
    site = urllib2.urlopen(AUTH_SITE)
    the_page = site.read()
    page_split = the_page.split()

    username = raw_input("Username: ")
    password = getpass.getpass()
    secret = find_value(page_split, "secret")
    vernier = find_value(page_split, "verify_vernier")

    dummy = urllib2.urlopen(AUTH_SITE + "/logon?query_string=&javaworks=1&vernier_id=hp&product_id=VNSS&releast_id=1.0&logon_status=0&guest_allowed=0&realm_required=0&secret="+secret+"&verify_vernier="+vernier+"&username="+username+"&password="+password+"&logon_action=Logon+User")

    logonstatus()
    sys.exit()

def log_out():
    """Logs the user out"""
    site = urllib2.urlopen(AUTH_SITE + "logon?logon_action=Logoff")
    logoffpage = site.read()
    
    if logoffpage.rfind("<!-- logged_off") > -1:
        print "You are now logged off..."
    else:
        print "Hmmm...not logged off... Strange..."

    sys.exit()


def main():
    """Main function"""

    parser = OptionParser(description='Lets you log in to the browser-based wireless authentication service offered by HP\'s Access Control Server 740wl.')
    
    parser.add_option("-s", "--status", 
                      action="store_true", 
                      dest="status",
                      help="Print status -- checks if you are logged in or not.")
    parser.add_option("-i", "--login", 
                      action="store_true", 
                      dest="login",
                      help="Log in via the authentication site.")
    parser.add_option("-o", "--logout", 
                      action="store_true", 
                      dest="logout",
                      help="Log out.")

    (options, args) = parser.parse_args()

    if options.status:
        logonstatus()
    elif options.login:
        log_in()
    elif options.logout:
        log_out()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

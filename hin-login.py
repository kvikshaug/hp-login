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
    """Displays the current logon status"""
    status = get_status()
    if status == "OFF":
        print "You are not logged on."
    else:
        print "Logged on as " + status

def find_value(pagesplit, fieldname):
    """Tries to find the 'secret' and 'vernier' fields"""
    # location of field. The value is +2 fields relative to this.
    loc_field = pagesplit.index('name=' + fieldname) 
    loc_value = loc_field + 2

    return pagesplit[loc_value].lstrip('value="').rstrip('">')

def log_in():
    """Logs the user in"""

    username = raw_input("Username: ")
    password = getpass.getpass()

    page_split = urllib2.urlopen(AUTH_SITE).read().split()
    secret = find_value(page_split, "secret")
    vernier = find_value(page_split, "verify_vernier")

    logon_site = urllib2.urlopen(AUTH_SITE + "/logon?query_string=&javaworks=1&vernier_id=hp&product_id=VNSS&releast_id=1.0&logon_status=0&guest_allowed=0&realm_required=0&secret="+secret+"&verify_vernier="+vernier+"&username="+username+"&password="+password+"&logon_action=Logon+User")

    if logon_site.rfind("Bad username or password") > 0:
        print "Wrong username or password; you are not logged on."
        sys.exit()

    status = get_status()
    if status == "OFF":
        print "Sorry, logging on failed for some unknown reason!"
    else:
        print "Now logged on as " + status + "."

def log_out():
    """Logs the user out"""
    urllib2.urlopen(AUTH_SITE + "logon?logon_action=Logoff").read()

    status = get_status()
    if status == "OFF":
        print "You are now logged off."
    else:
        print "I tried to log you off, but you seem to still be logged on as " + status + " - please try again, or log off manually."

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

# hp-login

## What's this?

HP provides a wireless authentication service, a so-called "HP ProCurve Wireless Edge Services zl Module", which is used by a number of universities in Norway.

This is a small script to automatically log you on from CLI, instead of having to visit their ugly site in a browser.

## Cool, I need that, what do I do?

1. Enter the URL to your authentication service in `hp-login.conf`
2. Run `hp-login.py -i` to log in

### Optional:

* Add your username and/or password in cleartext in the config file to avoid entering them for each logon (but exercise caution!)
* Add a symbolic link to /usr/local/bin to be able to login from anywhere
* *OR*: add an alias or function to your shell

## Usage

    Usage: hp-login.py [options]
    
    Lets you log in to the browser-based wireless authentication service offered
    by HP's Access Control Server 740wl.
    
    Options:
      -h, --help    show this help message and exit
      -s, --status  Print status -- checks if you are logged in or not.
      -i, --login   Log in via the authentication site.
      -o, --logout  Log out.

## Credits

* Originally written by Svein-Erik Larsen to be used at UiA.
* Modified by Øyvind Øvergaard (oyvindio) for use at HiN.
* Modified by Ali Kaafarani (murr4y) for general use.


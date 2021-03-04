# Sylfi - Simple LFI Tester

A simple local file inclusion vulnerability tester.

Made with Python 3

## Usage

|  **cli flags**  |                         **information**                         |
| :-------------: | :-------------------------------------------------------------: |
|   -h, --help    |                 show this help message and exit                 |
|    -u, --url    |                  specify target URL in quotes                   |
| -p, --parameter | specify known LFI parameter in quotes (?[file/page/path/site]=) |
| -d, --dir-depth |     specify maximum directory traversal depth (default = 5)     |
| -l, --login-url |                   specify login URL in quotes                   |

### With known LFI parameter (faster)

`sylfi.py -u 'http://<domain_name>:<port>/file_name.php' -p '?file='`

OR

`python3 sylfi.py -u 'http://<domain_name>:<port>/file_name.php' -p '?file='`

### Without specified LFI parameter (slower/brute force)

Might get you blocked for brute forcing.

`sylfi.py -u 'http://<domain_name>:<port>/file_name.php'`

This will try all the parameters specified in the `sylfi.py` file in `parameters` variable.

### If webpage needs user login

First edit the credentials parameters `username` and `password` and their values as per your webpage login POST request inside the variable `login_payload` in the `login` function.

`sylfi.py -u 'http://<domain_name>:<port>/file_name.php' -l 'http://<domain_name>:<port>/login_url' -p '?file='`

## Libraries/Packages Used

[argparse](https://docs.python.org/3/library/argparse.html)
[time](https://docs.python.org/3/library/time.html)
[requests](https://pypi.org/project/requests/)
[colorama](https://pypi.org/project/colorama/)

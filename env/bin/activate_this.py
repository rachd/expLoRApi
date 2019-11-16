Skip to content
 
Search or jump to…

Pull requests
Issues
Marketplace
Explore
 
@rachd 
Learn Git and GitHub without any code!
Using the Hello World guide, you’ll start a branch, write comments, and open a pull request.

 
163
3.3k 789 pypa/virtualenv
 Code  Issues 62  Pull requests 3  Actions  Security  Insights
virtualenv/virtualenv_embedded/activate_this.py  / 
@asottile asottile Fixes for python 3.10 (#1385)
311a909 on Jul 23
@stefanor @nonylene @carljm @gaborbernat @asottile
47 lines (37 sloc)  1.48 KB
  
Code navigation is available!
Navigate your code with ease. Click on function and method calls to jump to their definitions or references in the same repository. Learn more

 You're using jump to definition to discover and navigate code.
Learn more or give us feedback
"""Activate virtualenv for current interpreter:
Use exec(open(this_file).read(), {'__file__': this_file}).
This can be used when you must use an existing Python interpreter, not the virtualenv bin/python.
"""
import os
import site
import sys

try:
    __file__
except NameError:
    raise AssertionError("You must use exec(open(this_file).read(), {'__file__': this_file}))")

# prepend bin to PATH (this file is inside the bin directory)
bin_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] = os.pathsep.join([bin_dir] + os.environ.get("PATH", "").split(os.pathsep))

base = os.path.dirname(bin_dir)

# virtual env is right above bin directory
os.environ["VIRTUAL_ENV"] = base

# add the virtual environments site-package to the host python import mechanism
IS_PYPY = hasattr(sys, "pypy_version_info")
IS_JYTHON = sys.platform.startswith("java")
if IS_JYTHON:
    site_packages = os.path.join(base, "Lib", "site-packages")
elif IS_PYPY:
    site_packages = os.path.join(base, "site-packages")
else:
    IS_WIN = sys.platform == "win32"
    if IS_WIN:
        site_packages = os.path.join(base, "Lib", "site-packages")
    else:
        site_packages = os.path.join(base, "lib", "python{}.{}".format(*sys.version_info), "site-packages")

prev = set(sys.path)
site.addsitedir(site_packages)
sys.real_prefix = sys.prefix
sys.prefix = base

# Move the added items to the front of the path, in place
new = list(sys.path)
sys.path[:] = [i for i in new if i not in prev] + [i for i in new if i in prev]
© 2019 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About

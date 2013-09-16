import os
import sys
import shutil
from os.path import expanduser

home = expanduser("~")
cache_file = "%s/%s" % (home,".gotopycache")
cmd = 'function goto() { \n/usr/bin/python ~/.gotopy $@\n }'
bash_entry = 'source ~/.gotopybash'
bash_src = '%s/.bash_profile' % home
bash_py_src = "%s/%s" % (home,'.gotopybash')
py_src = "%s/%s" % (home,".gotopy")

def _setup():
    if not os.path.exists(cache_file):
        _write('')

def _write(entry):
    f = open(cache_file,'w+')
    f.write(entry)
    f.close()

def _add_to_file(file,entry):
    f = open(file,'a+')
    f.write("%s%s%s" % ("\n",entry,"\n"))
    f.close

def _install():
    _add_to_file(bash_src ,bash_entry)
    shutil.copy("./goto.py",py_src)
    _add_to_file(bash_py_src,cmd)

def _uninstall():
    os.system("rm %s" % bash_py_src)
    os.system("rm %s" % py_src)



def _key_exists(new_line):
    with open(cache_file) as f:
        content = f.readlines()
    for line in content:
        line_comp = line.split("::")
        new_line_comp = new_line.split("::")
        if len(new_line_comp) != 3:
            return "Format needed - path::cmd::key"
        if new_line_comp[0] in line_comp[0]:
            return "Already exists as %s::%s::%s" % (line_comp[0],line_comp[1],line_comp[2])
    return False

if len(sys.argv) == 2:

    if sys.argv[1] == "install":
        _install()
        print "Installed. Please restart your terminal"
        os.system("exit")
        sys.exit(1)
    if sys.argv[1] == "uninstall":
        _uninstall()
        print "Uninstalled. Please remove the line from your .bash_profile"
        sys.exit(1)

    _setup()

    with open(cache_file) as f:
        content = f.readlines()

    for line in content:
        line_comp = line.split("::")
        if(len(line_comp) == 3):
            if sys.argv[1] in line_comp[2]:
                cmd = "%s %s" % (line_comp[1],line_comp[0])
                os.system("echo %s | pbcopy" % cmd)
                print "Paste it now : %s" % cmd

elif len(sys.argv) == 3:
    _setup()
    out = _key_exists(sys.argv[2])
    if not out:
        _add_to_file(cache_file,sys.argv[2])
        print "Added"
    else:
        print "Error as %s" % out
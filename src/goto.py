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

def _read_cache():
    content = False
    if os.path.exists(cache_file):
        with open(cache_file) as f:
                content = f.readlines()

    print "Cache is empty" if not content else "..cache read"

    return content

def _key_exists(new_line):
    content = _read_cache()
    for line in content:
        line_comp = line.split("::")
        if len(line_comp) == 3:
            new_line_comp = new_line.split("::")
            if len(new_line_comp) != 3:
                return "Format needed - path::cmd::key"
            if str(new_line_comp[0]).strip() == str(line_comp[0]).strip():
                return "Already exists as %s::%s::%s" % (line_comp[0],line_comp[1],line_comp[2])
            elif str(new_line_comp[2]).strip() == str(line_comp[2]).strip():
                return "Conflicts with  %s::%s::%s" % (line_comp[0],line_comp[1],line_comp[2])
    return False

def _flush():
    if os.path.exists(cache_file):
        os.system("rm %s" % cache_file)

def _list():
    content = _read_cache()
    if content:
        for line in content:
            print line


if len(sys.argv) == 2:

    if sys.argv[1] == "install":
        _install()
        print "Installed. Please restart your terminal"
        os.system("exit")
        sys.exit(1)
    elif sys.argv[1] == "uninstall":
        _uninstall()
        print "Uninstalled. Please remove the line from your .bash_profile"
        sys.exit(1)

    elif sys.argv[1] == "flush":
        _flush()
        print "Cache cleared"

    elif sys.argv[1] == "list":
        _list()

    else:
        _setup()
        content = _read_cache()
        if content:
            for line in content:
                line_comp = line.split("::")
                if(len(line_comp) == 3):
                    if str(sys.argv[1]).strip() == str(line_comp[2]).strip():
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
        print "Error : %s" % out
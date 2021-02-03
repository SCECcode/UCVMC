#!/usr/bin/env python2
#
# This is the install script for the UCVMC software framework.
# This work in conjuction with scripts in the largefiles directory. The largefile scripts will download and distribute
# the required large files before this ucvm_setup script is run.
#
#
import os
import sys
import getopt
import urllib2
from subprocess import call, Popen, PIPE
import json
import platform
import socket
import shlex

# Variables

# Set the version number for the installation script.
VERSION = "19.4.0"

# User defined variables.
all_flag = False
dynamic_flag = True
use_iobuf = False
## control adding of explicit dynamic linker flag
user_dynamic_flag = False

# Should we abort after testing system conditions?
error_out = False

modelsToInstall = []
librariesToInstall = []
modelPaths = {}
unsupported_features = []
shell_script = ""

# Print usage.
def usage():
    print "Automatically sets up UCVMC and alerts the user to potential complications.\n"
    print "\t-s  --static       Use static linking."
    print "\t-d  --dynamic      Use dynamic linking."
    print "\t-a  --all          Use all available models."
    print ""
    print "UCVMC %s\n" % VERSION
    
# Stands for "error gracefully". Prints out a message for the error and asks to contact software@scec.org.
def eG(err, step):
    print "\nERROR:"
    print "An error occurred while trying to setup UCVMC. Specifically, the error was:\n"
    print str(err)
    print "\nAt step: %s\n" % step
    print "Please contact software@scec.org for assistance setting up UCVMC. In your message,"
    print "please let us know the operating system on which you are running and some"
    print "specifications about your computer.\n"
    exit(1)

# Find out if we have certain executables installed.
def which(file):
    for path in os.environ["PATH"].split(":"):
        if os.path.exists(path + "/" + file):
            return path + "/" + file
    return None


# Records the command to the global shell script variable.
def callAndRecord(command, nocall = False):
    global shell_script
    print '  ==> command used.. '+'_'.join(command)
    if nocall == False:
        retVal = call(command)
        if not retVal == 0:
            eG("Error executing command.", command)
    shell_script += command[0]
    for cmd in command[1:]:
        shell_script += " \"" + cmd + "\""
    shell_script += "\n"

# Prints a pretty text version of a tuple list.
def printPretty(list):
    buffer = ""
    # Make a nice comma list.
    for i in range(0, len(list)):
        buffer += list[i]
        if i < len(list) - 2:
            buffer += ", "
        elif i == len(list) - 2 and len(list) != 2:
            buffer += ", and "
        elif i == len(list) - 2:
            buffer += " and "
    print buffer

# create matching install directory from the build directory
# base on configure's prefix
def createInstallTargetPath( targetpath ):
  print 'ADDING '+targetpath
  if not os.path.exists(targetpath):
    call(["mkdir", "-p", targetpath])

# Install with the configure, make, make install paradigm.
#
# This makes three assumptions
# (1) All required tar files are in the current_working_directory/work directory, and are gzipped
# (2) All installs of type "model" go to ucvmpath/model
# (3) All installs of type "library" go to ucvmpath/lib

#
def installConfigMakeInstall(tarname, ucvmpath, type, config_data):

    print "\nInstalling " + type + " " + tarname
    pathname = "lib"
    if type == "model":
        pathname = "model"
    
    workpath = "./work/" + pathname
    
    strip_level = "2"
    if config_data["Path"] == "fftw" or \
	    config_data["Path"] == "proj-5" or \
            config_data["Path"] == "euclid3" or \
            config_data["Path"] == "netcdf" or \
            config_data["Path"] == "hdf5" or \
            config_data["Path"] == "curl":
        strip_level = "1"
    
    # 
    # We need to un-tar the file.
    # The strip level determines how much of the path found in the tar file are removed.
    # strip=1 will remove the proj-5.0.0/configure and output only configure.in 
    # This enables us to untar into drictories with static names like proj-5
    #
    print "Decompressing " + type
    callAndRecord(["mkdir", "-p", workpath + "/" + config_data["Path"]])
    callAndRecord(["tar", "zxvf", workpath  + "/" + tarname, "-C", workpath + "/" + config_data["Path"], \
                     "--strip", strip_level])

    savedPath = os.getcwd()
    os.chdir(workpath + "/" + config_data["Path"])
    callAndRecord(["cd", workpath + "/" + config_data["Path"]], True)

    #
    # proj-5 library is an exception. It does not require use of aclocal, only ./configure
    #
    if not config_data["Path"] == "proj-5":
        print "\nRunning aclocal"
        aclocal_array = ["aclocal"]
        if os.path.exists("./m4"):
            aclocal_array += ["-I", "m4"]
        callAndRecord(aclocal_array)

        print "\nRunning automake"
        callAndRecord(["automake", "--add-missing", "--force-missing"])
    
        print "\nRunning autoconf"
        callAndRecord(["autoconf"])
    
    print "\nRunning ./configure"
    
    configure_array = ["./configure", "--prefix=" + ucvmpath + "/" + pathname + "/" + config_data["Path"]]
    createInstallTargetPath( ucvmpath + "/" + pathname + "/" + config_data["Path"])
    
    if config_data["Path"] == "cvms5":
        configure_array.append("--with-etree-lib-path=" + ucvmpath + "/lib/euclid3/lib")
        configure_array.append("--with-etree-include-path=" + ucvmpath + "/lib/euclid3/include")
        configure_array.append("--with-proj4-lib-path=" + ucvmpath + "/lib/proj-5/lib")
        configure_array.append("--with-proj4-include-path=" + ucvmpath + "/lib/proj-5/include")
    elif config_data["Path"] == "cca":
        configure_array.append("--with-etree-lib-path=" + ucvmpath + "/lib/euclid3/lib")
        configure_array.append("--with-etree-include-path=" + ucvmpath + "/lib/euclid3/include")
        configure_array.append("--with-proj4-lib-path=" + ucvmpath + "/lib/proj-5/lib")
        configure_array.append("--with-proj4-include-path=" + ucvmpath + "/lib/proj-5/include")
    elif config_data["Path"] == "cs173h":
        configure_array.append("--with-etree-lib-path=" + ucvmpath + "/lib/euclid3/lib")
        configure_array.append("--with-etree-include-path=" + ucvmpath + "/lib/euclid3/include")
        configure_array.append("--with-proj4-lib-path=" + ucvmpath + "/lib/proj-5/lib")
        configure_array.append("--with-proj4-include-path=" + ucvmpath + "/lib/proj-5/include")
    elif config_data["Path"] == "cs173":
        configure_array.append("--with-etree-lib-path=" + ucvmpath + "/lib/euclid3/lib")
        configure_array.append("--with-etree-include-path=" + ucvmpath + "/lib/euclid3/include")
        configure_array.append("--with-proj4-lib-path=" + ucvmpath + "/lib/proj-5/lib")
        configure_array.append("--with-proj4-include-path=" + ucvmpath + "/lib/proj-5/include")
    elif config_data["Path"] == "cencal":
        configure_array.append("LDFLAGS=-L" + ucvmpath + "/lib/euclid3/lib -L" + ucvmpath + "/lib/proj-5/lib")
        configure_array.append("CPPFLAGS=-I" + ucvmpath + "/lib/euclid3/include -I" + ucvmpath + "/lib/proj-5/include")
    elif config_data["Path"] == "netcdf":
        configure_array.append("LDFLAGS=-L" + ucvmpath + "/lib/hdf5/lib")
        configure_array.append("CPPFLAGS=-I" + ucvmpath + "/lib/hdf5/include")
    
    if "CompileFlags" in config_data:
        configure_array += config_data["CompileFlags"].split(" ")
                    
    callAndRecord(configure_array)
    
    print "\nRunning make clean"
    callAndRecord(["make", "clean"])
    
    print "\nRunning make"
    if config_data["Path"] == "cencal":
        os.chdir("./libsrc")
        callAndRecord(["make"])
    else:
        callAndRecord(["make"])
    
    print "\nInstalling..."
    callAndRecord(["make", "install"])
    
    if config_data["Path"] == "cencal":
        os.chdir("../")
        callAndRecord(["mkdir", "-p", ucvmpath + "/model/" + config_data["Path"] + "/model"])
        callAndRecord(["mv", "./model/USGSBayAreaVM-08.3.0.etree", ucvmpath + "/model/" + config_data["Path"] + "/model/"])
        callAndRecord(["mv", "./model/USGSBayAreaVMExt-08.3.0.etree", ucvmpath + "/model/" + config_data["Path"] + "/model/"])
    
    config_data["Install"]="true"
    os.chdir(savedPath)
    callAndRecord(["cd", savedPath], True)


## create the ucvm.sh that is approriate to go into /etc/profile.d/
##
def _formLIBRARYPATH(modelsToInstall, librariesToInstall) :
    str= "${UCVM_INSTALL_PATH}/lib/euclid3/lib:" + \
        "${UCVM_INSTALL_PATH}/lib/proj-5/lib"
    if "CS173" in modelsToInstall:
        str=str + ":${UCVM_INSTALL_PATH}/model/cs173/lib"
    if "CS173H" in modelsToInstall:
        str=str + ":${UCVM_INSTALL_PATH}/model/cs173h/lib"
    if "CVM-H" in modelsToInstall:
        str=str + ":${UCVM_INSTALL_PATH}/model/cvmh1511/lib"
    if "CVM-S4" in modelsToInstall:
        str=str + ":${UCVM_INSTALL_PATH}/model/cvms/lib"
    if "CVM-S4.26" in modelsToInstall:
        str=str + ":${UCVM_INSTALL_PATH}/model/cvms5/lib"
    if "CVM-S4.26.M01" in modelsToInstall:
        str=str + ":${UCVM_INSTALL_PATH}/model/cvms426/lib"
    if "CenCalVM" in modelsToInstall:
        str=str + ":${UCVM_INSTALL_PATH}/model/cencal/lib"
    if "CCA" in modelsToInstall:
        str=str + ":${UCVM_INSTALL_PATH}/model/cca/lib"
    if "NetCDF" in librariesToInstall:
        str=str + ":${UCVM_INSTALL_PATH}/lib/netcdf/lib"
        str=str + ":${UCVM_INSTALL_PATH}/lib/hdf5/lib"
    return str

def makeBashScript(ucvmsrc, ucvmpath, modelsToInstall, librariesToInstall) :
    str="" 
    fp=open("conf/ucvm_bash.sh","w")
    fp.write("## \n")
    fp.write("##  models: [")
    for x in modelsToInstall:
      fp.write(x)
    fp.write("]")
    fp.write("\n")
    fp.write("##  libraries: [")
    for x in librariesToInstall:
      fp.write(x)
    fp.write("]")
    fp.write("\n")
    fp.write("## \n")
    fp.write("\n")
    str="export TOP_UCVM_DIR=" + ucvmsrc 
    fp.write(str)
    fp.write("\n")
    str="export UCVM_SRC_PATH=${TOP_UCVM_DIR}/UCVMC" 
    fp.write(str)
    fp.write("\n")
    str="export UCVM_INSTALL_PATH="+ucvmpath.rstrip("/")
    fp.write(str)
    fp.write("\n")
    fp.write("\n")


    ldstr=_formLIBRARYPATH(modelsToInstall,librariesToInstall)
    str="if [ \"$LD_LIBRARY_PATH\" ] ; then"
    fp.write(str)
    fp.write("\n")
    str="   export LD_LIBRARY_PATH=\""+ldstr+":${LD_LIBRARY_PATH}\""
    fp.write(str)
    fp.write("\n")
    str="   else"
    fp.write(str)
    fp.write("\n")
    str="     export LD_LIBRARY_PATH=\""+ldstr+"\""
    fp.write(str)
    fp.write("\n")
    str="fi"
    fp.write(str)
    fp.write("\n")
    fp.write("\n")

    str="if [ \"$DYLD_LIBRARY_PATH\" ] ; then"
    fp.write(str)
    fp.write("\n")
    str="   export DYLD_LIBRARY_PATH=\""+ldstr+":${DYLD_LIBRARY_PATH}\""
    fp.write(str)
    fp.write("\n")
    str="   else"
    fp.write(str)
    fp.write("\n")
    str="     export DYLD_LIBRARY_PATH=\""+ldstr+"\""
    fp.write(str)
    fp.write("\n")
    str="fi"
    fp.write(str)
    fp.write("\n")
    fp.write("\n")

    str="if [ $PYTHONPATH ] ; then"
    fp.write(str)
    fp.write("\n")
    str="   export PYTHONPATH=\"$PYTHONPATH:${UCVM_INSTALL_PATH}/utilities/pycvm\""
    fp.write(str)
    fp.write("\n")
    str="   else"
    fp.write(str)
    fp.write("\n")
    str="     export PYTHONPATH=\"" + "${UCVM_INSTALL_PATH}/utilities/pycvm\""
    fp.write(str)
    fp.write("\n")
    str="fi"
    fp.write(str)
    fp.write("\n")
    fp.write("\n")

    str="if [ $PATH ] ; then "
    fp.write(str)
    fp.write("\n")
    str="   export PATH=\"${UCVM_INSTALL_PATH}/bin:${UCVM_INSTALL_PATH}/utilities:${PATH}\""
    fp.write(str)
    fp.write("\n")
    str="   else"
    fp.write(str)
    fp.write("\n")
    str="     export PATH=\"${UCVM_INSTALL_PATH}/bin:${UCVM_INSTALL_PATH}/utilities\""
    fp.write(str)
    fp.write("\n")
    str="fi"
    fp.write(str)
    fp.write("\n")
    fp.write("\n")
    fp.close();
    


#
# Start of main method.
# Read in the possible arguments
#
try:
    opts, args = getopt.getopt(sys.argv[1:], "asdh", ["all", "static", "dynamic", "help"])
except getopt.GetoptError, err:
    print str(err)
    usage()
    exit(1)

for o, a in opts:
    if o in ('-a', '--all'):
        all_flag = True
	print "All Flag: True"
    elif o in ('-s', '--static'):
        dynamic_flag = False
        print "static Flag: True"
    elif o in ('-d', '--dynamic'):
        user_dynamic_flag = True 
        print "dynamic Flag: True"
    elif o in ('-h', '--help'):
        usage()
        exit(0)
    else:
        if o[0:6].lower() == "--with-":
            unsupported_features.append(o[7:].lower())
        else:
            print "Invalid option %s" % (o)
            exit(1)

print ""
print "UCVMC %s Installation" % VERSION
print "Copyright (C) 20%s SCEC. All rights reserved." % (VERSION.split(".")[0])

print "Using local setup.list and system.list ...."
    
try:
    f = open("./setup/system.list", "r")
    json_string = f.read()
    f.close()
    system_data = json.loads(json_string)
except StandardError, e:
    eG(e, "Parsing list of supported systems.")
    
try:
    # Check the all-applicable conditions first.
    for k, v in system_data["all"].items():
        if eval(k):
            print "\n" + v["message"]
            exec(v["code"])

    print "Now check system specific conditions."
    for k in system_data:
        print "System_data - k: ", k
        if k != "all" and k in socket.gethostname():
            for k2 in sorted(system_data[k].iterkeys()):
                var_array = system_data[k][k2]
                if k2 != "vars":
                    the_command = Popen([item.replace("\x00", "") for item in shlex.split(var_array["command"])], \
                                        stdout = PIPE, stderr = PIPE)
                    if var_array["listenOn"] == "stderr":
                        com_results = the_command.communicate()[1]
                    else:
                        com_results = the_command.communicate()[0]
                
                    if eval("not " + var_array["condition"] + " com_results"):
                        print "\n" + var_array["not"]
                        exit()
                else:
                    for k3, v3 in var_array.items():
                        if type(v3) is dict:
                            if not eval(k3) == v3["value"]:
                                print "\n" + v3["not"]
                                exec(k3 + " = " + v3["value"])
                            else:
                                exec(k3 + " = " + v3)
except StandardError, e:
    eG(e, "Checking system conditions.")

if error_out == True:
    print "\nError(s) encountered. Please resolve the above errors and re-run this script."
    exit(1)
    
print "Using local setup.list file"
    
try:
    # We now have our list. Parse it.
    f = open("./setup/setup.list", "r")
    json_string = f.read()
    f.close()
    config_data = json.loads(json_string)
except StandardError, e:
    eG(e, "Parsing available model list.")

print "\nPlease answer the following questions to install UCVMC.\n"
print "Note that this install and build process may take up to an hour depending on your"
print "computer speed."
print "Where would you like UCVMC to be installed?"

try:
    if ucvmpath[0] == "$":
        # We want to expand that.
        ucvmpath = os.environ(ucvmpath[1:])
except StandardError, e:
    # Use default path.
    ucvmpath = os.path.expanduser("~")

# Append the version info to the path.
ucvmpath = ucvmpath.rstrip("/") + "/ucvm-" + VERSION

print "(Default: " + ucvmpath + ")"
enteredpath = raw_input("Enter path or blank to use the default path: ")

if enteredpath.strip() == "":
    enteredpath = ucvmpath

while enteredpath is not "":
    # Check to see that that path exists and is writable.
    if not os.access(os.path.dirname(enteredpath.rstrip("/")), os.W_OK | os.X_OK):
        print "\n" + enteredpath + " does not exist or is not writable."
        enteredpath = raw_input("Exiting:Please enter a different path or blank to use the default path: ")
        sys.exit(0)
    else:
        break
    
# Copy final selected path back to the UCVMC path variable.
ucvmpath = enteredpath

# Create necessary directories
if not os.path.exists(ucvmpath):
  call(["mkdir", "-p", ucvmpath])
  call(["mkdir", "-p", ucvmpath+'/work'])
  call(["mkdir", "-p", ucvmpath+'/lib'])
    
for model in sorted(config_data["models"].iterkeys(), key=lambda k: config_data["models"][k]["Order"]):

    the_model = config_data["models"][model]
    tarname = the_model["URL"].split("/")[-1]
    ltarname = "./work/model/" + tarname
## continue only if the model is in work_model_dir 
    if not os.path.isfile(ltarname):
        continue
    if all_flag == True:
        modelsToInstall.append(model)
        continue

    if config_data["models"][model]["Ask"] != "no":
        print "\nWould you like to install " + model + "?"
        dlinstmodel = raw_input("Enter yes or no: ")
     
        if dlinstmodel != "" and dlinstmodel.lower()[0] == "y":
            modelsToInstall.append(model)
            
print "\nYou have indicated that you would like to install"
printPretty(modelsToInstall)

for library in config_data["libraries"]:
    the_library = config_data["libraries"][library]
    if the_library["Ask"] == "yes" or library.lower() in unsupported_features:
        if the_library["Prerequisites"] != "":
            if "Dynamic" in the_library["Prerequisites"] and dynamic_flag == False:
                print library + " requires UCVMC to be linked dynamically. If you would like " + library
                print "to be included, please re-run ucvm_setup.py with the '-d' flag."
            if "Static" in the_library["Prerequisites"] and dynamic_flag == True:
                print library + " requires UCVMC to be linked statically. If you would like " + library
                print "to be included, please re-run ucvm_setup.py without the '-d' flag."            
        
        if library.lower() in unsupported_features:
            print "WARNING: " + library + " is unsupported and we cannot guarantee that UCVMC"
            print "will install correctly on your system if you install it with this library included."
            
        print "\nWould you like to install support for " + library + "?"
        dlinstlibrary = raw_input("Enter yes or no: ")
                 
        if dlinstlibrary.strip() != "" and dlinstlibrary.strip().lower()[0] == "y":
            librariesToInstall.append(library)
    elif the_library["Required"] == "yes":
        librariesToInstall.append(library)

print "\nYou have indicated that you would like to install"
printPretty(librariesToInstall)

# Check if we can make the work directory.
try:
    if not os.path.exists("./work"):
#       call(["rm", "-R", "./work"])
#       call(["mkdir", "-p", "./work"])
        print "Work directory does not exist. Error, exitting..."
        sys.exit(1)
    if not os.path.exists("./work") or not os.access("./work", os.W_OK | os.X_OK):
        print "Could not create ./work directory."
        sys.exit(1)
except StandardError, e:
    eG(e, "Could not create ./work directory.")

print "\nNow setting up the required UCVMC libraries..."

for library in config_data["libraries"]:
    the_library = config_data["libraries"][library]
    if library in librariesToInstall:
        if the_library.get("Needs", "") != "":
            try:
                #downloadWithProgress(config_data["libraries"][the_library["Needs"]]["URL"], "./work/lib", \
                #                     "Downloading" + the_library["Needs"])
                tarname = config_data["libraries"][the_library["Needs"]]["URL"].split("/")[-1]
                print "Calling Needs Install with tarname,ucvmpath,library:",tarname,ucvmpath
                installConfigMakeInstall(tarname, ucvmpath, "library", config_data["libraries"][the_library["Needs"]])
            except StandardError, e:
                eG(e, "Error installing library " + the_library["Needs"] + " (needed by " + library + ").")
    
        try:
            #downloadWithProgress(the_library["URL"], "./work/lib", "Downloading " + library + "..." )
            tarname = the_library["URL"].split("/")[-1]
            print "Calling URL Install with tarname,ucvmpath,library:",tarname,ucvmpath
            installConfigMakeInstall(tarname, ucvmpath, "library", the_library)
        except StandardError, e:
            eG(e, "Error installing library " + library + ".")

print "\nNow setting up CVM models..."

for model in config_data["models"]:
    print "Install model_name: ", model
    the_model = config_data["models"][model]
    if model in modelsToInstall:
        try:
	    #
            # Currently, this test for existing tar file will always fail because of the
            # recursive directory removal done above
            # TODO: Change this to check for largefiles/file and copy over if it has been downloaded already
            #
            tarname = the_model["URL"].split("/")[-1]
            ltarname = "./work/model/" + tarname
            print "Preparing to install model with tarname: ",tarname
	    if not os.path.isfile(ltarname):
                print "Model file not found in work directory:",tarname
                print "Exiting..."
                sys.exit(1)
            else:
		print "Model tar file found in work directory:",ltarname
            installConfigMakeInstall(tarname, ucvmpath, "model", the_model)
        except StandardError, e:
            eG(e, "Error installing model " + model + ".")

# Now that the models are installed, we can finally install UCVMC!
print "\nInstalling UCVMC software..."

print "\nRunning aclocal"
callAndRecord(["aclocal", "-I", "./m4"])
print "\nRunning automake"
callAndRecord(["automake", "--add-missing", "--force-missing"])
print "\nRunning autoconf"
callAndRecord(["autoconf"])
 
print "\nRunning ./configure for UCVMC"
 
ucvm_conf_command = ["./configure", "--with-etree-include-path=" + ucvmpath + "/lib/euclid3/include", \
                     "--with-etree-lib-path=" + ucvmpath + "/lib/euclid3/lib", \
                     "--with-proj4-include-path=" + ucvmpath + "/lib/proj-5/include", \
                     "--with-proj4-lib-path=" + ucvmpath + "/lib/proj-5/lib", \
                     "--with-fftw-include-path=" + ucvmpath + "/lib/fftw/include", \
                     "--with-fftw-lib-path=" + ucvmpath + "/lib/fftw/lib"]

for model in modelsToInstall:
    the_model = config_data["models"][model]
    
    # We need to append the flags.
    flag_array = []
    flags = the_model["Flags"].split(" ")
     
    for flag in flags:
        flag_split = flag.split("=")
        if len(flag_split) == 1:
            flag_array.append(str(flag))
        else:
            pathToUse =  ucvmpath + "/model/" + the_model["Path"]
            if model in modelPaths:
                pathToUse = modelPaths[model]
            flag_array.append(str(flag_split[0] + "=" + pathToUse + "/" + flag_split[1]))
             
    ucvm_conf_command += flag_array
     
ucvm_conf_command.append("--prefix=" + ucvmpath)

if dynamic_flag == False:
    ucvm_conf_command.append("--enable-static")
if user_dynamic_flag == True:
    ucvm_conf_command.append("--enable-dynamic")
if use_iobuf == True:
    ucvm_conf_command.append("--enable-iobuf")
 
if "NetCDF" in librariesToInstall:
    ucvm_conf_command.append("--enable-netcdf")
    ucvm_conf_command.append("--with-netcdf-include-path=" + ucvmpath + "/lib/netcdf/include")
    ucvm_conf_command.append("--with-netcdf-lib-path=" + ucvmpath + "/lib/netcdf/lib")
    ucvm_conf_command.append("LDFLAGS=-L" + ucvmpath + "/lib/hdf5/lib")
    
callAndRecord(ucvm_conf_command)

print "\nMaking UCVMC"
callAndRecord(["make", "clean"])
callAndRecord(["make"])
print "\nInstalling UCVMC"
callAndRecord(["make", "install"])

print "\nDone installing UCVMC!"

sys.stdout.write("\nThank you for installing UCVMC. ")
sys.stdout.flush()

if platform.system() == "Darwin" or dynamic_flag == True:
    makeBashScript(os.getcwd(), ucvmpath ,modelsToInstall, librariesToInstall)

    print "To try out UCVMC, we recommend adding the content from " + ucvmpath.rstrip("/")  + "/conf/ucvm_bash.sh +" 
    print "to the end of your ~/.bash_profile file so that"
    print "they are preserved for the next time you login."

print "\nOnce you have set these environment variables, return to the UCVMC source directory and type"
print "make check"
print "This will run the UCVMC unite and acceptance tests. If all tests pass. UCVMC is correctly installed"
print "and ready to use on your computer."
print "\nTo try out ucvm, once the tests pass, move to the UCVMC installation directory, and run an example query."
print "\nAs an example:\ncd " + ucvmpath + "\n./bin/ucvm_query -f ./conf/ucvm.conf -m cvms < ./tests/inputs/test_latlons.txt"
print "You will then see the following output:\nUsing Geo Depth coordinates as default mode."
print " -118.0000    34.0000      0.000    280.896    390.000       cvms    696.491    213.000   1974.976       none      0.000      0.000      0.000      crust    696.491    213.000   1974.976"
print " -118.0000    34.0000     50.000    280.896    390.000       cvms   1669.540    548.000   2128.620       none      0.000      0.000      0.000      crust   1669.540    548.000   2128.620"
print " -118.0000    34.0000    100.000    280.896    390.000       cvms   1683.174    603.470   2130.773       none      0.000      0.000      0.000      crust   1683.174    603.470   2130.773"
print "-118.0000    34.0000    500.000    280.896    390.000       cvms   3097.562   1656.495   2354.105       none      0.000      0.000      0.000      crust   3097.562   1656.495   2354.105"
print " -118.0000    34.0000   1000.000    280.896    390.000       cvms   3660.809   2056.628   2443.042       none      0.000      0.000      0.000      crust   3660.809   2056.628   2443.042"


try:
    f = open('./setup_log.sh', 'w')
    f.write(shell_script)
    f.close()
except StandardError, e:
    eG(e, "Saving setup_log.sh.")

# Write out a installation json file (expanded from setup.list)
try:
    f = open('./setup_install.list', 'w')
    f.write(json.dumps(config_data,indent=2,sort_keys=True))
    f.close()
except StandardError, e:
    eG(e, "Saving setup_install.list.")

print "\nInstallation complete. Installation log file saved at ./setup_log.sh\n"

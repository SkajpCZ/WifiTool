import os,subprocess,time,datetime,codecs,sys,requests

## Info
__version__ = "1"
__creator__ = 'Skajp'
__link__ = "https://github.com/SkajpCZ/WifiTool"
__about__ = "This tool is for capturing wifi handshakes and extracting password hashes from them. It is specifically designed for wifi wardriving, this tool makes it easier and quicker to do."
__helpmenu__ = f"""
What this tool does?
    {__about__}

Usage:
    -w  \033[0;90m|\033[0m --write \033[0;90m<file>\033[0m        Writes to specific file
    -i  \033[0;90m|\033[0m --interface \033[0;90m<adapter>\033[0m Automatically selects wifi adapter
    -d  \033[0;90m|\033[0m --deauth              Script will deauthenticate wifis
    -dd \033[0;90m|\033[0m --dontdeauth          Script will not deauthenticate wifis
    -s  \033[0;90m|\033[0m --skip                Skips checking part
    -kA \033[0;90m|\033[0m --kavahi              Kills avahi_daemon \033[0;90m(recommended when in tty only)\033[0m
    -kN \033[0;90m|\033[0m --knetworkm           Kills NetworkManager and wpa_supplicant services
    -dN \033[0;90m|\033[0m --dknetworkm          Doesn't kill NetworkManager and wpa_supplicant services
    -sN \033[0;90m|\033[0m --startnetworkm       Stars NetworkManager and wpa_supplicant services after capturing handshakes
    -u  \033[0;90m|\033[0m --update              Check for updates
    -v  \033[0;90m|\033[0m --version             Displays current version of tool
    -h  \033[0;90m|\033[0m --help                Displays this help menu

Keep in mind that you need to have spaces between every argument!
Link: \033[0;36m{__link__}\033[0m"""

## Colors
grey = "\033[0;90m"
red = "\033[0;31m"
white = "\033[0m"
green = "\033[0;32m"
yellow = "\033[0;33m"

# Statuses
bad = "\033[0;90m[\033[0;31m-\033[0;90m]\033[0m"
good = "\033[0;90m[\033[0;32m+\033[0;90m]\033[0m"
status = "\033[0;90m[\033[0;33m~\033[0;90m]\033[0m"


banner = rf""" _    _ {yellow}_{white}  __ {yellow}_{white} _____           _ 
| |  | {yellow}(_){white}/ _{yellow}(_){white}_   _|         | |
| |  | |_| |_ _  | | ___   ___ | |
| |/\| | |  _| | | |/ _ \ / _ \| |
\  /\  / | | | | | | (_) | (_) | |
 \/  \/|_|_| |_| \_/\___/ \___/|_| 
                        {yellow}by {__creator__} {grey}|{white} v{__version__}

"""


def clear():os.system("cls") if os.name=="nt"else os.system("clear")

def Update():
    try:
        Chec = int(requests.get("https://pastebin.com/raw/RTm8i0in").text)
        ver = int(__version__.split(" ")[0]) if "testing" in __version__ else __version__
        if ver == Chec: print(f"\n{good} You have most recent version of WifiTool")
        elif ver < Chec: 
            print(f"\n{bad} You have older version of WifiTool")
            print(f"{status} Current version {grey}[{yellow} {__version__} {grey}]{white} most recent one is {grey}[{yellow} {Chec} {grey}]{white}")
            print(f"{status} New version is availaible on github: \033[0;36m{__link__}{white}")
            if input(f"\n{grey}/>{white} Do you want to automatically download newest version? {grey}(y/N)").lower() in ["y","yes"]:os.system("git pull")
        elif ver > Chec: 
            print(f"\n{good} You have testing version of WifiTool")
            print(f"{status} Keep in mind that not all things can work properly")
    except: print(f"\n{bad} Can't connect to internet, please check your internet connection and try again in few minutes")


def NM_runs():
    try:output = subprocess.check_output(['systemctl', 'is-active', 'NetworkManager']).decode().strip();return True
    except subprocess.CalledProcessError:return False

def avahi_runs():
    try:output = subprocess.check_output(['systemctl', 'is-active', 'avahi-daemon']).decode().strip();return True
    except subprocess.CalledProcessError:return False

def avahi(action):
    a = ["stopped","stopping"] if action=="stop" else ["started","starting"]
    try:subprocess.run(['sudo', 'systemctl', action, 'avahi_daemon.service'], check=True);print(f"{good} avahi_daemon {a[0]} successfully")
    except subprocess.CalledProcessError as e:print(f"Error {a[1]} avahi_daemon: {e}")


def nm(action):
    a = ["stopped","stopping"] if action=="stop" else ["started","starting"]
    try:subprocess.run(['sudo', 'systemctl', action, 'NetworkManager'], check=True);print(f"{good} NetworkManager {a[0]} successfully")
    except subprocess.CalledProcessError as e:print(f"{bad} Error {a[1]} NetworkManager: {e}")

def wpa(action):
    a = ["stopped","stopping"] if action=="stop" else ["started","starting"]
    try:subprocess.run(['sudo', 'systemctl', action, 'wpa_supplicant'], check=True);print(f"{good} wpa_supplicant {a[0]} successfully")
    except subprocess.CalledProcessError as e:print(f"Error {a[1]} wpa_supplicant: {e}")

def mm(interface):
    try:
        subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', interface, 'down'], check=True)
        subprocess.run(['sudo', 'iw', 'dev', interface, 'set', 'type', 'managed'], check=True)
        subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', interface, 'up'], check=True)
        print(f"{good} {interface} set to managed mode successfully")
    except subprocess.CalledProcessError as e: print(f"{bad} Error setting {interface} to monitor mode: {e}")

def CleanIt(hashfile, outputfile, adapter):
    try:alllwa=open(hashfile, "r");alllwa.close();BRUH=True
    except:BRUH=False;return "NO_HANDSHAKES"
    if BRUH:
        bruh = [];bruh1 = [];c = 0
        with open(hashfile, "r") as f:
            for i in f.readlines(): 
                if str(i[:-2]).split("*")[5] not in bruh1: 
                    bruh.append(i);bruh1.append(str(i[:-2]).split("*")[5])
                else: pass
            for i in bruh:
                c+=1
                print(f" FOUND  |  Count {c}  |  " + codecs.decode(i.split("*")[5],'hex').decode('latin-1'))
        try: 
            with open(str(outputfile + ".hc22000"),"a") as f:
                for i in bruh:f.write(i)
            return str(outputfile + ".hc22000")
        except:
            if input(f"\n [-] File '{outputfile}' already exists, do you want to add the wifis? (Y/N): ").lower() == "y":
                with open(str(outputfile + ".hc22000"),"a") as f:
                    for i in bruh:f.write(i)
                return str(outputfile + ".hc22000")
            else:
                time = str(datetime.datetime.now()).replace(":","-").split(".")[0].replace(" ", "_")
                with open(str(outputfile + {time} + ".hc22000"),"a") as f:
                    for i in bruh:f.write(i)
                return str(outputfile + {time} + ".hc22000")

def GetCurrentMode():
    global interfaces
    iwconfig_out=subprocess.check_output("iwconfig",stderr=subprocess.STDOUT).decode("latin-1").splitlines()
    interfaces=[];c=0
    for i in iwconfig_out:
        if "802." in i:
            if "SSID" in i:
                Mode = str(str(iwconfig_out[c+1]).split("Mode:")[1]).split(" ")[0]
                interfaces.append(i.split(" ")[0] + ":" + Mode)
            else:
                Mode = str(i.split("Mode:")[1]).split(" ")[0]
                interfaces.append(i.split(" ")[0] + ":" + Mode)
        c+=1

def StartMonitor(adapter):
    global Snmw
    rootACCS=False;Stop=False
    if Snmw:
        if KillnmAwpa:print(f"{status} Input your sudo password please\n");nm("stop");wpa("stop");rootACCS=True;Stop=True
        else: pass
    else:
        if NM_runs():
            if input(f"\n{status} NetworkManager and wpa_supplicant are running, do you want to stop them? {grey}(y/N):{white} ").lower() in ["y","yes"]:
                print(f"{status} Input your sudo password please\n")
                nm("stop");wpa("stop")
                rootACCS=True;Stop=True
        
    
    if not rootACCS:print(f"{status} Input your sudo password please\n")
    if avahi_runs() and not Stop:nm("stop");wpa("stop")
    mm(adapter)
    if avahi_runs() and not Stop:nm("start");wpa("start")
    GetCurrentMode()
    StartListen(adapter)

def StartListen(adapter):
    global outputfile, deauth
    file = f"/tmp/WIFItoolPCAP" + str(datetime.datetime.now()).replace(":","-").split(".")[0].replace(" ", "_") +".pcap"
    hashfile = f"/tmp/Hashes" + str(datetime.datetime.now()).replace(":","-").split(".")[0].replace(" ", "_") +".hc22000"
    
    if Sdea:
        if input(f"\n{status} Do you want to use deauthentication? {grey}(y/N):{white} ").lower() in ["y","yes"]:deauth = ""
    input(f"{status} After your capture is done just press {grey}[{yellow} Ctrl + c {grey}]\n{status} Press {grey}[{yellow} Enter {grey}]{white} to start capture...")
    os.system(f"sudo hcxdumptool -i {adapter} --beacontx=1 --attemptapmax=25 {deauth} -F --rds=1 -w {file}")
    if Sout: outputfile = input(f"\n\n{grey}/>{white} To what file do you want the hashes extracted?: ")
    print(f"\n{status} Extracting hashes...\n")
    os.system(f"hcxpcapngtool -o {hashfile} {file}")
    print(f"\n{status} Checking and clearing hashes...\n")
    out = CleanIt(hashfile, outputfile,adapter)
    if not out == "NO_HANDSHAKES": print(f"\n{good} Hashes written to {yellow}{out}\n")
    else: print(f"{bad} You didn't capture any handshakes")

    print(f"{status} Putting adapter back to managed mode...")
    if avahi_runs():nm("stop");wpa("stop");mm(adapter);nm("start");wpa("start")
    elif Sava and KillAva: avahi("start")
    elif StartsNM: nm("start");wpa("start")
    else: mm(adapter)
    print(f"\nGoodbye..")

def handleSysArgs():
    global outputfile,deauth,Sout,Sdea,Skip,KillAva,KillnmAwpa,Sava,Snmw,StartsNM,interf,AdaSet 
    Sout = True;Sdea = True;Skip = False;KillAva = False;KillnmAwpa = False;Sava = False;Snmw = False;StartsNM = False;AdaSet = False
    outputfile = "clean"
    deauth = "--disable_deauthentication"
    interf = ""
    for i, arg in enumerate(sys.argv):
        #print(f"{i} - {arg}")
        if arg.lower() == "-w" or arg.lower() == "--write":outputfile = str(sys.argv[int(i+1)]);Sout=False
        elif arg.lower() == "-i" or arg.lower() == "--interface":interf = str(sys.argv[int(i+1)]);AdaSet=True
        elif arg.lower() == "-d" or arg.lower() == "--deauth":deauth="";Sdea=False
        elif arg.lower() == "-dd" or arg.lower() == "--dontdeauth":Sdea=False
        elif arg.lower() == "-s" or arg.lower() == "--skip":Skip=True
        elif arg.lower() == "-ka" or arg.lower() == "--kavahi":KillAva=True;Sava=True
        elif arg.lower() == "-kn" or arg.lower() == "--knetworkm":KillnmAwpa=True;Snmw=True
        elif arg.lower() == "-dn" or arg.lower() == "--dknetworkm":KillnmAwpa=False;Snmw=True
        elif arg.lower() == "-sn" or arg.lower() == "--startnetworkm":StartsNM = True
        elif arg.lower() == "-u" or arg.lower() == "--update":Update();quit()
        elif arg.lower() == "-h" or arg.lower() == "--help":print(banner,__helpmenu__);quit()
        elif arg.lower() == "-v" or arg.lower() == "--version":print(f"\nWifiTool by {__creator__} | version: {__version__}");quit()

def main():
    global AdaŚet, interf
    def SelAdapt():
            adapt = input(f"{grey}/>{white} Choose adapter: ")
            inter = []
            for i in interfaces:inter.append(i.split(":")[0])
            if adapt in inter:
                if i.split(":")[1] == "Managed":StartMonitor(adapt)
                else: StartListen(adapt)
            else:
                print(f"\n{bad} That adapter doesn't exist\n")
                SelAdapt()
    clear();GetCurrentMode()
    print("Welcome to")
    print(banner)
    print(f"{good} Available Adapters:")
    for i in interfaces:print(" "*4 + i.split(":")[0] + " - " + i.split(":")[1])
    print("\n")
    if not AdaSet or len(interf)<1:SelAdapt()
    else:
        adapt = interf
        inter = []
        for i in interfaces:inter.append(i.split(":")[0])
        if adapt in inter:
            if i.split(":")[1] == "Managed":StartMonitor(adapt)
            else: StartListen(adapt)
        else:
            print(f"\n{bad} That adapter doesn't exist\n")
            SelAdapt()
        SelAdapt()

def check():
    # Check for tools
    if not os.path.exists("/usr/bin/hcxdumptool") and not os.path.exists("/usr/bin/hcxpcapngtool") and not os.path.exists("/usr/sbin/iw"):
        with open("/usr/lib/os-release") as f:
            a = f.read()
            if not "Kali" in a: 
                print(f"{status} Installing needed tools...")
                os.system("sudo apt install hcxtools")
            else:
                c = ""
                for i in a.splitlines():
                    if "NAME=" in i and not "PRETTY" in i:c=i.split("=")[1].replace('"',"")
                print(f"{status} This script is made for {grey}[{yellow} Kali Linux {grey}]{white} it seems that you have different distribution {grey}({yellow} {c} {grey}){white}")
                print(f"{bad} For this tool to function you need to install {grey}[{yellow} hcxdumptool {grey}]{white} and {grey}[{yellow} hcxpcapngtool {grey}]{white} and you also need to install {grey}[{yellow} iw {grey}]")
                quit()
    # Check if adapter has monitor mode
    a = subprocess.check_output("iw list",shell=True,stderr=subprocess.STDOUT).decode()
    if not "monitor" in a:
        print(f"{bad} Your wifi adapter doesn't support {grey}[{yellow} monitor mode {grey}]{white}")
        print(f"{status} If you want, here is list of adapters you can buy: {grey}[{yellow} https://pastebin.com/raw/4XRQxFqU {grey}]{white}")
    # avahi check
    if avahi_runs():
        if Sava and KillAva: avahi("stop")
        else:
            print(f"{status} Problematic service {grey}[{yellow} avahi-daemon {grey}]{white} is running\n")
            c = 3
            for _ in range(3):
                print(f" Continuing in {c}s...", end="\r")
                c -= 1
                time.sleep(1)

if __name__ == "__main__":
    if os.name in ["posix","darwin"]:
        if os.path.exists("/usr/lib/os-release"): 
            handleSysArgs()
            if not Skip: check()
        else: 
            print(f"{status} It seems that you have a mac, this script isn't made for it...\n")
            c = 5
            for _ in range(3):
                print(f" Exiting in {c}s...", end="\r")
                c -= 1
                time.sleep(1)
            quit()
        main()
    else: 
        clear()
        print(f"{bad} You need to run this on linux")
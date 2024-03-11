import os,subprocess,time,datetime,codecs,sys,requests

## Info
__version__ = "4"
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
    -eS \033[0;90m|\033[0m --exportssid          Script will export ssids to file \033[0;90m(recommended everytime)\033[0m
    -ds \033[0;90m|\033[0m --dontexportssid      Script will not export ssids to file
    -as \033[0;90m|\033[0m --autostart           Bypasses Enter press before starting
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
        ver = int(__version__.split(" ")[0]) if "testing" in __version__ else int(__version__)
        if ver == Chec: print(f"\n{good} You have most recent version of WifiTool")
        elif ver < Chec: 
            print(f"\n{bad} You have older version of WifiTool")
            print(f"{status} Installed version {grey}[{yellow} {__version__} {grey}]{white} most recent one is {grey}[{yellow} {Chec} {grey}]{white}")
            print(f"{status} New version is available on github: \033[0;36m{__link__}{white}")
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
    try:subprocess.run(['sudo', 'systemctl', action, 'avahi_daemon.service'],check=True);print(f"{good} {yellow}avahi_daemon{white} {a[0]} successfully")
    except subprocess.CalledProcessError as e:print(f"Error {a[1]} {yellow}avahi_daemon{white}: {e}")


def nm(action):
    a = ["stopped","stopping"] if action=="stop" else ["started","starting"]
    try:subprocess.run(['sudo', 'systemctl', action, 'NetworkManager'],check=True);print(f"{good} {yellow}NetworkManager{white} {a[0]} successfully")
    except subprocess.CalledProcessError as e:print(f"{bad} Error {a[1]} {yellow}NetworkManager{white}: {e}")

def wpa(action):
    a = ["stopped","stopping"] if action=="stop" else ["started","starting"]
    try:subprocess.run(['sudo', 'systemctl', action, 'wpa_supplicant'], check=True);print(f"{good} {yellow}wpa_supplicant{white} {a[0]} successfully")
    except subprocess.CalledProcessError as e:print(f"Error {a[1]} {yellow}wpa_supplicant{white}: {e}")

def mm(interface, mode):
    try:
        subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', interface, 'down'], check=True)
        subprocess.run(['sudo', 'iw', 'dev', interface, 'set', 'type', mode], check=True)
        subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', interface, 'up'], check=True)
        print(f"{good} {yellow}{interface}{white} set to {yellow}{mode}{white} mode successfully")
    except subprocess.CalledProcessError as e: print(f"{bad} Error setting {yellow}{interface}{white} to {yellow}{mode}{white} mode: {e}")

def CleanIt(hashfile, outputfile, adapter):
    global ExpSSID,SSIDsF,SSIDsW,deauth
    if ExpSSID:
        SSIDsW = [];CapSW = []
        with open(SSIDsF, "r") as f:
            for i in f.readlines(): CapSW.append(i)
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
                SSID = codecs.decode(i.split("*")[5],'hex').decode('latin-1')
                print(f" {green}FOUND  {grey}|{yellow}  Count {white}{c}  {grey}|{yellow}  {SSID}")
                if ExpSSID:
                    if str(i[:-2]).split("*")[1]=="02":SSIDsW.append([SSID,str(i[:-2]).split("*")[6],str(i[:-2]).split("*")[1]])
                    elif str(i[:-2]).split("*")[1]=="01":SSIDsW.append([SSID,str(i[:-2]).split("*")[2],str(i[:-2]).split("*")[1]])
        Fout = ""
        time = str(datetime.datetime.now())
        try: 
            with open(str(outputfile + ".hc22000"),"a") as f:
                for i in bruh:f.write(i)
            Fout = str(outputfile + ".hc22000")
        except:
            if input(f"\n{status} File {grey}[{yellow} {outputfile} {grey}]{white} already exists, do you want to add the wifis? {grey}(y/N):{white} ").lower() in ["y","yes"]:
                with open(str(outputfile + ".hc22000"),"a") as f:
                    for i in bruh:f.write(i)
                Fout = str(outputfile + ".hc22000")
            else:
                timeForSave = time.replace(":","-").split(".")[0].replace(" ", "_")
                with open(str(outputfile + {time} + ".hc22000"),"a") as f:
                    for i in bruh:f.write(i)
                Fout = str(outputfile + {time} + ".hc22000")
        if ExpSSID:
            try: open(outputfile + "-SSIDs.txt","x")
            except:pass
            with open(outputfile + "-SSIDs.txt","w+") as f:
                f.write(" - WifiTool | by Skajp - \n")
                f.write(f"Interface: {adapter}\n")
                f.write(f"Scan Time: {time[:-7]}\n")
                Sargs = ""
                for i in sys.argv:Sargs += i + " "
                f.write(f"Tool arguments: {Sargs}\n")
                f.write(f"Hashes save path: {str(Fout)}\n")
                f.write(f"Deauthing: {'Enabled' if len(deauth) < 1 else 'Disabled'}\n\n")
                f.write("~------------------- Captured Handshakes -------------------~\n")
                longestI=1;longestR=1
                for i,j,k in SSIDsW:
                    if int(len(i))>longestI:longestI=len(i)
                    if int(len(j))>longestR:longestR=len(j)
                for name,hashS,wpa in SSIDsW: f.write(f'{name:<{int(longestI+1)}}| WPA: {wpa:<{3}}| Hash: {hashS:<{int(longestR+1)}}\n')
                f.write("\n\n~-------------------- Captured Networks --------------------~\n")
                for i in CapSW: f.write(i)
            print(f"\n{good} SSIDs written to {yellow}{outputfile + '-SSIDs.txt'}")
        return Fout
        

def GetCurrentMode():
    global interfaces
    iwconfig_out=subprocess.check_output("iwconfig",stderr=subprocess.STDOUT,shell=True).decode("latin-1").splitlines()
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
        if KillnmAwpa:print(f"{status} Input your sudo password\n");nm("stop");wpa("stop");rootACCS=True;Stop=True
        else: pass
    else:
        if NM_runs():
            if input(f"\n{status} {yellow}NetworkManager{white} and {yellow}wpa_supplicant{white} are running, do you want to stop them? {grey}(y/N):{white} ").lower() in ["y","yes"]:
                print(f"{status} Input your sudo password\n")
                nm("stop");wpa("stop")
                rootACCS=True;Stop=True
    
    if not rootACCS:print(f"{status} Input your sudo password\n")
    if avahi_runs() and not Stop:nm("stop");wpa("stop")
    mm(adapter,"monitor")
    if avahi_runs() and not Stop:nm("start");wpa("start")
    GetCurrentMode()
    StartListen(adapter)

def StartListen(adapter):
    global outputfile,deauth,ExpSSID,SSIDsF,SSIDZ
    file = f"/tmp/WIFItool-PCAP" + str(datetime.datetime.now()).replace(":","-").split(".")[0].replace(" ", "_") +".pcap"
    hashfile = f"/tmp/WIFItool-Hashes" + str(datetime.datetime.now()).replace(":","-").split(".")[0].replace(" ", "_") +".hc22000"
    SSIDsF = f"/tmp/WifiTool-SSID" + str(datetime.datetime.now()).replace(":","-").split(".")[0].replace(" ", "_") +".txt"
    
    if Sdea:
        if input(f"\n{status} Do you want to use deauthentication? {grey}(y/N):{white} ").lower() in ["y","yes"]:deauth = ""
    input(f"{status} After your capture is done just press {grey}[{yellow} Ctrl + c {grey}]\n{status} Press {grey}[{yellow} Enter {grey}]{white} to start capture...") if not Astart else print(f"{status} Starting...")
    os.system(f"sudo hcxdumptool -i {adapter} --beacontx=1 --attemptapmax=25 {deauth} -F --rds=1 -w {file}")
    if Sout: outputfile = input(f"\n\n{grey}/>{white} What file do you want to extract the hashes to?: ")
    print(f"\n{status} Extracting hashes...\n")

    if SSIDZ:
        ExpSSID=True
        if input(f"\n{status} Do you want to extract SSIDs? {grey}(Y/n):{white} ").lower() == "n":ExpSSID=False
    eOPT = f"-o {hashfile} -E {SSIDsF}" if ExpSSID else f"-o {hashfile}"

    os.system(f"hcxpcapngtool {eOPT} {file}")
    print(f"\n{status} Checking and clearing hashes...\n")
    out=CleanIt(hashfile, outputfile,adapter)
    if not out=="NO_HANDSHAKES": print(f"\n{good} Hashes written to {yellow}{out}\n")
    else: print(f"{bad} You didn't capture any handshakes")
    print(f"{status} Putting {yellow}{adapter}{white} back to managed mode...")
    if avahi_runs():nm("stop");wpa("stop");mm(adapter,"managed");nm("start");wpa("start")
    elif Sava and KillAva: avahi("start");mm(adapter,"managed")
    elif StartsNM: nm("start");wpa("start")
    else: mm(adapter,"managed")
    print(f"{status} Whole pcap stored in {grey}[{yellow} {file} {grey}]{white}")
    print(f"\nGoodbye..");quit()

def handleSysArgs():
    global outputfile,deauth,Sout,Sdea,Skip,KillAva,KillnmAwpa,Sava,Snmw,StartsNM,interf,AdaSet,ExpSSID,Astart,SSIDZ
    Sout=True;Sdea=True;Skip=False;KillAva=False;KillnmAwpa=False;Sava=False;Snmw=False;StartsNM=False;AdaSet=False;ExpSSID=False;Astart=False;SSIDZ=True
    outputfile = "clean"
    deauth = "--disable_deauthentication"
    interf = ""
    for i, arg in enumerate(sys.argv):
        if arg.lower() == "-w" or arg.lower() == "--write":outputfile = str(sys.argv[int(i+1)]);Sout=False
        elif arg.lower() == "-i" or arg.lower() == "--interface":interf = str(sys.argv[int(i+1)]);AdaSet=True
        elif arg.lower() == "-d" or arg.lower() == "--deauth":deauth="";Sdea=False
        elif arg.lower() == "-dd" or arg.lower() == "--dontdeauth":Sdea=False
        elif arg.lower() == "-s" or arg.lower() == "--skip":Skip=True
        elif arg.lower() == "-ka" or arg.lower() == "--kavahi":KillAva=True;Sava=True
        elif arg.lower() == "-kn" or arg.lower() == "--knetworkm":KillnmAwpa=True;Snmw=True
        elif arg.lower() == "-dn" or arg.lower() == "--dknetworkm":KillnmAwpa=False;Snmw=True
        elif arg.lower() == "-sn" or arg.lower() == "--startnetworkm":StartsNM=True
        elif arg.lower() == "-es" or arg.lower() == "--exportssid":ExpSSID=True;SSIDZ=False
        elif arg.lower() == "-ds" or arg.lower() == "--dontexportssid":ExpSSID=True;SSIDZ=False
        elif arg.lower() == "-as" or arg.lower() == "--autostart":Astart=True
        elif arg.lower() == "-u" or arg.lower() == "--update":Update();quit()
        elif arg.lower() == "-h" or arg.lower() == "--help":print(banner,__helpmenu__) if sys.platform!="win32" else print(banner,__helpmenu__,f"\n{bad} You have Windows, this script wont work on it");quit()
        elif arg.lower() == "-v" or arg.lower() == "--version":print(f"\nWifiTool by {__creator__} | version: {__version__}");quit()

def main():
    global AdaSet, interf
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
    # Check for updates
    Update()
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
            for _ in range(c):
                print(f" Continuing in {c}s...", end="\r")
                c -= 1
                time.sleep(1)
    try:
        if str(str(subprocess.check_output("hcxdumptool -v",shell=True).decode().split()[1]).replace(".","")) != "631":
            print(f"{status} This script is tested with {grey}[{yellow} hcxdumptool v6.3.1 {grey}]{white}, it seems like you have different version, so some things maybe will not work for you\n")
            c = 15
            for _ in range(c):
                print(f" Continuing in {c}s...", end="\r")
                c -= 1
                time.sleep(1)
    except:print(f"{bad} Can't get version of {grey}[{yellow} hcxdumptool {grey}]{white}")

if __name__ == "__main__":
    # New OS Check
    if sys.platform in ["linux","darwin"]:
        if not os.path.exists("/usr/lib/os-release") or not os.path.exists("/etc/os-release"): 
            handleSysArgs()
            if not Skip: check()
        elif os.path.exists("/system/app") or os.path.exists("/system/priv-app"):
            handleSysArgs()
            print(f"{status} It seems that you have a {yellow}android{white}, some things may not work...\n");time.sleep(3)
            if not Skip: check()
        else:
            if sys.platform == "darwin":
                handleSysArgs()
                print(f"{status} It seems that you have a {yellow}mac{white}, this script isn't made for it...\n")
                c = 3
                for _ in range(c):
                    print(f" Exiting in {c}s...", end="\r")
                    c -= 1
                    time.sleep(1)
                quit()
            else:
                handleSysArgs()
                print(f"{bad} Can't determine your {yellow}linux{white} distribution...\n")
                if input(f"{status} Do you still want to continue? {grey}(y/N):{white} ").lower() in ["y","yes"]:
                    if not Skip: check()
                quit()
        main()
    else:
        handleSysArgs()
        print(f"{bad} It seems that you are not on {yellow}linux{white}, this script only works on linux\n")
        c = 3
        for _ in range(c):
            print(f" Exiting in {c}s...", end="\r")
            c -= 1
            time.sleep(1)
    

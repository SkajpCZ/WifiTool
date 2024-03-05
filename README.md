# WifiTool 
This tool is for capturing wifi handshakes and extracting password hashes from them. It is specifically designed for wifi wardriving, this tool makes it easier and quicker to do.

<br>

# Updates in v2

### Added
- More polished output in terminal
- Better checking
- Output of SSIDs with some info about scan
### Fixes
- Setting monitor mode on adapter
- Termux indetified as mac

---

```
 _    _ _  __ _ _____           _ 
| |  | (_)/ _(_)_   _|         | |
| |  | |_| |_ _  | | ___   ___ | |
| |/\| | |  _| | | |/ _ \ / _ \| |
\  /\  / | | | | | | (_) | (_) | |
 \/  \/|_|_| |_| \_/\___/ \___/|_| 
                        by Skajp | v2 

 
What this tool does?
    This tool is for capturing wifi handshakes and extracting password hashes from them. It is specifically designed for wifi wardriving, this tool makes it easier and quicker to do.

Usage:
    -w  | --write <file>        Writes to specific file
    -i  | --interface <adapter> Automatically selects wifi adapter
    -d  | --deauth              Script will deauthenticate wifis
    -dd | --dontdeauth          Script will not deauthenticate wifis
    -s  | --skip                Skips checking part
    -kA | --kavahi              Kills avahi_daemon (recommended when in tty only)
    -kN | --knetworkm           Kills NetworkManager and wpa_supplicant services
    -dN | --dknetworkm          Doesn't kill NetworkManager and wpa_supplicant services
    -sN | --startnetworkm       Stars NetworkManager and wpa_supplicant services after capturing handshakes
    -eS | --exportssid          Script will export ssid to file
    -as | --autostart           Bypasses Enter press before starting
    -u  | --update              Check for updates
    -v  | --version             Displays current version of tool
    -h  | --help                Displays this help menu

Keep in mind that you need to have spaces between every argument!
Link: https://github.com/SkajpCZ/WifiTool
```


# Download

```bash
git clone https://github.com/SkajpCZ/WifiTool
cd WifiTool
pip install -r requirements.txt
python3 WifiTool.py -h
```

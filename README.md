# WifiTool 
This tool is for capturing wifi handshakes and extracting password hashes from them. It is specifically designed for wifi wardriving, this tool makes it easier and quicker to do.


---

```
 _    _ _  __ _ _____           _ 
| |  | (_)/ _(_)_   _|         | |
| |  | |_| |_ _  | | ___   ___ | |
| |/\| | |  _| | | |/ _ \ / _ \| |
\  /\  / | | | | | | (_) | (_) | |
 \/  \/|_|_| |_| \_/\___/ \___/|_| 
                        by Skajp | v1 

 
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

# Scan urls and IP addresses with virus total
The iocs.py script will parse ip addresses and domains from logs to scan them against the virus total api.
ps: virus total API key is required to make the script work!

# Setup
1. pip install -r requirements.txt
2. run `python3 iocs.py server.log`
3. await for json output
# Scan urls and IP addresses with virus total
The iocs.py script will parse ip addresses and domains from logs to scan them against the virus total api.
ps: virus total API key is required to make the script work!

# Setup
1. **edit the source code to a VirusTotal API_KEY**
2. pip install -r requirements.txt
3. run `python3 iocs.py server.log`
4. await for json output
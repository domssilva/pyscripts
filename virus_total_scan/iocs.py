"""
IOCS Extraction script

Parse sample.log and determine malicious score.
The verdict about The IOCs from any free source:
    - VirusTotal
    - OTX
    - Falcon Sandbox

The output should be printed to std out in JSON

indicators []
    value s (parameter used to fetch report from virustotal)
    type s (host, ip, etc.)
    providers[]
        verdict s (malicious OR not malicious)
        score s /optional
"""

import sys
import re
import requests
import json
from time import sleep
from datetime import datetime

API_KEY = '' # 'add your API key here.'
REQ_DELAY = 0.35

if len(sys.argv) <= 1:
    print('Error: file missing.\nUsage: python3 iocs.py <file.log>. Please try again')
    sys.exit(1)

ip_addr = { 'regx': r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', 'matches': [] }
domains = { 'regx': r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?=\s|$)?' , 'matches': [] }

log = sys.argv[1]
output = { 'indicators': [] }

# parse from file IP addresses and domains
def collect_values(file):
    for log_line in file:
        # collect ip addresses
        ip_match = re.findall(ip_addr['regx'], log_line)
        ip_addr['matches'].extend(ip_match)
        # collect domains
        domain_match = re.findall(domains['regx'], log_line)
        domains['matches'].extend(domain_match)

# Scans IP addresses with virus total
def vt_scan_ip(ip):
    # https://developers.virustotal.com/reference/ip-info
    url = f'https://www.virustotal.com/api/v3/ip_addresses/{ip}'
    params = { 'X-Apikey': API_KEY, 'accept': 'application/json' }
    response = requests.get(url, headers=params)
    # data.attributes is the data source
    json = response.json().get('data').get('attributes')
    # structure output
    output['indicators'].append({
        'value': ip,
        'type': 'ip address',
        'providers': []
        })
    # iterate over providers to collect data
    for provider in json.get('last_analysis_results'):
        p = json.get('last_analysis_results')[provider]
        provider_obj = {
                'provider': p['engine_name'],
                'verdict': 'not malicious' if p['result'] == 'clean' else 'malicious'
                }
        # add score only if available
        score = json.get('reputation')
        if score and score > 0:
            provider_obj['score'] = f'{score}/100'
        output['indicators'][-1]['providers'].append(provider_obj)
    # debug
    # print(output)

# Scans domain with virus total
def vt_scan_domain(domain):
    # https://developers.virustotal.com/reference/domain-info
    url = f'https://www.virustotal.com/api/v3/domains/{domain}'
    params = { 'X-Apikey': API_KEY, 'accept': 'application/json' }
    response = requests.get(url, headers=params)
    # data.attributes is the data source
    json = response.json().get('data').get('attributes')
    # structure output
    output['indicators'].append({
        'value': domain,
        'type': 'domain',
        'providers': []
        })
    # iterate over providers to collect data
    for provider in json.get('last_analysis_results'):
        p = json.get('last_analysis_results')[provider]
        provider_obj = {
                'provider': p['engine_name'],
                'verdict': 'not malicious' if p['result'] == 'clean' else 'malicious'
                }
        # add score only if available
        if json.get('reputation'):
            provider_obj['score'] = f'{json.get("reputation")}/100'
        output['indicators'][-1]['providers'].append(provider_obj)
    # debug
    # print(output)

# open file
log_file = open(log, 'r')

try:
    collect_values(log_file)
    print('===== Generating Json File =====')
    print(f'Current delay between requests = {REQ_DELAY}')
    # for each IP address -> virus total scan
    for ip in ip_addr['matches']:
        sleep(REQ_DELAY) # add delay
        vt_scan_ip(ip)

    # for each domain -> virus total scan
    for domain in domains['matches']: 
        sleep(REQ_DELAY) # add delay
        vt_scan_domain(domain)
    # write json file
    filename = f'{datetime.now().strftime("%d%m%Y-%H%M%S")}-iocs_output.json'
    with open(filename, 'w') as json_file:
        json.dump(output, json_file, indent=4)
except Exception as e:
    print(e)
finally:
    # close file
    log_file.close()
    print(f'{filename} is ready!')
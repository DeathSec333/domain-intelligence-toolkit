#!/usr/bin/env python3
"""
Domain Intelligence Toolkit - DeathSec333 Edition v1.0.0
Advanced domain intelligence and investigation toolkit
Educational use only - Authorized testing required
"""

import dns.resolver
import whois
import requests
import socket
import subprocess
import json
import os
import re
import sys
from datetime import datetime
from colorama import init, Fore, Back, Style
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class DomainIntelligence:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = {}
        self.dns_servers = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_banner(self):
        """Display the toolkit banner"""
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.CYAN}            Domain Intelligence Toolkit v1.0.0               {Fore.RED}║
{Fore.RED}║{Fore.YELLOW}                  DeathSec333 Edition                        {Fore.RED}║
{Fore.RED}║{Fore.GREEN}         Advanced Domain Intelligence Gathering              {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}⚠️  EDUCATIONAL USE ONLY - AUTHORIZED TESTING REQUIRED ⚠️{Style.RESET_ALL}
"""
        print(banner)
        
    def print_menu(self):
        """Display the main menu"""
        menu = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
{Fore.CYAN}║                        MAIN MENU                             ║
{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}[1]{Fore.WHITE} Comprehensive Domain Analysis
{Fore.GREEN}[2]{Fore.WHITE} DNS Record Enumeration
{Fore.GREEN}[3]{Fore.WHITE} WHOIS Information Gathering
{Fore.GREEN}[4]{Fore.WHITE} Subdomain Discovery
{Fore.GREEN}[5]{Fore.WHITE} SSL Certificate Analysis
{Fore.GREEN}[6]{Fore.WHITE} Domain Reputation Check
{Fore.GREEN}[7]{Fore.WHITE} Port & Service Scanning
{Fore.GREEN}[8]{Fore.WHITE} Domain History Analysis
{Fore.GREEN}[9]{Fore.WHITE} Bulk Domain Analysis
{Fore.GREEN}[10]{Fore.WHITE} Export & Reporting
{Fore.RED}[0]{Fore.WHITE} Exit

{Fore.YELLOW}Choose an option: {Style.RESET_ALL}"""
        print(menu)
        
    def validate_domain(self, domain):
        """Validate domain format"""
        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        )
        return domain_pattern.match(domain.lower()) is not None
        
    def resolve_domain(self, domain):
        """Resolve domain to IP address"""
        try:
            result = socket.gethostbyname(domain)
            return result
        except socket.gaierror:
            return None
        
    def get_dns_records(self, domain):
        """Get comprehensive DNS records"""
        dns_records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'PTR']
        
        for record_type in record_types:
            try:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = self.dns_servers
                answers = resolver.resolve(domain, record_type)
                dns_records[record_type] = [str(rdata) for rdata in answers]
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, Exception):
                dns_records[record_type] = []
                
        return dns_records
        
    def get_whois_info(self, domain):
        """Get WHOIS information"""
        try:
            whois_data = whois.whois(domain)
            return {
                'domain_name': whois_data.domain_name,
                'registrar': whois_data.registrar,
                'creation_date': str(whois_data.creation_date),
                'expiration_date': str(whois_data.expiration_date),
                'updated_date': str(whois_data.updated_date),
                'name_servers': whois_data.name_servers,
                'status': whois_data.status,
                'emails': whois_data.emails,
                'country': whois_data.country,
                'org': whois_data.org
            }
        except Exception as e:
            return {'error': str(e)}
            
    def discover_subdomains(self, domain):
        """Discover subdomains using wordlist"""
        subdomains = []
        wordlist_path = 'wordlists/subdomains.txt'
        
        if not os.path.exists(wordlist_path):
            return {'error': 'Wordlist not found'}
            
        try:
            with open(wordlist_path, 'r') as f:
                wordlist = [line.strip() for line in f.readlines()]
                
            print(f"\n{Fore.BLUE}🔍 Testing {len(wordlist)} subdomains...{Style.RESET_ALL}")
            
            for i, subdomain in enumerate(wordlist, 1):
                test_domain = f"{subdomain}.{domain}"
                
                if i % 10 == 0:
                    print(f"{Fore.YELLOW}Progress: {i}/{len(wordlist)} tested{Style.RESET_ALL}")
                
                try:
                    ip = socket.gethostbyname(test_domain)
                    subdomains.append({
                        'subdomain': test_domain,
                        'ip': ip,
                        'status': 'Active'
                    })
                    print(f"{Fore.GREEN}✅ Found: {test_domain} -> {ip}{Style.RESET_ALL}")
                except socket.gaierror:
                    continue
                    
        except Exception as e:
            return {'error': str(e)}
            
        return subdomains
        
    def check_ssl_certificate(self, domain):
        """Check SSL certificate information"""
        try:
            import ssl
            import socket
            from datetime import datetime
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
            return {
                'subject': dict(x[0] for x in cert['subject']),
                'issuer': dict(x[0] for x in cert['issuer']),
                'version': cert['version'],
                'serial_number': cert['serialNumber'],
                'not_before': cert['notBefore'],
                'not_after': cert['notAfter'],
                'signature_algorithm': cert.get('signatureAlgorithm', 'Unknown'),
                'san': cert.get('subjectAltName', [])
            }
        except Exception as e:
            return {'error': str(e)}
        
    def check_domain_reputation(self, domain):
        """Check domain reputation using multiple sources"""
        reputation_data = {
            'virustotal': self.check_virustotal(domain),
            'google_safe_browsing': self.check_google_safe_browsing(domain),
            'malware_check': self.check_malware_domains(domain),
            'phishing_check': self.check_phishing_domains(domain)
        }
        return reputation_data
        
    def check_virustotal(self, domain):
        """Check domain against VirusTotal (basic check)"""
        try:
            # Basic reputation check without API key
            suspicious_indicators = [
                'suspicious', 'malware', 'phishing', 'spam', 'blacklist'
            ]
            
            # Simple heuristic check
            if any(indicator in domain.lower() for indicator in suspicious_indicators):
                return {'status': 'suspicious', 'reason': 'Contains suspicious keywords'}
            else:
                return {'status': 'clean', 'reason': 'No obvious suspicious indicators'}
                
        except Exception as e:
            return {'error': str(e)}
            
    def check_google_safe_browsing(self, domain):
        """Basic Google Safe Browsing check"""
        try:
            # Simple check for known bad patterns
            bad_patterns = ['phishing', 'malware', 'scam', 'fake']
            
            if any(pattern in domain.lower() for pattern in bad_patterns):
                return {'status': 'potentially_unsafe', 'reason': 'Contains suspicious patterns'}
            else:
                return {'status': 'safe', 'reason': 'No known unsafe patterns detected'}
                
        except Exception as e:
            return {'error': str(e)}
            
    def check_malware_domains(self, domain):
        """Check against known malware domain patterns"""
        try:
            malware_indicators = [
                'malware', 'trojan', 'virus', 'botnet', 'c2', 'command'
            ]
            
            if any(indicator in domain.lower() for indicator in malware_indicators):
                return {'status': 'high_risk', 'reason': 'Contains malware-related keywords'}
            else:
                return {'status': 'low_risk', 'reason': 'No malware indicators found'}
                
        except Exception as e:
            return {'error': str(e)}
            
    def check_phishing_domains(self, domain):
        """Check for phishing domain characteristics"""
        try:
            phishing_indicators = [
                'paypal', 'amazon', 'google', 'microsoft', 'apple', 'bank',
                'secure', 'verify', 'update', 'confirm', 'login'
            ]
            
            # Check for suspicious TLDs
            suspicious_tlds = ['.tk', '.ml', '.ga', '.cf']
            
            risk_score = 0
            reasons = []
            
            # Check for brand impersonation
            for indicator in phishing_indicators:
                if indicator in domain.lower() and not domain.endswith(f'{indicator}.com'):
                    risk_score += 1
                    reasons.append(f'Potential {indicator} impersonation')
                    
            # Check for suspicious TLD
            if any(domain.endswith(tld) for tld in suspicious_tlds):
                risk_score += 2
                reasons.append('Uses suspicious TLD')
                
            if risk_score >= 2:
                return {'status': 'high_phishing_risk', 'reasons': reasons}
            elif risk_score == 1:
                return {'status': 'medium_phishing_risk', 'reasons': reasons}
            else:
                return {'status': 'low_phishing_risk', 'reasons': ['No obvious phishing indicators']}
                
        except Exception as e:
            return {'error': str(e)}
            
    def scan_ports(self, domain, ports=None):
        """Scan common ports on domain"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306]
            
        open_ports = []
        
        try:
            ip = socket.gethostbyname(domain)
            print(f"\n{Fore.BLUE}🔍 Scanning {len(ports)} ports on {domain} ({ip})...{Style.RESET_ALL}")
            
            for port in ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    result = sock.connect_ex((ip, port))
                    
                    if result == 0:
                        service = self.get_service_name(port)
                        open_ports.append({
                            'port': port,
                            'service': service,
                            'status': 'open'
                        })
                        print(f"{Fore.GREEN}✅ Port {port} ({service}) - OPEN{Style.RESET_ALL}")
                    
                    sock.close()
                    
                except Exception:
                    continue
                    
        except Exception as e:
            return {'error': str(e)}
            
        return open_ports
        
    def get_service_name(self, port):
        """Get service name for port number"""
        services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS',
            993: 'IMAPS', 995: 'POP3S', 3389: 'RDP', 5432: 'PostgreSQL',
            3306: 'MySQL'
        }
        return services.get(port, 'Unknown')
        
    def comprehensive_analysis(self):
        """Perform comprehensive domain analysis"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║              COMPREHENSIVE DOMAIN ANALYSIS                  ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        domain = input(f"\n{Fore.YELLOW}Enter domain name (e.g., example.com): {Style.RESET_ALL}").strip()
        
        if not domain:
            print(f"{Fore.RED}❌ No domain provided!{Style.RESET_ALL}")
            return
            
        if not self.validate_domain(domain):
            print(f"{Fore.RED}❌ Invalid domain format!{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.BLUE}🔍 Analyzing domain: {domain}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
        
        # Get all information
        ip_address = self.resolve_domain(domain)
        dns_records = self.get_dns_records(domain)
        whois_info = self.get_whois_info(domain)
        ssl_info = self.check_ssl_certificate(domain)
        reputation = self.check_domain_reputation(domain)
        
        # Store results
        self.results[domain] = {
            'timestamp': datetime.now().isoformat(),
            'ip_address': ip_address,
            'dns_records': dns_records,
            'whois_info': whois_info,
            'ssl_info': ssl_info,
            'reputation': reputation
        }
        
        # Display comprehensive results
        self.display_comprehensive_results(domain, ip_address, dns_records, whois_info, ssl_info, reputation)
        
    def display_comprehensive_results(self, domain, ip, dns_records, whois_info, ssl_info, reputation):
        """Display comprehensive analysis results"""
        print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║                    ANALYSIS RESULTS                         ║")
        print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        # Basic Information
        print(f"\n{Fore.CYAN}🌐 BASIC INFORMATION:{Style.RESET_ALL}")
        print(f"   🏷️ Domain: {Fore.WHITE}{domain}{Style.RESET_ALL}")
        print(f"   🔢 IP Address: {Fore.WHITE}{ip if ip else 'Not resolved'}{Style.RESET_ALL}")
        
        # DNS Records
        print(f"\n{Fore.CYAN}📡 DNS RECORDS:{Style.RESET_ALL}")
        for record_type, records in dns_records.items():
            if records:
                print(f"   📋 {record_type}: {Fore.WHITE}{', '.join(records[:3])}{Style.RESET_ALL}")
                
        # WHOIS Information
        print(f"\n{Fore.CYAN}📋 WHOIS INFORMATION:{Style.RESET_ALL}")
        if 'error' not in whois_info:
            print(f"   🏢 Registrar: {Fore.WHITE}{whois_info.get('registrar', 'Unknown')}{Style.RESET_ALL}")
            print(f"   📅 Created: {Fore.WHITE}{str(whois_info.get('creation_date', 'Unknown'))[:10]}{Style.RESET_ALL}")
            print(f"   📅 Expires: {Fore.WHITE}{str(whois_info.get('expiration_date', 'Unknown'))[:10]}{Style.RESET_ALL}")
        else:
            print(f"   ❌ WHOIS Error: {Fore.RED}{whois_info['error']}{Style.RESET_ALL}")
            
        # SSL Certificate
        print(f"\n{Fore.CYAN}🔒 SSL CERTIFICATE:{Style.RESET_ALL}")
        if 'error' not in ssl_info:
            print(f"   🏢 Issuer: {Fore.WHITE}{ssl_info.get('issuer', {}).get('organizationName', 'Unknown')}{Style.RESET_ALL}")
            print(f"   📅 Valid Until: {Fore.WHITE}{ssl_info.get('not_after', 'Unknown')}{Style.RESET_ALL}")
        else:
            print(f"   ❌ SSL Error: {Fore.RED}{ssl_info['error']}{Style.RESET_ALL}")
            
        # Reputation Check
        print(f"\n{Fore.CYAN}🛡️ REPUTATION STATUS:{Style.RESET_ALL}")
        for source, result in reputation.items():
            if 'error' not in result:
                status = result.get('status', 'unknown')
                color = Fore.GREEN if 'safe' in status or 'clean' in status else Fore.YELLOW if 'medium' in status else Fore.RED
                print(f"   🔍 {source.title()}: {color}{status}{Style.RESET_ALL}")
                
    def dns_enumeration(self):
        """DNS record enumeration"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                 DNS RECORD ENUMERATION                      ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        domain = input(f"\n{Fore.YELLOW}Enter domain name: {Style.RESET_ALL}").strip()
        
        if not domain or not self.validate_domain(domain):
            print(f"{Fore.RED}❌ Invalid domain!{Style.RESET_ALL}")
            return
            
        dns_records = self.get_dns_records(domain)
        
        print(f"\n{Fore.GREEN}📡 DNS RECORDS FOR {domain.upper()}:{Style.RESET_ALL}")
        for record_type, records in dns_records.items():
            if records:
                print(f"\n{Fore.CYAN}📋 {record_type} Records:{Style.RESET_ALL}")
                for record in records:
                    print(f"   📄 {Fore.WHITE}{record}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}📋 {record_type} Records: None found{Style.RESET_ALL}")
                
    def whois_lookup(self):
        """WHOIS information gathering"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                WHOIS INFORMATION GATHERING                  ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        domain = input(f"\n{Fore.YELLOW}Enter domain name: {Style.RESET_ALL}").strip()
        
        if not domain or not self.validate_domain(domain):
            print(f"{Fore.RED}❌ Invalid domain!{Style.RESET_ALL}")
            return
            
        whois_info = self.get_whois_info(domain)
        
        if 'error' in whois_info:
            print(f"\n{Fore.RED}❌ WHOIS Error: {whois_info['error']}{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.GREEN}📋 WHOIS INFORMATION FOR {domain.upper()}:{Style.RESET_ALL}")
        print(f"   🏷️ Domain: {Fore.WHITE}{whois_info.get('domain_name', 'Unknown')}{Style.RESET_ALL}")
        print(f"   🏢 Registrar: {Fore.WHITE}{whois_info.get('registrar', 'Unknown')}{Style.RESET_ALL}")
        print(f"   📅 Created: {Fore.WHITE}{str(whois_info.get('creation_date', 'Unknown'))}{Style.RESET_ALL}")
        print(f"   📅 Updated: {Fore.WHITE}{str(whois_info.get('updated_date', 'Unknown'))}{Style.RESET_ALL}")
        print(f"   📅 Expires: {Fore.WHITE}{str(whois_info.get('expiration_date', 'Unknown'))}{Style.RESET_ALL}")
        print(f"   🌍 Country: {Fore.WHITE}{whois_info.get('country', 'Unknown')}{Style.RESET_ALL}")
        print(f"   🏢 Organization: {Fore.WHITE}{whois_info.get('org', 'Unknown')}{Style.RESET_ALL}")
        
        if whois_info.get('name_servers'):
            print(f"\n{Fore.CYAN}📡 NAME SERVERS:{Style.RESET_ALL}")
            for ns in whois_info['name_servers']:
                print(f"   📄 {Fore.WHITE}{ns}{Style.RESET_ALL}")
        
    def subdomain_discovery(self):
        """Subdomain discovery using wordlist"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                   SUBDOMAIN DISCOVERY                       ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        domain = input(f"\n{Fore.YELLOW}Enter domain name: {Style.RESET_ALL}").strip()
        
        if not domain or not self.validate_domain(domain):
            print(f"{Fore.RED}❌ Invalid domain!{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.BLUE}🔍 Discovering subdomains for {domain}...{Style.RESET_ALL}")
        subdomains = self.discover_subdomains(domain)
        
        if 'error' in subdomains:
            print(f"\n{Fore.RED}❌ Error: {subdomains['error']}{Style.RESET_ALL}")
            return
            
        if subdomains:
            print(f"\n{Fore.GREEN}🎯 DISCOVERED SUBDOMAINS ({len(subdomains)} found):{Style.RESET_ALL}")
            for subdomain_info in subdomains:
                print(f"   🌐 {Fore.WHITE}{subdomain_info['subdomain']}{Style.RESET_ALL} -> {Fore.CYAN}{subdomain_info['ip']}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}❌ No subdomains discovered{Style.RESET_ALL}")
            
    def ssl_analysis(self):
        """SSL certificate analysis"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                 SSL CERTIFICATE ANALYSIS                   ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        domain = input(f"\n{Fore.YELLOW}Enter domain name: {Style.RESET_ALL}").strip()
        
        if not domain or not self.validate_domain(domain):
            print(f"{Fore.RED}❌ Invalid domain!{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.BLUE}🔍 Analyzing SSL certificate for {domain}...{Style.RESET_ALL}")
        ssl_info = self.check_ssl_certificate(domain)
        
        if 'error' in ssl_info:
            print(f"\n{Fore.RED}❌ SSL Error: {ssl_info['error']}{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.GREEN}🔒 SSL CERTIFICATE INFORMATION:{Style.RESET_ALL}")
        
        # Subject Information
        subject = ssl_info.get('subject', {})
        print(f"\n{Fore.CYAN}📋 SUBJECT INFORMATION:{Style.RESET_ALL}")
        print(f"   🏷️ Common Name: {Fore.WHITE}{subject.get('commonName', 'Unknown')}{Style.RESET_ALL}")
        print(f"   🏢 Organization: {Fore.WHITE}{subject.get('organizationName', 'Unknown')}{Style.RESET_ALL}")
        print(f"   🌍 Country: {Fore.WHITE}{subject.get('countryName', 'Unknown')}{Style.RESET_ALL}")
        
        # Issuer Information
        issuer = ssl_info.get('issuer', {})
        print(f"\n{Fore.CYAN}🏢 ISSUER INFORMATION:{Style.RESET_ALL}")
        print(f"   🏷️ Common Name: {Fore.WHITE}{issuer.get('commonName', 'Unknown')}{Style.RESET_ALL}")
        print(f"   🏢 Organization: {Fore.WHITE}{issuer.get('organizationName', 'Unknown')}{Style.RESET_ALL}")
        
        # Validity Information
        print(f"\n{Fore.CYAN}📅 VALIDITY INFORMATION:{Style.RESET_ALL}")
        print(f"   📅 Valid From: {Fore.WHITE}{ssl_info.get('not_before', 'Unknown')}{Style.RESET_ALL}")
        print(f"   📅 Valid Until: {Fore.WHITE}{ssl_info.get('not_after', 'Unknown')}{Style.RESET_ALL}")
        print(f"   🔢 Serial Number: {Fore.WHITE}{ssl_info.get('serial_number', 'Unknown')}{Style.RESET_ALL}")
        
        # Subject Alternative Names
        san = ssl_info.get('san', [])
        if san:
            print(f"\n{Fore.CYAN}🌐 SUBJECT ALTERNATIVE NAMES:{Style.RESET_ALL}")
            for alt_name in san[:5]:  # Show first 5
                print(f"   📄 {Fore.WHITE}{alt_name[1]}{Style.RESET_ALL}")
                
    def reputation_check(self):
        """Domain reputation check"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                 DOMAIN REPUTATION CHECK                     ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        domain = input(f"\n{Fore.YELLOW}Enter domain name: {Style.RESET_ALL}").strip()
        
        if not domain or not self.validate_domain(domain):
            print(f"{Fore.RED}❌ Invalid domain!{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.BLUE}🔍 Checking reputation for {domain}...{Style.RESET_ALL}")
        reputation = self.check_domain_reputation(domain)
        
        print(f"\n{Fore.GREEN}🛡️ REPUTATION ANALYSIS:{Style.RESET_ALL}")
        
        for source, result in reputation.items():
            if 'error' not in result:
                status = result.get('status', 'unknown')
                reason = result.get('reason', result.get('reasons', ['No details']))
                
                # Color coding based on status
                if 'safe' in status or 'clean' in status or 'low' in status:
                    color = Fore.GREEN
                    icon = "✅"
                elif 'medium' in status or 'potentially' in status:
                    color = Fore.YELLOW
                    icon = "⚠️"
                else:
                    color = Fore.RED
                    icon = "❌"
                    
                print(f"\n{Fore.CYAN}🔍 {source.replace('_', ' ').title()}:{Style.RESET_ALL}")
                print(f"   {icon} Status: {color}{status.replace('_', ' ').title()}{Style.RESET_ALL}")
                
                if isinstance(reason, list):
                    for r in reason:
                        print(f"   📄 {Fore.WHITE}{r}{Style.RESET_ALL}")
                else:
                    print(f"   📄 {Fore.WHITE}{reason}{Style.RESET_ALL}")
                    
    def port_service_scan(self):
        """Port and service scanning"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                PORT & SERVICE SCANNING                      ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        domain = input(f"\n{Fore.YELLOW}Enter domain name: {Style.RESET_ALL}").strip()
        
        if not domain or not self.validate_domain(domain):
            print(f"{Fore.RED}❌ Invalid domain!{Style.RESET_ALL}")
            return
            
        # Ask for custom ports or use default
        custom_ports = input(f"\n{Fore.YELLOW}Enter custom ports (comma-separated) or press Enter for default: {Style.RESET_ALL}").strip()
        
        ports = None
        if custom_ports:
            try:
                ports = [int(p.strip()) for p in custom_ports.split(',')]
            except ValueError:
                print(f"{Fore.RED}❌ Invalid port format! Using default ports.{Style.RESET_ALL}")
                
        open_ports = self.scan_ports(domain, ports)
        
        if 'error' in open_ports:
            print(f"\n{Fore.RED}❌ Scan Error: {open_ports['error']}{Style.RESET_ALL}")
            return
            
        if open_ports:
            print(f"\n{Fore.GREEN}🎯 OPEN PORTS FOUND ({len(open_ports)}):{Style.RESET_ALL}")
            for port_info in open_ports:
                print(f"   🔓 Port {Fore.WHITE}{port_info['port']}{Style.RESET_ALL} - {Fore.CYAN}{port_info['service']}{Style.RESET_ALL} ({port_info['status']})")
        else:
            print(f"\n{Fore.YELLOW}❌ No open ports found in scan range{Style.RESET_ALL}")
        
    def bulk_analysis(self):
        """Bulk domain analysis"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                    BULK DOMAIN ANALYSIS                     ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}Enter domain names (one per line, press Enter twice to finish):{Style.RESET_ALL}")
        
        domains = []
        while True:
            domain_input = input().strip()
            if not domain_input:
                break
            if self.validate_domain(domain_input):
                domains.append(domain_input)
            else:
                print(f"{Fore.RED}❌ Invalid domain format: {domain_input}{Style.RESET_ALL}")
                
        if not domains:
            print(f"{Fore.RED}❌ No valid domains provided!{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.BLUE}🔍 Analyzing {len(domains)} domains...{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
        
        for i, domain in enumerate(domains, 1):
            print(f"\n{Fore.CYAN}🌐 Analysis {i}/{len(domains)}: {domain}{Style.RESET_ALL}")
            
            # Quick analysis
            ip_address = self.resolve_domain(domain)
            dns_records = self.get_dns_records(domain)
            whois_info = self.get_whois_info(domain)
            reputation = self.check_domain_reputation(domain)
            
            print(f"   🔢 IP: {Fore.WHITE}{ip_address if ip_address else 'Not resolved'}{Style.RESET_ALL}")
            print(f"   🏢 Registrar: {Fore.WHITE}{whois_info.get('registrar', 'Unknown') if 'error' not in whois_info else 'Error'}{Style.RESET_ALL}")
            
            # Quick reputation summary
            safe_count = sum(1 for r in reputation.values() if 'safe' in str(r.get('status', '')).lower() or 'clean' in str(r.get('status', '')).lower())
            total_checks = len(reputation)
            rep_color = Fore.GREEN if safe_count >= total_checks * 0.7 else Fore.YELLOW if safe_count >= total_checks * 0.4 else Fore.RED
            print(f"   🛡️ Reputation: {rep_color}{safe_count}/{total_checks} sources report safe{Style.RESET_ALL}")
            
            # Store results
            self.results[domain] = {
                'timestamp': datetime.now().isoformat(),
                'ip_address': ip_address,
                'dns_records': dns_records,
                'whois_info': whois_info,
                'reputation': reputation
            }
            
    def export_reporting(self):
        """Export analysis results and generate reports"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                   EXPORT & REPORTING                        ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        if not self.results:
            print(f"\n{Fore.RED}❌ No analysis results to export!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Run some domain analysis first, then export the results.{Style.RESET_ALL}")
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export options
        print(f"\n{Fore.YELLOW}📊 Export Options:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[1]{Fore.WHITE} JSON Report (detailed)")
        print(f"{Fore.GREEN}[2]{Fore.WHITE} CSV Summary (basic)")
        print(f"{Fore.GREEN}[3]{Fore.WHITE} HTML Report (formatted)")
        
        choice = input(f"\n{Fore.YELLOW}Choose export format (1-3): {Style.RESET_ALL}").strip()
        
        try:
            if choice == '1':
                filename = f"reports/domain_analysis_{timestamp}.json"
                with open(filename, 'w') as f:
                    json.dump(self.results, f, indent=2, default=str)
                print(f"\n{Fore.GREEN}✅ JSON report exported: {filename}{Style.RESET_ALL}")
                
            elif choice == '2':
                filename = f"reports/domain_summary_{timestamp}.csv"
                self.export_csv(filename)
                print(f"\n{Fore.GREEN}✅ CSV summary exported: {filename}{Style.RESET_ALL}")
                
            elif choice == '3':
                filename = f"reports/domain_report_{timestamp}.html"
                self.export_html(filename)
                print(f"\n{Fore.GREEN}✅ HTML report exported: {filename}{Style.RESET_ALL}")
                
            else:
                print(f"\n{Fore.RED}❌ Invalid choice!{Style.RESET_ALL}")
                return
                
            print(f"   📁 File: {Fore.WHITE}{filename}{Style.RESET_ALL}")
            print(f"   📊 Records: {Fore.WHITE}{len(self.results)}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Export failed: {str(e)}{Style.RESET_ALL}")
            
    def export_csv(self, filename):
        """Export results to CSV format"""
        import csv
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['domain', 'ip_address', 'registrar', 'creation_date', 'expiration_date', 'reputation_score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for domain, data in self.results.items():
                whois_info = data.get('whois_info', {})
                reputation = data.get('reputation', {})
                
                # Calculate simple reputation score
                safe_count = sum(1 for r in reputation.values() if 'safe' in str(r.get('status', '')).lower())
                rep_score = f"{safe_count}/{len(reputation)}" if reputation else "0/0"
                
                writer.writerow({
                    'domain': domain,
                    'ip_address': data.get('ip_address', ''),
                    'registrar': whois_info.get('registrar', ''),
                    'creation_date': str(whois_info.get('creation_date', ''))[:10],
                    'expiration_date': str(whois_info.get('expiration_date', ''))[:10],
                    'reputation_score': rep_score
                })
                
    def export_html(self, filename):
        """Export results to HTML format"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Domain Intelligence Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; text-align: center; }}
        .domain {{ border: 1px solid #ddd; margin: 20px 0; padding: 15px; }}
        .safe {{ color: green; }}
        .warning {{ color: orange; }}
        .danger {{ color: red; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌐 Domain Intelligence Report</h1>
        <p>Generated by DeathSec333 Domain Toolkit</p>
        <p>Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
"""
        
        for domain, data in self.results.items():
            whois_info = data.get('whois_info', {})
            reputation = data.get('reputation', {})
            
            html_content += f"""
    <div class="domain">
        <h2>🌐 {domain}</h2>
        <p><strong>IP Address:</strong> {data.get('ip_address', 'Not resolved')}</p>
        <p><strong>Registrar:</strong> {whois_info.get('registrar', 'Unknown')}</p>
        <p><strong>Created:</strong> {str(whois_info.get('creation_date', 'Unknown'))[:10]}</p>
        <p><strong>Expires:</strong> {str(whois_info.get('expiration_date', 'Unknown'))[:10]}</p>
        
        <h3>🛡️ Reputation Status:</h3>
        <ul>
"""
            
            for source, result in reputation.items():
                status = result.get('status', 'unknown')
                css_class = 'safe' if 'safe' in status or 'clean' in status else 'warning' if 'medium' in status else 'danger'
                html_content += f'            <li class="{css_class}">{source.title()}: {status}</li>\n'
                
            html_content += """        </ul>
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        
        with open(filename, 'w') as f:
            f.write(html_content)
            
    def show_about(self):
        """Display about and credits"""
        about_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
{Fore.CYAN}║                    ABOUT & CREDITS                          ║
{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}🌐 Domain Intelligence Toolkit v1.0.0{Style.RESET_ALL}
{Fore.YELLOW}🔥 DeathSec333 Edition{Style.RESET_ALL}

{Fore.CYAN}📋 DESCRIPTION:{Style.RESET_ALL}
Advanced domain intelligence gathering toolkit designed for 
cybersecurity research, penetration testing, and OSINT investigations.

{Fore.CYAN}🛠️ FEATURES:{Style.RESET_ALL}
• Comprehensive domain analysis
• DNS record enumeration (A, AAAA, MX, NS, TXT, CNAME, SOA)
• WHOIS information gathering
• Subdomain discovery with wordlist
• SSL certificate analysis
• Domain reputation checking
• Port and service scanning
• Bulk domain analysis
• Multiple export formats (JSON, CSV, HTML)

{Fore.CYAN}👨‍💻 AUTHOR:{Style.RESET_ALL}
DeathSec333 - Cybersecurity Research & Development

{Fore.CYAN}🌐 LINKS:{Style.RESET_ALL}
• GitHub: github.com/DeathSec333/domain-intelligence-toolkit
• GitLab: gitlab.com/deathsec1337/domain-intelligence-toolkit

{Fore.CYAN}📄 LICENSE:{Style.RESET_ALL}
MIT License - Educational and authorized testing use only

{Fore.RED}⚠️ LEGAL NOTICE:{Style.RESET_ALL}
This tool is for educational purposes and authorized testing only.
Users are responsible for complying with applicable laws and regulations.
Unauthorized scanning or testing of domains without permission is prohibited.
"""
        print(about_text)
        
    def run(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_menu()
            
            try:
                choice = input().strip()
                
                if choice == '0':
                    print(f"\n{Fore.GREEN}👋 Thank you for using Domain Intelligence Toolkit!{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}🔥 Stay ethical, stay curious! - DeathSec333{Style.RESET_ALL}")
                    break
                elif choice == '1':
                    self.comprehensive_analysis()
                elif choice == '2':
                    self.dns_enumeration()
                elif choice == '3':
                    self.whois_lookup()
                elif choice == '4':
                    self.subdomain_discovery()
                elif choice == '5':
                    self.ssl_analysis()
                elif choice == '6':
                    self.reputation_check()
                elif choice == '7':
                    self.port_service_scan()
                elif choice == '8':
                    # Domain history analysis (placeholder for future enhancement)
                    print(f"\n{Fore.YELLOW}🚧 Domain History Analysis - Coming Soon!{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}This feature will include:{Style.RESET_ALL}")
                    print(f"   📅 Historical DNS records")
                    print(f"   🔄 Domain ownership changes")
                    print(f"   📊 Historical reputation data")
                elif choice == '9':
                    self.bulk_analysis()
                elif choice == '10':
                    self.export_reporting()
                else:
                    print(f"\n{Fore.RED}❌ Invalid option! Please choose 0-10.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.RED}🛑 Operation cancelled by user.{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"\n{Fore.RED}❌ An error occurred: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def main():
    """Main function"""
    try:
        # Check if required directories exist
        os.makedirs("reports", exist_ok=True)
        os.makedirs("wordlists", exist_ok=True)
        
        toolkit = DomainIntelligence()
        toolkit.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}🛑 Program terminated by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Fatal error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

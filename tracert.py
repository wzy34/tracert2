import subprocess
import re
import requests
import folium

site = input("Enter the website: ")
print("Start to find IP locations, this may take a few minutes")
class IPTracer:
    def __init__(self):
        self.ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        self.ip_addresses = []
    def run_traceroute(self, site):
        result = subprocess.run(f"tracert {site}", shell=True, stdout=subprocess.PIPE, text=True)
        self.ip_addresses = re.findall(self.ip_pattern, result.stdout)
    def get_location(self, ip):
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json?token=505acf9b1383ec")
            response.raise_for_status()
            data = response.json()
            try:
              return data['loc'].split(',')
            except:
              return
        except requests.RequestException as e:
            print(f"Error fetching location for IP {ip}: {e}")
            return None
    def save_map(self):
        if not self.ip_addresses:
            print("No IP addresses found.")
            return
        first_location = self.get_location(self.ip_addresses[0])
        if not first_location:
            print("Could not get location for the first IP address.")
            return
        mymap = folium.Map(location=[float(first_location[0]), float(first_location[1])], zoom_start=2)
        for ip in self.ip_addresses:
            loc = self.get_location(ip)
            if loc:
                folium.Marker([float(loc[0]), float(loc[1])], popup=f"ip:{ip}, location:{loc[0]}, {loc[1]}").add_to(mymap)
        mymap.save("ip_map.html")
        print("Map saved as ip_map.html")
tracer = IPTracer()
tracer.run_traceroute(site)
tracer.save_map()
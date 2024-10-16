import requests

def get_ip_info():
    # Public API for IP information
    url = "https://ipapi.co/json/"
    
    try:
        # Fetch the IP information from ipapi.co
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        ip_info = response.json()

        # Display relevant information
        print("IP Address Information:\n")
        print(f"IP Address: {ip_info.get('ip')}")
        print(f"City: {ip_info.get('city')}")
        print(f"Region: {ip_info.get('region')}")
        print(f"Country: {ip_info.get('country_name')}")
        print(f"Latitude: {ip_info.get('latitude')}")
        print(f"Longitude: {ip_info.get('longitude')}")
        print(f"ISP: {ip_info.get('org')}")
        print(f"Timezone: {ip_info.get('timezone')}")
        print(f"Postal Code: {ip_info.get('postal')}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP information: {e}")

get_ip_info()

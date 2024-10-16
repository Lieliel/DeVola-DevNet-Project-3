import requests
import tkinter as tk
from tkinter import messagebox

def fetch_ip_info():
    url = "https://ipapi.co/json/"
    
    try:
        # Fetch the IP information from ipapi.co
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching IP information: {e}")
        return None

def display_ip_info():
    ip_info = fetch_ip_info()
    
    if ip_info:
        # Clear previous data
        for widget in info_frame.winfo_children():
            widget.destroy()
        
        # Display relevant information in a table format
        fields = [
            ("IP Address", ip_info.get('ip')),
            ("City", ip_info.get('city')),
            ("Region", ip_info.get('region')),
            ("Country", ip_info.get('country_name')),
            ("Latitude", ip_info.get('latitude')),
            ("Longitude", ip_info.get('longitude')),
            ("ISP", ip_info.get('org')),
            ("Timezone", ip_info.get('timezone')),
            ("Postal Code", ip_info.get('postal'))
        ]
        
        # Table headers
        tk.Label(info_frame, text="Field", font=('Arial', 12, 'bold'), width=20, anchor="w").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(info_frame, text="Information", font=('Arial', 12, 'bold'), width=40, anchor="w").grid(row=0, column=1, padx=10, pady=5)

        # Add the IP information to the GUI in a table format
        for i, (field, value) in enumerate(fields, start=1):
            tk.Label(info_frame, text=field, font=('Arial', 10), anchor="w").grid(row=i, column=0, padx=10, pady=2)
            tk.Label(info_frame, text=value, font=('Arial', 10), anchor="w").grid(row=i, column=1, padx=10, pady=2)

# Create the main window
root = tk.Tk()
root.title("IP Address Information")
root.geometry("500x400")

# Create a frame to hold the IP information table
info_frame = tk.Frame(root)
info_frame.pack(pady=20)

# Create a button to fetch and display the IP information
fetch_button = tk.Button(root, text="Fetch IP Information", font=('Arial', 12), command=display_ip_info)
fetch_button.pack(pady=10)

# Run the GUI application
root.mainloop()

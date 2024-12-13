import requests
from ttkbootstrap.constants import *
import time

# Replace with your ipinfo.io API token
API_TOKEN = "5d9a6ed2b14418"

# Function to fetch IP information using the ipinfo.io API
def fetch_ip_info(ip=None):
    # Use the provided IP or default to the user's public IP
    url = f"https://ipinfo.io/{ip if ip else 'json'}?token={API_TOKEN}"
    retries = 3  # Maximum number of retries
    backoff = 1  # Initial backoff in seconds

    for attempt in range(retries):
        try:
            # Send a request to the API to fetch IP details
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()  # Return the response in JSON format

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"Rate limit hit. Retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff
            else:
                print(f"HTTP Error {response.status_code}: {e}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching IP information: {e}")
            return None

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    # If all retries fail
    print("Failed to fetch IP information after multiple attempts.")
    return None

# Function to initialize and run the GUI
def run_gui():
    import ttkbootstrap as ttk

    # Create the main window with ttkbootstrap styling
    root = ttk.Window(themename="cosmo")  # Choose a modern theme
    root.title("IP Address Information")  # Set window title
    root.geometry("800x600")  # Set the window size
    root.resizable(False, False)  # Disable resizing

    # Header section
    header_frame = ttk.Frame(root, padding=(20, 10))
    header_frame.pack(fill="x")
    header_label = ttk.Label(header_frame, text="Public & Remote IP Address Information",
                             font='Arial 20 bold', anchor="center")
    header_label.pack()

    # Input field for entering a remote IP address
    input_frame = ttk.Frame(root, padding=(20, 10))
    input_frame.pack(fill="x")
    ip_label = ttk.Label(input_frame, text="Enter an IP Address (Optional):", font='Arial 12')
    ip_label.pack(side="left", padx=(0, 10))
    ip_entry = ttk.Entry(input_frame, width=30)
    ip_entry.pack(side="left", padx=(0, 10))
    ip_entry.insert(0, "")  # Default to an empty field

    # Fetch button (aligned with the input field)
    fetch_button = ttk.Button(input_frame, text="Fetch IP Information", bootstyle=PRIMARY)
    fetch_button.pack(side="left", padx=(10, 0))

    # Table section
    table_frame = ttk.Labelframe(root, text="IP Information", padding=(10, 5))
    table_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
    info_table = ttk.Treeview(table_frame, columns=("Field", "Value"), show="headings", height=12)
    info_table.heading("Field", text="Field")
    info_table.heading("Value", text="Value")
    info_table.column("Field", anchor="w", width=250)
    info_table.column("Value", anchor="w", width=500)
    info_table.pack(fill="both", expand=True)

    # Status bar section
    status_bar = ttk.Frame(root, padding=(10, 5))
    status_bar.pack(fill="x")
    status_label = ttk.Label(status_bar, text="", font='Arial 11 italic', anchor="center")
    status_label.pack()

    # Fetch and display information
    def display_ip_info():
        ip = ip_entry.get().strip()  # Get the entered IP address
        status_label.config(text="Fetching IP information...", bootstyle=INFO)
        root.update_idletasks()

        ip_info = fetch_ip_info(ip)
        if ip_info:
            for row in info_table.get_children():
                info_table.delete(row)

            fields = [
                ("IP Address", ip_info.get('ip')),
                ("Hostname", ip_info.get('hostname')),
                ("City", ip_info.get('city')),
                ("Region", ip_info.get('region')),
                ("Country", ip_info.get('country')),
                ("Latitude, Longitude", ip_info.get('loc')),
                ("Postal Code", ip_info.get('postal')),
                ("ISP", ip_info.get('org')),
                ("Timezone", ip_info.get('timezone')),
                ("Anycast", str(ip_info.get('anycast', False)))
            ]
            for field, value in fields:
                info_table.insert("", "end", values=(field, value))
            status_label.config(text=f"IP information fetched successfully for {ip or 'your public IP'}!", bootstyle=SUCCESS)
        else:
            status_label.config(text=f"Failed to fetch information for {ip or 'your public IP'}.", bootstyle=DANGER)

    # Attach button function
    fetch_button.config(command=display_ip_info)

    # Run the main event loop for the GUI application
    root.mainloop()

# Only run the GUI if this script is executed directly
if __name__ == "__main__":
    run_gui()

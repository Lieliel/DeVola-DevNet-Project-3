import requests
from ttkbootstrap.constants import *

# Replace with your ipinfo.io API token
API_TOKEN = "5d9a6ed2b14418"

# Function to fetch public IP information using the ipinfo.io API
def fetch_ip_info():
    url = f"https://ipinfo.io/json?token={API_TOKEN}"
    retries = 3  # Maximum number of retries
    backoff = 1  # Initial backoff in seconds

    for attempt in range(retries):
        try:
            # Send a request to the API to fetch the public IP details
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception if there is an HTTP error
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

    # If all retries fail, display a failure message
    print("Failed to fetch IP information after multiple attempts.")
    return None

# Function to initialize and run the GUI
def run_gui():
    import ttkbootstrap as ttk

    # Create the main window with ttkbootstrap styling
    root = ttk.Window(themename="litera")  # Choose a Windows-like theme
    root.title("IP Address Information")  # Set window title
    root.geometry("700x500")  # Set the window size to 700x500
    root.resizable(False, False)  # Disable window resizing

    # Header section
    header_frame = ttk.Frame(root, padding=(10, 5))
    header_frame.pack(fill="x")
    header_label = ttk.Label(header_frame, text="Public IP Address Information", font='Arial 18 bold', anchor="center")
    header_label.pack()

    # Action button section
    button_frame = ttk.Frame(root, padding=(10, 5))
    button_frame.pack(fill="x")

    # Fetch and display information
    def display_ip_info():
        status_label.config(text="Fetching IP information...", bootstyle=INFO)
        root.update_idletasks()

        ip_info = fetch_ip_info()
        if ip_info:
            for row in info_table.get_children():
                info_table.delete(row)

            fields = [
                ("IP Address", ip_info.get('ip')),
                ("City", ip_info.get('city')),
                ("Region", ip_info.get('region')),
                ("Country", ip_info.get('country')),
                ("Latitude, Longitude", ip_info.get('loc')),
                ("ISP", ip_info.get('org')),
                ("Timezone", ip_info.get('timezone')),
                ("Postal Code", ip_info.get('postal'))
            ]
            for field, value in fields:
                info_table.insert("", "end", values=(field, value))
            status_label.config(text="IP information fetched successfully!", bootstyle=SUCCESS)
        else:
            status_label.config(text="Failed to fetch IP information.", bootstyle=DANGER)

    fetch_button = ttk.Button(button_frame, text="Fetch IP Information", bootstyle=PRIMARY, command=display_ip_info)
    fetch_button.pack(pady=10)

    # Table section
    table_frame = ttk.Labelframe(root, text="IP Information", padding=(10, 5))
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)
    info_table = ttk.Treeview(table_frame, columns=("Field", "Value"), show="headings", height=10)
    info_table.heading("Field", text="Field")
    info_table.heading("Value", text="Value")
    info_table.column("Field", anchor="w", width=200)
    info_table.column("Value", anchor="w", width=400)
    info_table.pack(fill="both", expand=True)

    # Status bar section
    status_bar = ttk.Frame(root, padding=(10, 5))
    status_bar.pack(fill="x")
    status_label = ttk.Label(status_bar, text="", font='Arial 10 italic', anchor="w")
    status_label.pack()

    # Run the main event loop for the GUI application
    root.mainloop()

# Only run the GUI if this script is executed directly
if __name__ == "__main__":
    run_gui()
import tracker
import storage

def show_menu():
    """Displays the main menu to the user."""
    print("\n--- Manga Tracker Menu ---")
    print("1. Add a new series to track")
    print("2. Check for updates")
    print("3. Show currently tracked series")
    print("4. Exit")
    print("--------------------------")

def handle_add_new_series():
    """Prompts the user for details to add a new series."""
    site_name = input("Enter the site name (e.g., 'asuracomic', 'flame'): ").strip().lower()
    series_url = input("Enter the full URL of the series: ").strip()
    
    # Pass the user input to the tracker module
    tracker.add_new_series(site_name, series_url)

def handle_show_tracked_series():
    """Loads and displays the list of all series the user is tracking."""
    data = storage.load_data()
    if not data:
        print("You are not currently tracking any series.")
        return
        
    print("\n--- Your Tracked Series ---")
    for site_name, series_dict in data.items():
        print(f"[{site_name.capitalize()}]:")
        for title, info in series_dict.items():
            print(f"  - {title}")
            print(f"    - URL: {info['url']}")
            print(f"    - Last Checked Chapter: {info['last_chapter']}")
        
    print("----------------------------")

def main():
    """The main function that runs the application loop."""
    while True:
        show_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            handle_add_new_series()
        elif choice == '2':
            tracker.check_for_updates()
        elif choice == '3':
            handle_show_tracked_series()
        elif choice == '4':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

# This is the line that makes the program run
if __name__ == "__main__":
    main()
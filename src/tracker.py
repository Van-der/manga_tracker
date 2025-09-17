import importlib
import storage

def get_scraper_instance(site_name: str):
    """
    Dynamically imports and returns a scraper class instance for a given site.

    This allows the program to support new sites just by adding a new file
    to the 'scrapers' directory without changing this core logic.

    Args:
        site_name (str): The name of the scraper module (e.g., 'asuracomic').

    Returns:
        BaseScraper: An instance of the specific scraper class.
        Returns None if the scraper module or class is not found.
    """
    try:
        # Import the module dynamically based on the site_name
        module = importlib.import_module(f".scrapers.{site_name}", package="src")
        
        # Get the class from the module (e.g., AsuracomicScraper)
        # We assume the class name follows the pattern: SiteNameScraper
        class_name = f"{site_name.capitalize()}Scraper"
        scraper_class = getattr(module, class_name)
        
        # Return an instance of the scraper class
        return scraper_class()
    except (ImportError, AttributeError) as e:
        print(f"Error: Scraper for '{site_name}' not found. {e}")
        return None

def check_for_updates():
    """
    Checks all tracked series for new chapters and prints the updates.
    """
    print("Checking for new chapters...")
    # Load the user's tracked series from the local storage
    data = storage.load_data()
    updates_found = False

    # Iterate through each site the user is tracking
    for site_name, series_dict in data.items():
        # Get the correct scraper instance for this site
        scraper = get_scraper_instance(site_name)
        
        if not scraper:
            continue  # Skip if the scraper isn't found
        
        # Iterate through each series on this site
        for series_title, series_info in series_dict.items():
            series_url = series_info["url"]
            last_chapter = series_info["last_chapter"]
            
            print(f"  - Checking '{series_title}' on {site_name}...")
            
            # Use the scraper to get the latest chapter info
            latest_info = scraper.get_latest_chapter(series_url)
            
            if latest_info and latest_info["chapter_number"] > last_chapter:
                updates_found = True
                new_chapter = latest_info["chapter_number"]
                
                print(f"    ✅ NEW CHAPTER FOUND! {series_title} - Chapter {new_chapter}")
                print(f"       -> Link: {latest_info['chapter_url']}")
                
                # Update the last_chapter number in the data dictionary
                series_info["last_chapter"] = new_chapter
    
    # Save the updated data to the file
    if updates_found:
        storage.save_data(data)
    else:
        print("No new chapters found.")

def add_new_series(site_name: str, series_url: str):
    """
    Adds a new series to the tracked list.

    Args:
        site_name (str): The name of the scraper module (e.g., 'asuracomic').
        series_url (str): The URL of the series to track.
    """
    print(f"Adding new series from {site_name}...")
    scraper = get_scraper_instance(site_name)
    
    if not scraper:
        return
        
    latest_info = scraper.get_latest_chapter(series_url)
    
    if not latest_info:
        print("Could not retrieve series info. Please check the URL.")
        return
    
    # Load existing data
    data = storage.load_data()
    
    # Add a new entry for the site if it doesn't exist
    if site_name not in data:
        data[site_name] = {}
        
    # Add the series to the dictionary
    series_title = latest_info["title"]
    data[site_name][series_title] = {
        "url": series_url,
        "last_chapter": latest_info["chapter_number"]
    }
    
    # Save the updated data
    storage.save_data(data)
    print(f"Successfully added '{series_title}' to your tracker.")
import requests
from bs4 import BeautifulSoup


def login_session(username, password, login_url):
    # Create a session object
    session = requests.Session()

    # Send a POST request with login credentials
    login_data = {
        'username': username,
        'password': password
    }
    response = session.post(login_url, data=login_data)

    # Check if login was successful
    if response.status_code == 200:
        print("Login successful!")
        return session
    else:
        print("Failed to login. Status code:", response.status_code)
        return None


def scrape_search_results(url, session):
    # Check if session is valid
    if session is None:
        print("Session not logged in. Exiting.")
        return

    # Send a GET request to the URL
    response = session.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all search result items
        search_results = soup.find_all('div', class_='member-card')

        # Check if there are search results
        if len(search_results) == 0:
            print("No search results found.")
            return

        # Save search results to a text file
        with open('search_results.txt', 'w') as file:
            for result in search_results:
                name = result.find('h4').text.strip()
                email = result.find('a', class_='btn-email').get('href').split(':')[-1]
                cell_phone = result.find('span', class_='cellPhone').text.strip()
                initiation_year = result.find('span', class_='initiationYear').text.strip()
                birthday = result.find('span', class_='birthday').text.strip()
                # Write data to file
                file.write(f"Name: {name}\n")
                file.write(f"Email: {email}\n")
                file.write(f"Cell Phone: {cell_phone}\n")
                file.write(f"Initiation Year: {initiation_year}\n")
                file.write(f"Birthday: {birthday}\n\n")

        print("Search results saved to search_results.txt")

    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)


# Example usage
login_url = 'https://everyday.chiomega.com/Special-Pages/sign-in.aspx'
username = 'pelinich'
password = 'kcc199357'
url = 'https://everyday.chiomega.com/Interactive-Tools/Member-Search#%20/%20/%20/%20/%20/%20/%20/0041/%20/%20/%20/false/lastName/1/100/%20/false/%20/false'

# Login to get session
session = login_session(username, password, login_url)

# Scrape search results if login was successful
if session:
    scrape_search_results(url, session)

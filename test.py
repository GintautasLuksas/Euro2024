import csv
from selenium import webdriver
from selenium.webdriver.common.by import By


def scrape_team_names(url):
    # Set up Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get(url)

    # Find all team names using XPath targeting span elements with slot="primary"
    team_elements = driver.find_elements(By.XPATH, '//span[@slot="primary"]')

    team_names = [element.text for element in team_elements]

    # Close the WebDriver
    driver.quit()

    return team_names


def save_team_names_to_csv(team_names, filename):
    # Strings to exclude from the list of team names
    exclude_strings = [
        "UEFA Women's Under-17",
        "UEFA Under-19",
        "UEFA Under-17",
        "UEFA Regions' Cup",
        "UEFA Futsal Champions League",
        "UEFA Futsal EURO",
        "Futsal Finalissima",
        "UEFA Women's Futsal EURO",
        "UEFA U-19 Futsal EURO",
        "FIFA Futsal World Cup"
    ]

    # Clean team names: remove empty strings, unwanted text, and exclude_strings
    cleaned_team_names = [name for name in team_names if name.strip() and name not in exclude_strings]

    # Save team names to a CSV file
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Team Names'])
        csvwriter.writerows([[team] for team in cleaned_team_names])

    print(f"Team names saved to {filename}")


if __name__ == "__main__":
    url = 'https://www.uefa.com/euro2024/standings/'
    teams = scrape_team_names(url)

    if teams:
        print("List of teams:")
        for team in teams:
            print(team)

        csv_filename = 'uefa_team_names.csv'
        save_team_names_to_csv(teams, csv_filename)

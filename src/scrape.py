from selenium import webdriver
from selenium.webdriver.common.by import By
import csv


def scrape_team_data(url):
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        # Find all team names using XPath targeting span elements with slot="primary"
        team_elements = driver.find_elements(By.XPATH, '//span[@slot="primary"]')
        team_names = [element.text.strip() for element in team_elements]

        # Find all "played" values using the provided XPath
        played_elements = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div/div[3]/div[1]/div[2]/div/div[2]/div/pk-box[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[3]/div[1]/div[2]/div/div[3]/div[2]')
        played_values = [element.text.strip() for element in played_elements]

    except Exception as e:
        print(f"Exception occurred: {e}")
        team_names = []
        played_values = []

    finally:
        driver.quit()

    return team_names, played_values


def save_team_data_to_csv(team_names, played_values, filename):
    # Save team names and played values to a CSV file
    rows = zip(team_names, played_values)

    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Team Names', 'Played'])
        csvwriter.writerows(rows)

    print(f"Team data saved to {filename}")


if __name__ == "__main__":
    url = 'https://www.uefa.com/euro2024/standings/'
    team_names, played_values = scrape_team_data(url)

    if team_names and played_values:
        print("List of teams and their played values:")
        for team, played in zip(team_names, played_values):
            print(f"{team}: {played}")

        csv_filename = 'uefa_team_data.csv'
        save_team_data_to_csv(team_names, played_values, csv_filename)

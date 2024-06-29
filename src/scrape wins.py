from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


def scrape_team_statistics(url):
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        # Explicit wait for elements to be present
        wait = WebDriverWait(driver, 5)
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@role="presentation"]')))

        values = [element.text.strip() for element in elements]

        # Filter out non-numeric values
        numeric_values = []
        for value in values:
            try:
                num = int(value)
                numeric_values.append(num)
            except ValueError:
                continue

    except Exception as e:
        print(f"Exception occurred: {e}")
        numeric_values = []

    finally:
        driver.quit()

    return numeric_values


def organize_statistics(values, columns_per_team=8):
    num_teams = len(values) // columns_per_team
    organized_data = []
    for i in range(num_teams):
        start_index = i * columns_per_team
        end_index = start_index + columns_per_team
        team_data = values[start_index:end_index]
        organized_data.append(team_data)
    return organized_data


def save_to_csv(data, filename, headers):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(data)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    url = 'https://www.uefa.com/euro2024/standings/'
    stats_values = scrape_team_statistics(url)

    if stats_values:
        headers = ['Played', 'Won', 'Drawn', 'Lost', 'Goals For', 'Goals Against', 'Goal Difference', 'Points']
        organized_data = organize_statistics(stats_values)
        save_to_csv(organized_data, 'uefa_team_statistics.csv', headers)

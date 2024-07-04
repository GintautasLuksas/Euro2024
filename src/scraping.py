import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


def scrape_team_data(url):
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 12)

        # Scrape team names
        team_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@slot="primary"]')))
        team_names = []
        exclude_strings = [
            "UEFA Women's Under-17", "UEFA Under-19", "UEFA Under-17",
            "UEFA Regions' Cup", "UEFA Futsal Champions League",
            "UEFA Futsal EURO", "Futsal Finalissima",
            "UEFA Women's Futsal EURO", "UEFA U-19 Futsal EURO",
            "FIFA Futsal World Cup"
        ]
        for element in team_elements:
            try:
                team_name = element.text
                if team_name.strip() and team_name not in exclude_strings:
                    team_names.append(team_name)
            except StaleElementReferenceException:
                team_elements = driver.find_elements(By.XPATH, '//span[@slot="primary"]')
                team_name = team_elements[team_elements.index(element)].text
                if team_name.strip() and team_name not in exclude_strings:
                    team_names.append(team_name)

        stat_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@role="presentation"]')))
        stats_values = []
        for element in stat_elements:
            try:
                stats_values.append(int(element.text.strip()))
            except ValueError:
                continue
            except StaleElementReferenceException:
                stat_elements = driver.find_elements(By.XPATH, '//span[@role="presentation"]')
                try:
                    stats_values.append(int(stat_elements[stat_elements.index(element)].text.strip()))
                except ValueError:
                    continue

    except Exception as e:
        print(f"Exception occurred: {e}")
        team_names = []
        stats_values = []

    finally:
        driver.quit()

    return team_names, stats_values


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
    data_to_write = data[8:]

    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(data_to_write)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    url = 'https://www.uefa.com/euro2024/standings/'

    team_names, stats_values = scrape_team_data(url)

    if team_names and stats_values:
        organized_data = organize_statistics(stats_values)

        # Combine team names with statistics
        combined_data = []
        for i, team in enumerate(team_names):
            if i < len(organized_data):
                combined_data.append([team] + organized_data[i])
            else:
                combined_data.append([team] + [0] * 8)


        headers = ['Team', 'Played', 'Won', 'Drawn', 'Lost', 'Goals For', 'Goals Against', 'Goal Difference', 'Points']

        # Save combined data to CSV
        save_to_csv(combined_data, 'uefa_team_data.csv', headers)

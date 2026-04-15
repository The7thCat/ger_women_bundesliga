from match_data_class import *

def scrape_match_data(driver, By, WebDriverWait, EC, sleep):
    matchday_day = None
    # initializing saison instance
    season = Season()

    # Calc the nr of matchdays + label them
    def amount_of_matchdays_for_label():
        teams = 12
        amount_of_matchdays = (teams * 2) - 2

        list_of_matchday_numbers = [f"{n}. " + "Spieltag" for n in range(1, amount_of_matchdays + 1)]
        return list_of_matchday_numbers

    # select and open the dropdown
    def select_matchday_dropdown():
        try:
            matchday_labels = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//div[@class="module-select"]/select[contains(@class, "navigation")'
                                                ' and contains(@class, "round-navigation")]'))
            )

            matchday_labels.click()
        except Exception as e:
            print(f"Error extracting match details: {e}")

#TODO: write a func which grabs the current season

    # extracting a var
    def grab_day(day):
        global matchday_day
        matchday_day = day
        return matchday_day

    # iteration: matchday -> days of the matchday -> pairings on day of matchday
    def iterate_over_matchdays(list_of_matchday_numbers, scrape_matchday_entries):
        # alternative: driver.find_element(By.CSS_SELECTOR, "option[value*='spieltag/md1']")
        for day in list_of_matchday_numbers:
            try:
                select_matchday_dropdown()
                xpath = f'//option[text()="{day}"]'
                select_matchday_by_number = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                select_matchday_by_number.click()
                sleep(1)
                grab_day(day)
                scrape_matchday_entries()

            except:
                print(f"Matchday {day} not found.")

    # grabbing all relevant vars of the matchday

    def scrape_matchday_entries():
        try:
            matchday_number = matchday_day

            xpath_date = '//li[@class="hs-head hs-head--date hs-head--date date-head match-date"]/h4'
            date_elements = driver.find_elements(By.XPATH, xpath_date)
            dates = [dates.text for dates in date_elements]

            amount_of_dates = len(date_elements)

            #calculate range of matchday
            if amount_of_dates <= 1:
                matchday_range = f'{dates[0]}'
            else:
                matchday_range = f'{dates[0]} - {dates[-1]}'

            #sets inital counter for
            matchday_counter = 1

            # actual date is the one of the days of the current match day
            # find all days then iterate over em, extract vars from each day
            for actual_date in date_elements:  # date_elements_list:

                actual_date_xpath = f"//li[contains(@class, 'match') and contains(@class, 'match-{matchday_counter}')]"
                match_element = actual_date.find_element(By.XPATH, actual_date_xpath)

                home_team = match_element.find_element(By.XPATH, ".//div[contains(@class, 'team-name-home')]").text

                home_micro_name = driver.execute_script(
                    "return document.querySelector('.team-microname.team-microname-home').textContent")

                match_result_home = match_element.find_element(By.XPATH,
                                                               ".//div[contains(@class, 'match-result-home')]//div[contains(@class, 'match-result-0')]").text

                away_team = match_element.find_element(By.XPATH, ".//div[contains(@class, 'team-name-away')]").text

                away_micro_name = driver.execute_script(
                    "return document.querySelector('.team-microname.team-microname-away').textContent")

                match_result_away = match_element.find_element(By.XPATH,
                                                               ".//div[contains(@class, 'match-result-away')]//div[contains(@class, 'match-result-0')]").text

                match_time = driver.execute_script("return document.querySelector('.match-time').textContent")

                match_status = driver.execute_script("return document.querySelector('.match-status').textContent")
                match_pairing = f'{home_team} VS {away_team}'
                matchday_counter += 1

                if matchday_counter > amount_of_dates:
                    matchday_counter = 1

                #add matchday to data object
                matchday = Matchday(
                    matchday_number=matchday_number,
                    matchday_range=matchday_range
                )

                matchday.add_match(
                    home_team=home_team,
                    home_micro_name=home_micro_name,
                    match_result_home=match_result_home,
                    away_team=away_team,
                    away_micro_name=away_micro_name,
                    match_result_away=match_result_away,
                    match_time=match_time,
                    match_status=match_status,
                )


                # adds the matchday to the season list
                season.add_matchday(matchday)
                return matchday

        except Exception as e:
            print(f"Error extracting match details: {e}")

    # run the functions
    list_of_matchday_numbers = amount_of_matchdays_for_label()

    iterate_over_matchdays(list_of_matchday_numbers, scrape_matchday_entries)
    print(season) #debuging
    driver.quit()
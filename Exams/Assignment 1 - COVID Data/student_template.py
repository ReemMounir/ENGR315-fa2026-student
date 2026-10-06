import os
import sys

"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###

def analyze_county_data(file_path, target_counties):
    #parse the data from the NYT file
    records = parse_nyt_data(file_path)

    #organize the data for each county in the target_counties list
    county_data = {county: {} for county in target_counties}

    for row in records:
        date, county, state, fips, cases, deaths = row
        if state == "Virginia" and county in target_counties:
            county_data[county][date] = cases

    for county in target_counties:
        data_cases = county_data[county]
        if not data_cases:
            print(f"No data found for {county} in Virginia.")

        #sort the data by date
        sorted_data = sorted(data_cases.keys())

        #track number of cases 
        daily_new_cases = {}
        previous_cases = 0
        first_case_date = None

        for date in sorted_data:
            total_cases = data_cases[date]

            #answer question 1: first case date with a positive case
            if total_cases > 0 and first_case_date is None:
                first_case_date = date

            #find the number of new cases for the day
            new_cases = max(0, total_cases - previous_cases)
            daily_new_cases[date] = new_cases
            previous_cases = total_cases

        #answer question 2: date with the highest number of sinlge-day new cases
        max_single_day = max(sorted_data, key=lambda d: daily_new_cases[d])
        max_single_cases = daily_new_cases[max_single_day]

        #answer question 3: find the worst 7 day period for new cases
        max_seven_day_sum = -1
        worst_period_start = None
        worst_period_end = None

        for i in range(len(sorted_data) - 6):
            window_dates = sorted_data[i:i+7]
            window_sum = sum(daily_new_cases[d] for d in window_dates)
            if window_sum > max_seven_day_sum:
                max_seven_day_sum = window_sum
                worst_period_start = window_dates[0]
                worst_period_end = window_dates[-1]

        #print the results for the county
        print(f"--- analysis for {county}---")
        print(f"question 1: first case date with a positve case: {first_case_date}")
        print(f"question 2: date with the highest number of single-day new cases: {max_single_cases} cases on {max_single_day}")
        print(f"question 3: worst 7 day period for new cases: {worst_period_start} to {worst_period_end} (total: {max_seven_day_sum} new cases)")

    if __name__ == "__main__":
        #run the analysis on the specified counties in Virginia
        data_file = "us-counties.csv"
        counties_to_analyze = ["Harrisonburg", "Rockingham"]
        analyze_county_data(data_file, counties_to_analyze)   

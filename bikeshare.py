import pandas as pd
from datetime import datetime
from datetime import timedelta
import time

## Filenames
# chicago = 'chicago.csv'
# new_york_city = 'new_york_city.csv'
# washington = 'washington.csv'

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_city_name():
    '''Asks the user for a city and returns the filename for that city's bike share data.

       Args:
           none.
       Returns:
           (str) Filename for a city's bikeshare data.
       '''
    city = ''
    while city.lower() not in ['chicago', 'new york', 'washington']:
        city = input('\nPlease enter the city name Chicago or Washington or NewYork\n')
        if city.lower() == 'chicago':
            return 'chicago.csv'
        elif city.lower() == 'new york':
            return 'new_york_city.csv'
        elif city.lower() == 'washington':
            return 'washington.csv'
        else:
            print('Incorrect input. Please input either '
                  'Chicago, New York, or Washington.')


def get_time_period():
    '''Asks the user for a time period and returns the specified filter.

        Args:
            none.
        Returns:
            a string describing the user preference of filter of month, day or no filter for none
        '''
    time_period = ''
    while time_period.lower() not in ['month', 'day', 'none']:
        time_period = input('\nDo you want to filter the data  by month, day,'
                            ' or not at all? Type "none" if filter is not required.\n')
        if time_period.lower() not in ['month', 'day', 'none']:
            print('Incorrect Input')
    return time_period


def get_month_name():
    '''Asks the user for a month and returns the specified month.

       Args:
           none.
       Returns:
           (str) String representation of month for lower filter to the data frame
           9str) String representation of month for upper filter to the dataframe
       '''
    month_name = ''

    months_dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4,
                   'may': 5, 'june': 6}
    while month_name.lower() not in months_dict.keys():
        month_name = input('\nWhich month? Choose any month between January to June\n')
        if month_name.lower() not in months_dict.keys():
            print('Incorrect input. Please type in a '
                  'month between January and June')
    month = months_dict[month_name.lower()]
    return ('2017-{}'.format(month), '2017-{}'.format(month + 1))


def get_day_of_week():
    '''Asks the user for a day of a month and returns the specified day upper and lower filters

           Args:
               none.
           Returns:
               (str) String representation of particular day for lower filter to the data frame
               9str) String representation of particular day for upper filter to the dataframe
           '''
    this_month = get_month_name()[0]
    month = int(this_month[5:])
    valid_date = False
    while valid_date == False:
        is_int = False
        day = input(
            '\nWhich day? Please type your response as an integer for a particular day in a datetime fashion DD.\n')
        while is_int == False:
            try:
                day = int(day)
                is_int = True
            except ValueError:
                print('Sorry, I do not understand your input. Please type your'
                      ' response as an integer.')
                day = raw_input(
                    '\nWhich day? Please type your response as an integer for a particular day in a datetime fashion DD.\n')
        try:
            start_date = datetime(2017, month, day)
            valid_date = True
        except ValueError as e:
            print(str(e).capitalize())
    end_date = start_date + timedelta(days=1)
    return (str(start_date), str(end_date))


def popular_month(df):
    '''Finds and prints the most popular month for start time by taking bikeshare dataframe as input and calculates mode of the month in starttime
    data table.'''
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    index = int(df['start_time'].dt.month.mode())
    most_pop_month = months[index - 1]
    print('The most popular month is {}.'.format(most_pop_month))


def popular_day(df):
    '''Finds and prints the most popular day of week (Monday, Tuesday, etc.) for start time with bikeshare dataframe as input and
    calcualtes mode of the day of the week
    '''
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
    index = int(df['start_time'].dt.dayofweek.mode())
    most_pop_day = days_of_week[index]
    print('The most popular day of week for start time is {}.'.format(most_pop_day))


def popular_hour(df):
    '''Finds and prints the most popular hour of day for start time.
    '''
    most_pop_hour = int(df['start_time'].dt.hour.mode())
    if most_pop_hour == 0:
        am_pm = 'am'
        pop_hour_readable = 12
    elif 1 <= most_pop_hour < 13:
        am_pm = 'am'
        pop_hour_readable = most_pop_hour
    elif 13 <= most_pop_hour < 24:
        am_pm = 'pm'
        pop_hour_readable = most_pop_hour - 12
    print('The most popular hour of day for start time is {}{}.'.format(pop_hour_readable, am_pm))


def most_popular_stations(df):
    '''Finds and prints the most popular start station and most popular end station.'''
    common_start = df['start_station'].mode().to_string(index=False)
    common_end = df['end_station'].mode().to_string(index=False)
    print('The most common start station is {}.'.format(common_start))
    print('The most common end station is {}.'.format(common_end))


def most_common_trip(df):
    '''Finds and prints the most popular trip.'''
    most_pop_trip = df['journey'].mode().to_string(index=False)
    # The 'journey' column is created in the statistics() function.
    print('The most popular trip is {}.'.format(most_pop_trip))


def trip_duration(df):
    '''Finds and prints the total trip duration and average trip duration in
       hours, minutes, and seconds.
    '''
    total_duration = df['trip_duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print('The total trip duration is {} hours, {} minutes and {}'
          ' seconds.'.format(hour, minute, second))
    average_duration = round(df['trip_duration'].mean())
    m, s = divmod(average_duration, 60)
    if m > 60:
        h, m = divmod(m, 60)
        print('The average trip duration is {} hours, {} minutes and {}'
              ' seconds.'.format(h, m, s))
    else:
        print('The average trip duration is {} minutes and {} seconds.'.format(m, s))


def users(df):
    '''Finds and prints the counts of each user type.
    '''
    subscribers_count = df.query('user_type == "Subscriber"').user_type.count()
    customers_count = df.query('user_type == "Customer"').user_type.count()
    print('There are {} number of Subscribers and {} number of Customers.'.format(subscribers_count, customers_count))


def gender(df):
    '''Finds and prints the counts of gender.'''
    number_male = df.query('gender == "Male"').gender.count()
    number_female = df.query('gender == "Male"').gender.count()
    print('There are {} male users and {} female users.'.format(number_male, number_female))


def birth_years(df):
    ''' Finds and prints the earliest (i.e. oldest user), most recent (i.e.
        youngest user), and most popular birth years.'''
    earliest_born = int(df['birth_year'].min())
    latest_born = int(df['birth_year'].max())
    pop_birth_year = int(df['birth_year'].mode())
    print('The oldest users are born in {}.\nThe youngest users are born in {}.'
          '\nThe most popular birth year is {}.'.format(earliest_born, latest_born, pop_birth_year))


def run_statistics():
    '''Calculates and prints out the descriptive statistics about a city and
    time period specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''
    # Filter by city (Chicago, New York, Washington)
    city = get_city_name()
    print('Loading data...')
    df = pd.read_csv(city, parse_dates=['Start Time', 'End Time'])

    # change all column names to lowercase letters and replace spaces with underscores
    new_labels = []
    for col in df.columns:
        new_labels.append(col.replace(' ', '_').lower())
    df.columns = new_labels

    # increases the column width so that the long strings in the 'journey'
    # column can be displayed fully
    pd.set_option('max_colwidth', 100)

    # creates a 'journey' column that concatenates 'start_station' with
    # 'end_station' for the use popular_trip() function
    df['journey'] = df['start_station'].str.cat(df['end_station'], sep=' to ')

    # Filter by time period (month, day, none)
    time_period = get_time_period()
    if time_period == 'none':
        df_filtered = df
    elif time_period == 'month' or time_period == 'day':
        if time_period == 'month':
            filter_lower, filter_upper = get_month_name()
        elif time_period == 'day':
            filter_lower, filter_upper = get_day_of_week()
        print('Filtering data...')
        df_filtered = df[(df['start_time'] >= filter_lower) & (df['start_time'] < filter_upper)]
    print('\nCalculating the first statistic...')

    if time_period == 'none':
        start_time = time.time()

        # What is the most popular month for start time?
        popular_month(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")

    if time_period == 'none' or time_period == 'month':
        start_time = time.time()

        # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
        popular_day(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")


        # What is the most popular hour of day for start time?
    start_time = time.time()
    popular_hour(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the total trip duration and average trip duration?
    trip_duration(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the most popular start station and most popular end station?
    most_popular_stations(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the most popular trip?
    most_common_trip(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What are the counts of each user type?
    users(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))

    if city == 'chicago.csv' or city == 'new_york_city.csv':
        print("\nCalculating the next statistic...")
        start_time = time.time()

        # What are the counts of gender?
        gender(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        start_time = time.time()

        # What are the earliest (i.e. oldest user), most recent (i.e. youngest
        # user), and most popular birth years?
        birth_years(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))

    # Would you like to restart?
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    while restart.lower() not in ['yes', 'no']:
        print("Invalid input. Please type 'yes' or 'no'.")
        restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes':
        run_statistics()


if __name__ == "__main__":
    run_statistics()
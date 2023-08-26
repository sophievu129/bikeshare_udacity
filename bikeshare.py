"""Bikeshare explorer."""
import time
import pandas as pd
import json

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Ask user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
        or "all" to apply no month filter
        (str) day - name of the day of week to filter by,
        or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = ''
    while not city:
        city = input("What city would you like to check?"
                     " (Chicago, New York City, Washington)\n")
        city = city.strip().lower()
        if city in ("chicago", "new york city", "washington"):
            city = city.replace(" ", "_")
        elif city == "new york":
            city = "new_york_city"
        else:
            print("Please input only Chicago, New York City or Washington.")
            city = ''
    date_filter = ''
    months = ("all", "january", "february", "march",
              "april", "may", "june")
    weekdays = ("all", "sunday", "monday", "tuesday",
                "wednesday", "thursday", "friday", "saturday")

    while not date_filter:
        month_filter, day_filter = False, False
        date_filter = input("Would you like to filter the data by month,"
                            " day, both or not at all? Type \"none\" for"
                            " no time filter.\n")
        date_filter = date_filter.lower()
        if date_filter == "none":
            month = ''
            day = ''
        elif date_filter == "month":
            day = ''
            month_filter = True
        elif date_filter == "day":
            month = ''
            day_filter = True
        elif date_filter == "both":
            month_filter = True
            day_filter = True
        else:
            date_filter = ''
            print("Please input only 'month', 'day', 'both' or 'none'")
            continue

        while month_filter:
            month = input("Which month? (January, February, March, April,"
                          " May, June)\n")
            month = month.strip().lower()
            if month in months:
                break
            else:
                print("Please input only suggested month.")

        while day_filter:
            day = input("Which day? Please input a number."
                        " eg: 0 = all, 1 = Sunday, 2 = Monday, etc.\n")
            try:
                day = int(day)
                if day < 0 or day > 7:
                    print("Please input correct number. From 0 to 7.")
                else:
                    day = weekdays[day]
                    break
            except Exception:
                print("Must input a number!")

    print('-'*40)
    return city, month, day, date_filter


def load_data(city, month, day):
    """
    Load data for the specified city and filters.

    Filter by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
         or "all" to apply no month filter
        (str) day - name of the day of week to filter by,
         or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    file_name = city + '.csv'
    df = pd.read_csv(file_name)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')
    if month != 'all' and month != '':
        month = month.lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df.loc[df['month'] == month]
    if day != 'all' and day != '':
        day = day.title()
        df = df.loc[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Display statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    if data_filter != 'month' and data_filter != 'both':
        months = ["January", "February", "March", "April", "May", "June"]
        popular_month = df['month'].mode()[0]
        popular_month_str = months[popular_month-1]
        count_month = df[df['month'] == popular_month]['month'].count()
        print(f"Most common month is:\n"
              f"\t{popular_month_str}\n"
              f"\tCount: {count_month}\n"
              f"\tFilter: {data_filter}")
    if data_filter != 'day' and data_filter != 'both':
        popular_dow = df['day_of_week'].mode()[0]
        count_dow = df[df['day_of_week'] == popular_dow]['day_of_week'].count()
        print(f"Most common day of week is:\n"
              f"\t{popular_dow}\n"
              f"\tCount: {count_dow}\n"
              f"\tFilter: {data_filter}")

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    count_hour = df[df['hour'] == popular_hour]['hour'].count()
    print(f"Most common start hour is:\n"
          f"\t{popular_hour}\n"
          f"\tCount: {count_hour}\n"
          f"\tFilter: {data_filter}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df_start_station = df['Start Station'].mode()[0]
    count_start = df[df['Start '
                        'Station'] == df_start_station]['Start '
                                                        'Station'].count()
    popular_start_station = df_start_station
    print(f"Most commonly used start station:\n"
          f"\t{popular_start_station}\n"
          f"\tCount: {count_start}\n"
          f"\tFilter: {data_filter}")

    popular_end_station = df['End Station'].mode()[0]
    count_end = df[df['Start '
                      'Station'] == popular_end_station]['Start '
                                                         'Station'].count()
    print(f"Most commonly used end station is:\n"
          f"\t{popular_end_station}\n"
          f"\tCount: {count_end}\n"
          f"\tFilter: {data_filter}")

    popular_combination = df.groupby(['Start Station',
                                      'End Station']).size().idxmax()
    count_combination = df.groupby(['Start Station',
                                    'End Station']).size()[popular_combination]
    start, end = popular_combination
    print(f"Most popular trip is:\n"
          f"\tStart: {start}\n"
          f"\tEnd: {end}\n"
          f"\tCount: {count_combination}\n"
          f"\tFilter: {data_filter}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    count = df['Trip Duration'].count()
    average_duration = total_duration/count
    print(f"Trip duration:\n"
          f"\tTotal Duration: {total_duration}\n"
          f"\tCount: {count}\n"
          f"\tAverage Duration: {average_duration}\n"
          f"\tFilter {data_filter}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Display statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    msg = 'User types:\n'
    user_type_row = df.get("User Type", "not found")
    if str(user_type_row) != "not found":
        user_counts = dict(json.loads(user_type_row.value_counts().to_json()))
        for user, count in user_counts.items():
            msg += f"\t{user}: {count}\n"
        msg += f"\tFilter: {data_filter}"
        print(msg)

    # Display counts of gender
    msg = 'Gender:\n'
    gender_row = df.get("Gender", "not found")
    if str(gender_row) != "not found":
        gender_counts = dict(json.loads(gender_row.value_counts().to_json()))
        for gender, count in gender_counts.items():
            msg += f"\t{gender}: {count}\n"
        msg += f"\tFilter: {data_filter}"
        print(msg)

    # Display earliest, most recent, and most common year of birth
    birth_year = df.get("Birth Year", "not found")
    if str(birth_year) != "not found":
        earliest_year = df.min(axis='index', numeric_only=True)["Birth Year"]
        recent_year = df.max(axis='index', numeric_only=True)["Birth Year"]
        common_year = df["Birth Year"].mode()[0]
        print(f"Birth year:\n\tOldest: {earliest_year}\n"
              f"\tNewest: {recent_year}\n"
              f"\tMost common: {common_year}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """Bikeshare explorer application."""
    global data_filter
    while True:
        city, month, day, data_filter = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

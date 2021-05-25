import time
import pandas as pd
import numpy as np
import math

"""
This is a small project to showcase the power of python and it's most 
commonly used libraries. This program will take in a document of raw data,
 calculate some useful statistics, and produce results in a digestible format
 for users to see. Anyone should be able to run this program with python installed
 on their machine.
"""
# To run this program from this repository,
# First, make sure to have pip installed. use command |pip3 install pandas| to get libraries set up
# Then you must specify python3 in your python command.
# | python3 bikeshare_2.py |
# the above command will initiate the program, which will direct the user for prompts.

# city data holds our data frames
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# this list holds the months we have data for
VALID_MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

# this list is used as reference in calculations
VALID_DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city would you like to analyze?(chicago, new york city, washington): ").lower()
    while city not in CITY_DATA:
        print("Input Invalid")
        city = input("please choose from chicago, new york city, or washington. : ").lower()


    # get user input for month (all, january, february, ... , june)
    month = input("Which month would you like to analyze?\n Type out any month from january - june, or type 'all' for all months: ").lower()
    while month not in VALID_MONTHS:
        print("Input Invalid")
        month = input("Please choose a month between january and june, or type all. : ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day of the week would you like to analyze?\n Choose any day of the week, or type 'all' for all days. : ").lower()
    while day not in VALID_DAYS:
        print("Input Invalid")
        day = input("Please choose a day of the week, or type all. : ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # create data frame
    df = pd.read_csv(CITY_DATA[city])
    # convert time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # create month and day of week columns with datetime
    df['month'] = df['Start Time'].dt.month
    # weekday_name wasn't working, but dt.day_name() worked
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #create hour column to do time_stats faster
    df['hour'] = df['Start Time'].dt.hour

    #filter checks
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        # index of the month plus one since index starts at 0
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe, easier than month because it's by name
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""

    print(f'\nCalculating The Most Frequent Times of Travel for {city} ...\n')

    start_time = time.time()

    # These first two if statements save time, because
    # The user already filters based on these two things, so if they aren't examining all months,
    # There is no insights gained from this.

    # display the most common month
    if len(df['month'].unique()) > 1:
        print(f"The most popular month is: {VALID_MONTHS[df['month'].mode()[0]].title()}")

    # display the most common day of week
    if len(df['day_of_week'].unique()) > 1:
        print(f"The most popular day of the week is: {df['day_of_week'].mode()[0]}")

    # display the most common start hour

    print(f"The most common starting hour is: {df['hour'].mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"The most commonly used starting bike station is: {df['Start Station'].mode()[0]}\n")
    print(f"Here are the usage numbers for the top 5 starting stations:\n {df['Start Station'].value_counts()[:5]}")


    # display most commonly used end station
    print(f"\nThe most commonly used ending bike station is:\n {df['End Station'].mode()[0]}\n")
    print(f"Here are the usage numbers for the top 5 ending stations:\n {df['End Station'].value_counts()[:5]}")
   
   # display most frequent combination of start station and end station trip
    print(f"\n THe most commonly travelled route is {df.groupby(['Start Station', 'End Station']).size().idxmax()}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    seconds = df['Trip Duration'].sum()

    # in case the user inputs a small time frame, this function will compute the proper level of time to be output.
    # This function is defined within a function, because we are defining the variables to be used within the scope of the trip_duration_stats function.
    # scope matters!
    def time_calc(seconds):

        years = seconds / 60 / 60 / 24 / 365.25
        days = seconds / 60 / 60 / 24
        hours = seconds / 60 / 60
        minutes = seconds / 60

        
        if years > 1:
            days = (years - math.floor(years)) * 24
            hours = (days - math.floor(days)) * 60
            minutes = (hours - math.floor(hours)) * 60
            seconds = (minutes - math.floor(minutes)) * 60
            print(f"{math.floor(years)} years, {math.floor(days)} days, {math.floor(hours)} hours, {math.floor(minutes)} minutes, {seconds} seconds")
            

        elif days > 1:
            hours = (days - math.floor(days)) * 60
            minutes = (hours - math.floor(hours)) * 60
            seconds = (minutes - math.floor(minutes)) * 60
            print(f"{math.floor(days)} days, {math.floor(hours)} hours, {math.floor(minutes)} minutes, {seconds} seconds")
            

        elif hours > 1:
            minutes = (hours - math.floor(hours)) * 60
            seconds = (minutes - math.floor(minutes)) * 60
            print(f"{math.floor(hours)} hours, {math.floor(minutes)} minutes, {seconds} seconds")

        else:
            seconds = (minutes - math.floor(minutes)) * 60
            print(f"{math.floor(minutes)} minutes, {seconds} seconds")


    print('\nCalculating Trip Duration Stats...\n')
    start_time = time.time()

    # display total travel time
    print("For the chosen city and time frame, we spent a total of:\n")
    print(time_calc(seconds))
    print("\nriding bikes!\n")

    # display mean travel time

    print("The average travel time for one trip is:\n")
    print(time_calc(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # wrapping this in a try/except lets us handle washington by returning a "sorry" message.

    try:
        # Display counts of user types

        print(f"The user types were: \n{df['User Type'].value_counts()}")

        # Display counts of gender

        print(f"The user genders were: \n{df['Gender'].value_counts()}")


        # Display earliest, most recent, and most common year of birth
        print(f"The earliest year of birth among users is: \n{int(df['Birth Year'].min())}\n")
        print(f"|The most recent year of birth among users is: \n{int(df['Birth Year'].max())}\n")
        print(f"The most common year of birth among users is: \n{int(df['Birth Year'].mode()[0])}\n")

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except:
        print('\n Sorry, this city has no other user information available!\n')

def display_raw_data(df):
    """Displays the dataframe for the chosen city, printing 5 lines at a time."""
    i = 0
    ie = 4

    raw = input(f"\n Type yes to see the first 5 records, type no to exit. \n")

    # This will make it so that we output all of the results we want.
    pd.set_option('display.max_columns',200)


    while True:
        if raw.lower() =='no':
            break
        elif raw.lower() == 'yes':
            print(df[i:ie])
            raw = input("Would you like to view the next 5 rows?")

            i += 5
            ie += 5

        else:
            raw = input("\nYour input is invalid. Please enter either 'yes' or 'no'.\n")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        valid_restart = ['yes', 'no']

        # We can ask users if they'd like to see raw data either before the statistics, or after.
        # Assuming that they use this program to gain some sort of insight, it's reasonable to assume they want stats first
        # and if they want to dig deeper, they can view the raw data afterwards to browse deeper.

        # Stats portion
        # we can either print stats by section, or all in one shot.
        # typing yes here will print all stats in one shot, and ask if you want to restart.
        all_stats = input('\nIf you want to print all stats at once, type yes. Otherwise, press enter\n to continue to see time-based stats.\n')
        # if you don't type yes, then the program starts with time stats, and asks before sending each continuing section.
        if all_stats.lower() != 'yes':
            print("\nTo start, here are some time-based statistics\n")
            time_stats(df, city)

            cont_stats = input('\nTo show station-based stats, type yes. Other input will skip this portion. \n')
            if cont_stats.lower() == 'yes':
                print(f"\n{station_stats(df)}\n")

            cont_stats = input('\nTo show trip duration stats, type yes. Other input will skip this portion. \n')
            if cont_stats.lower() == 'yes':
                print(f"\n{trip_duration_stats(df)}")

            cont_stats = input('\nTo show user base stats, type yes. Other input will skip this portion. \n')
            if cont_stats.lower() == 'yes':
            	print(f"\n{user_stats(df)}")

            raw_ask = input("\n That's all of the data we have! Would you like to view the raw data?\n Type 'yes' to view raw data, all other input will skip this.\n")
            if raw_ask.lower() == 'yes':
                print(f"\n{display_raw_data(df)}")

            restart = input('\nThis is the end of the program. To restart, type "yes". Type "no" to quit. \n')
            while restart not in valid_restart:
            	print("Not valid Input")
            	restart = input('\nYou reached the end of this program! To restart, type "yes". Type "no" to quit. \n')
            if restart.lower() != 'yes':
                break

        else:
            print("\n\n\n")
            time_stats(df,city)
            print("\n\n\n")
            station_stats(df)
            print("\n\n\n")
            trip_duration_stats(df)
            print("\n\n\n")
            user_stats(df)
            raw_ask = input("\n That's all of the data we have! Would you like to view the raw data?\n Type 'yes' to view raw data, all other input will skip this. \n")
            if raw_ask.lower() == 'yes':
                print(f"\n{display_raw_data(df)}")

        if all_stats.lower() == 'yes':
            restart = input('\nThis is the end of the program. To restart, type "yes". Type "no" to quit. \n')
            while restart not in valid_restart:
            	print("Not valid Input")
            	restart = input('\nYou reached the end of this program! To restart, type "yes". Type "no" to quit. \n')
            if restart.lower() != 'yes':
                break

# use this to initiate the main loop for the program
if __name__ == "__main__":
	main()

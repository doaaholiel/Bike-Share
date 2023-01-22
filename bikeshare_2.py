import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months =['january','february','march','april','may','june']
days = ['saturday', 'sunday', 'monday', 'tuesday','wensday','thursday','friday']
        
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "" to apply no month filter
        (str) day - name of the day of week to filter by, or "" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York City or Washington?\n').lower().strip()
    while city not in CITY_DATA:
        city = input('Invalid input, please try again.\n').lower().strip()
    
    # get user input for month (all, january, february, ... , june)
    time_filter = input('Would you like to filter the data by month, day, both or not at all ? Type "none" for no time filter.\n').lower().strip()
    while time_filter not in ['month','day','both','none']:
        time_filter = input('Invalid filter! \nWould you like to filter the data by month, day, both or not at all ? Type "none" for no time filter.\n').lower().strip()
          
    month =''
    day =''

    if time_filter == 'month' or time_filter == 'both':
        month = input('Which month? January, February, March, April, May or June ? Please type out the full month name.\n').lower().strip()
        
        while month not in months:
            month = input('Invalid input, please try again.\n').lower().strip()
        
        month = str(months.index(month) + 1)
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if time_filter == 'day' or time_filter == 'both':
        day = input('Which day? Saturday, Sunday, Monday, Tuesday, Wensday, Thursday or Friday ? Please type out the full day name.\n').lower().strip()
        
        while day not in days:
            day = input('Invalid input, please try again.\n').lower().strip()
        

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "" to apply no month filter
        (str) day - name of the day of week to filter by, or "" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from the Start Time column to create an Month column
    df['Month'] = df['Start Time'].dt.month

    # extract day from the Start Time column to create an Day column
    df['Day'] = df['Start Time'].dt.day_name()

    # extract hour from the Start Time column to create an Hour column
    df['Hour'] = df['Start Time'].dt.hour
     
     # create Start_End Station trip column
    df['Trip'] = df['Start Station'] + ' -- ' + df['End Station']
   
    # filter by month if applicable
    if month != '':
        # filter by month to create the new dataframe
        df = df[df['Month'] == int(month)] 
     # filter by day of week if applicable    
    if day != '':
        # filter by day of week to create the new dataframe
        df = df[df['Day'] == day.title()]
    
    return df


def time_stats(df, month, day):
   
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (dataframe) df - dataframe that will calaculate stats on
        (str) month - name of the month to filter by, or "" to apply no month filter
        (str) day - name of the day of week to filter by, or "" to apply no day filter
    
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month when no filter by month
    if month =='':
        most_common_month = months[int(df['Month'].mode()[0]) -1].title()
        print('\nThe most common month: ',most_common_month ,',Count: ',df['Month'].value_counts().max())
   
    # display the most common day of week when no filter by day
    if day == '':       
        print('\nThe most common day of week: ' , df['Day'].mode()[0] ,',Count: ',df['Day'].value_counts().max())

    # display the most common start hour
    print('\nThe most common start hour: ' , df['Hour'].mode()[0] ,',Count: ',df['Hour'].value_counts().max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (dataframe) df - dataframe that will calaculate stats on
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nThe most commonly used start station:\n ' , df['Start Station'].mode()[0] ,',Count: ',df['Start Station'].value_counts().max())

    # display most commonly used end station
    print('\nThe most commonly used end station:\n ' , df['End Station'].mode()[0] ,',Count: ',df['End Station'].value_counts().max())

    # display most frequent combination of start station and end station trip
    print('\nThe most frequent combination of start station and end station trip:\n ' , df['Trip'].mode()[0] ,',Count: ',df['Trip'].value_counts().max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        (dataframe) df - dataframe that will calaculate stats on
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nTotal travel time: ',df['Trip Duration'].sum())   

    # display mean travel time
    print('\nAverage travel time: ',df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users. 

    Args:
        (dataframe) df - dataframe that will calaculate stats on
    """ 

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts().to_string()
    print('\nCounts of User Types:\n ',user_types_counts)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts().to_string()
        print('\nCounts of Gender:\n ',gender_counts)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_bd = df['Birth Year'].min()
        print('\nEarliest year of birth: ',int(earliest_bd))

        most_recent_bd = df['Birth Year'].max()
        print('\nMost recent year of birth: ',int(most_recent_bd))

        most_common_bd = df['Birth Year'].mode()[0]
        print('\nMost common year of birth: ',int(most_common_bd))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_row_data(city):
    """
    Displays sample of bikeshare row data for city selected by user.

    Args:
        (str) city - name of the city to get sample from.
    """   
    redisplay = input('\nWould you like to see sample of row data? Enter yes or no.\n')       
    while redisplay.lower() == 'yes':
        # load data file into a dataframe
        df = pd.read_csv(CITY_DATA[city])

        # get sample of 5 rows from dataframe
        df = df.sample(n=5)
        # display sample of row data
        print('\nSample row data:\n ',df)

        redisplay = input('\nWould you like to see another sample of row data? Enter yes or no.\n')           
        if redisplay.lower() != 'yes':
            break  

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty == False:         
            time_stats(df,month,day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_row_data(city)
            
        else:
            no_data_msg = "No data available for {city_}{month_}{day_}.".format(city_=city.title(),day_=", Day: "  + day.title() if day !=''else '',month_=" on Month: " + months[int(month)-1].title() if month != '' else '')
            print(no_data_msg)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
                break

if __name__ == "__main__":
	main()

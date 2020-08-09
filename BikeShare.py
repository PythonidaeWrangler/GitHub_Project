
import time
import pandas as pd
import numpy as np





CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }





def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please enter the city you would like to explore from Chicago, Washington or New York City?').title()
    cities = ['Chicago','New York City','Washington']
    while True:
        if city in cities:
            break
        else:
            city = input('Please enter a valid city by entering one of the following - Chicago, Washington or New York City')
            
    # get user input for month (all, january, february, ... , june)
    print('\n')
    print('\n')
    print(f'Great! You have chosen to view data for {city}')
    print('\n')
    month = input("What month from January to June would you like to view data for?\nIf you would like to view data for all months please enter 'Y'").title()
    months = ['January','February','March','April','May','June','Y']
    while True:
        if month in months:
            break
        else:
            month = input("Please enter a valid month from January to June.\n If you want to see data for all months then enter 'Y'")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('\n')
    if month.lower() != 'y':
        x = (f'Okay, you want to view {city} for the month of {month}')
    else:
        x = (f'Okay, you want to view {city} for all months')
    
    print(x)
    print('\n')                     
    day = input("Finally, what day, Monday to Sunday, would you like to filter the data by?\nIf you want to see all days please enter 'Y'").title()
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Y']
    print('\n')
    while True:
        if day in days:
            break
        else:
            day = input("Please enter a valid day from Monday to Sunday or select 'Y' if you want to see data for all days")
    print('\n')
    if day.lower() != 'y':
    
        print(x + ' ' + f'and you would like to filter on {day}')
    else:
        print(x + ' ' + 'and you would like to see data for all days')
    print('\n')
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
    df = pd.read_csv(CITY_DATA[city])
    
    df['Month'] = pd.to_datetime(df['Start Time']).apply(lambda x : x.month)
    month_dict = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June'}
    df.Month = df.Month.map(month_dict)

    df['Hour'] = pd.to_datetime(df['Start Time']).apply(lambda x : x.hour)

    df['Day'] = pd.to_datetime(df['Start Time']).apply(lambda x : x.dayofweek)
    day_dict = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
    df.Day = df.Day.map(day_dict)
    
    if day == 'Y' and month == 'Y':
        df = df.copy()
    elif day == 'Y':
        df = df[df.Month==month]
    elif month =='Y':
        df = df[df.Day==day]
    else:
        df = df[(df.Month==month) & (df.Day == day)]
    
    return df


# In[ ]:


def time_stats(df):
    """Displays stats on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = (df.Month.value_counts().iloc[[0]].index.item(),df.Month.value_counts().iloc[[0]][0])
    print(f'The most popular month is {popular_month[0]}, with a count of {popular_month[1]}')
    
    # display the most common day of week
    popular_day = (df.Day.value_counts().iloc[[0]].index.item(),df.Day.value_counts().iloc[[0]][0])
    print(f'The most popular day is {popular_day[0]}, with a count of {popular_day[1]}')
    # display the most common start hour
    popular_hour = (df.Hour.value_counts().iloc[[0]].index.item(),df.Hour.value_counts().iloc[[0]].item())
    print(f'The most popular start hour is {popular_hour[0]}:00, with a count of {popular_hour[1]}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def station_stats(df):
    """Displays stats on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    popular_start = (df['Start Station'].value_counts().iloc[[0]].index.item(),df['Start Station'].value_counts().iloc[[0]][0])
    popular_end = (df['End Station'].value_counts().iloc[[0]].index.item(),df['End Station'].value_counts().iloc[[0]][0])

    df['Start_End'] = df['Start Station'] + ' + ' + df['End Station']

    stations = df['Start_End'].value_counts().iloc[[0]].index.item()
    value = df['Start_End'].value_counts().iloc[[0]][0]
    start = stations.split('+')[0].strip()
    end = stations.split('+')[1].strip()
    # display most commonly used start station
    print(f'The most popular start station is {popular_start[0]} with a count of {popular_start[1]}')

    # display most commonly used end station
    print('\n')
    print(f'The most popular end station is {popular_end[0]} with a count of {popular_end[1]}')

    # display most frequent combination of start station and end station trip
    print('\n')
    print(f'The most popular combination of start and end stations is.....\n{start} and {end} with a count of {value}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def trip_duration_stats(df):
    """Displays stats on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['time_start'] = pd.to_datetime(df['Start Time'])
    df['time_end'] = pd.to_datetime(df['End Time'])
    df['duration'] = (df['time_end'] - df['time_start'])

    avg_travel = df['duration'].mean()
    total_travel = df['duration'].sum()
    # display total travel time
    print('\n')
    print(f'The total travel time is {total_travel}')
    
    # display mean travel time
    print('\n')
    print(f'The average travel time is {avg_travel}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def user_stats(df,city):
    """Displays stats on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    users_counts = df['User Type'].value_counts()
    
    # Display counts of user types
    
    print(f'The counts by user are \n{users_counts}')
    print('\n')
    
    # Display counts of gender
    
    if city != 'Washington':
        gender_counts = df['Gender'].value_counts()
        print(f'The counts by gender are \n{gender_counts}')
    else:
        print('\n')
        print('There is no gender data available for Washington')

    # Display earliest, most recent, and most common year of birth
    
    if city != 'Washington':
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        mode = df['Birth Year'].mode().item()
        print('\n')
        print(f'The earliest birth was in {int(earliest)}')
        print('\n')
        print(f'The most recent birth was in {int(most_recent)}')
        print('\n')
        print(f'The most common birth year is {int(mode)}')
        print('\n')
        print('\n')
    else:
        print('\n')
        print('There is no birth year information for Washington')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
              
        while True:
            num_yes = []
            x = input("Would you like to see individual trip data? Enter 'Yes' or 'No'")
            if x.title() == "Yes":
                while True:
                    num_yes.append(x)
                    to_print = len(num_yes*5)
                    print(df.iloc[(to_print -5):(to_print)])
                    x = input("Would you like to view the next five rows of trip data? Enter 'Yes' or 'No'")
                    if x.title() == 'No':
                        break
            break
        
        restart = input('\nWould you like to restart? Enter Yes or No.\n')
        if restart.lower() != 'yes':
            break


# In[ ]:


if __name__ == "__main__":
    main()


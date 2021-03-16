#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
95-888 Data Focused Python Final Project

@author: Pandas-Siyuan Liu
"""

from justwatch import JustWatch
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import twitter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image

'''
# This function takes the name of the movie to
# gets twitter data and plots the wordcloud

# Parameters
# ----------
# name : string of movie name

# Returns
# -------
# wordcloud graph
'''
def show_cloud_word(name):
    
    api = twitter.Api(consumer_key = "ZKohWx0NE4Cq4hz4xB7dtbZ6h",
                  consumer_secret = "PcGpXnmJPZgfA32hDX83VNS7SV0TOA4ixXAvDxf9sIesFnkSFY",
                  access_token_key = "1334946510476197889-3KlLfg8VR5yr1BtkyrXIecjrCWQe6f",
                  access_token_secret = "AOq8YUpcOWJ6NnLtIF9le1u9bzdQBHrjj4BecJCAxigGn")
    
    result = api.GetSearch(name, lang = "en-us", count = 100)

    tweets = ""
    for i in result:
        tweets = tweets + i.text + " "

    stopwords = set(STOPWORDS)
    stop_list = [name]
    stop_list.append("movie")
    stop_list.append("https")
    stop_list.append("screen")
    stop_list.append("see")
    stop_list.append("theatres")
    
    stopwords.update(stop_list)

    mask = np.array(Image.open('movie.png'))
   
    wc = WordCloud(background_color="white", max_words=2000, mask=mask,
               stopwords=stopwords, contour_width=3, contour_color='steelblue')

    wc.generate(tweets)


    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    #plt.show()
    plt.savefig('word-cloud.jpg')
'''
# This function will get the providers' table from JustWatch API.

# Returns
# -------
# dataframe of providers' information
'''
def get_jw_providers():
    just_watch = JustWatch()
    results = just_watch.get_providers()
    providers = []
    for i in results:
        providers.append([i['id'], i['short_name'], i['clear_name'], i['monetization_types']])
    
    return pd.DataFrame(providers, columns = ['id', 'short_name', "clear_name", "monetization_types"])

'''
# This function use movie name and release year to find detail in the movies.csv data.

# Parameters
# ----------
# name : string of movie name
# year : integer of movie release year

# Returns
# -------
# a list of details if found, none if not found

'''
def loadMovies(name,year):

    moviesInfo = pd.read_csv('movies.csv')
    movies_basic = moviesInfo[['title','year','genre','avg_vote','director','actors','description']].copy()
    
    t = movies_basic[movies_basic['title'].str.lower() == name.lower()]
    t = t[t['year'] == year]
    if(len(t) > 0):
        #print('found')
        rating = t.avg_vote
        director = t.director
        actors = t.actors
        genre = t.genre
        description = t.description
        #print(rating,director, genre, description)
        return [rating, director, actors, genre, description]
        
    return None

    
'''
# This function get movie details from JustWatch API.

# Parameters
# ----------
# name : string of movie name

# Returns
# -------
# a dataframe of movie details

'''
def get_jw_movies(name):
    just_watch = JustWatch(country = 'US')
    results = just_watch.search_for_item(query=name)
    movies = []
    for i in results['items']:
        if re.search(r'\b'+ name, i['title'].lower()) != None:
            movie = []
            movie.append(i['title'])
            if ('original_release_year' in i):
                movie.append(i['original_release_year'])
            else:
                movie.append("")
                
            if ('tmdb_popularity' in i):
                movie.append(i['tmdb_popularity'])
            else:
                movie.append("")
                
            if ('scoring' in i):
                movie.append(i['scoring'])
            else:
                movie.append("") 
            
            if ('localized_release_date' in i):
                movie.append(i['localized_release_date'])
            else:
                movie.append("")
            
            if ('cinema_release_date' in i):
                movie.append(i['cinema_release_date'])
            else:
                movie.append("")
            
            if ('offers' in i):
                movie.append(i['offers'])
            else:
                movie.append("")
                
            movies.append(movie)
            
    return pd.DataFrame(movies, columns = ['title', 'original_release_year', 'tmdb_popularity', 'scoring', 'localized_release_date', 'cinema_release_date','offers'])
    
'''
# This function tabulate the offering information of a particular movie and match the 
# providers' table to find the name of the provider.

# Parameters
# ----------
# offers : json string of offers of the movie

# Returns
# -------
# dataframe of the price of the movie's different offers

'''
def get_jw_price(offers):
    
    providers = get_jw_providers()
    prices = []
    for i in offers:
        price = []
        price.append(i['monetization_type'])
        price.append(i['provider_id'])
        
        if ('retail_price' in i):
            price.append(i['retail_price'])
        else:
            price.append("")
            
        if ('currency' in i):
            price.append(i['currency'])
        else:
            price.append("")
        
        if ('urls' in i):
            price.append(i['urls']['standard_web'])
        else:
            price.append("")
            
        if ('presentation_type' in i):
            price.append(i['presentation_type'])
        else:
            price.append("")
            
        prices.append(price)
        
    prices_table = pd.DataFrame(prices, columns = ['monetization_type', 'provider_id', 'retail_price', 'currency', 'urls', 'presentation_type'])
    new_df = pd.merge(prices_table, providers, how='inner', left_on='provider_id', right_on='id')
    return new_df[['monetization_type','clear_name','retail_price', 'currency', 'presentation_type', 'urls']]


'''
# This function will filter out the rent offers of the movie. 

# Parameters
# ----------
# prices : dataframe of the prices of the movie

# Returns
# -------
# dataframe of the prices of rent for the movie

'''
def get_rent_table(prices):
    rent_price = prices.loc[prices['monetization_type'] == 'rent']
    return rent_price


'''
# This function will filter out the buy offers of the movie.
# Support method to form a colorful table if necessary.

# Parameters
# ----------
# prices : dataframe of the prices of the movie

# Returns
# -------
# dataframe of the prices of buying the movie

'''
def get_buy_table(prices):
    buy_price = prices.loc[prices['monetization_type'] == 'buy']
    return buy_price



'''
# This function will filter out the subscribe offers of the movie.

# Parameters
# ----------
# prices : dataframe of the prices of the movie

# Returns
# -------
# dataframe of the prices of subscribing the movie

'''
def get_subscribe_table(prices):
    flatrate_price = prices.loc[prices['monetization_type'] == 'flatrate']
    return flatrate_price
    
'''
# This function will plot the movie renting information.
# Support method to form a colorful table if necessary.
# Parameters
# ----------
# movie_df : dataframe of movies found

# Returns
# -------
# bar chart

'''    
def plot_rent_price(prices):
    rent_price = prices.loc[prices['monetization_type'] == 'rent']
    ax = sns.barplot(x = 'clear_name', y='retail_price', hue = "presentation_type", data = rent_price)
    plt.tight_layout()
    plt.savefig("rent-price.png",bbox_inches='tight')
    # ax.get_figure().tight_layout()
    # ax.get_figure().savefig("rent-price.jpg",bbox_inches='tight')
    
    
'''
# This function will plot the movie buying information.
# Support method to form a colorful table if necessary.
# Parameters
# ----------
# movie_df : dataframe of movies found

# Returns
# -------
# bar chart

'''  
def plot_buy_price(prices):
    buy_price = prices.loc[prices['monetization_type'] == 'buy']
    ax = sns.barplot(x = 'clear_name', y='retail_price', hue = "presentation_type", data = buy_price)
    plt.tight_layout()
    plt.savefig("buy-price.png",bbox_inches='tight')
    # ax.tight_layout()
    # ax.savefig("buy-price.jpg",bbox_inches='tight')

'''
# This function will plot the sorted bar chart of the rating of the movies

# Parameters
# ----------
# movie_df : dataframe of movies found

# Returns
# -------
# bar chart

'''
def plot_rating_graph(movie_df):
    ax = sns.barplot(x = 'No.', y='Rating', data = movie_df, order=movie_df.sort_values('Rating')['No.'])
    plt.savefig("rating-comparison.jpg")

'''
# This function will combine the details of movie in movies.csv and movie found through JustWatch API.

# Parameters
# ----------
# name : string name of the movie

# Returns
# -------
# a dataframe of the complete details of the movie

'''
def get_movie_list(name):
    data = get_jw_movies(name)
    movie_list = []
    count = 1
    for i in range(len(data)):
        movie_name = data.iloc[i]['title']
        movie_year = int(data.iloc[i]['original_release_year'])
        movie_offer = data.iloc[i]['offers']
        imdb_result = loadMovies(movie_name, movie_year)
        row_value = []
        if (imdb_result != None):
            row_value.append(count)
            row_value.append(movie_name)
            row_value.append(movie_year)
            row_value.append(movie_offer)
            row_value.append(imdb_result[0].values[0])
            row_value.append(imdb_result[1].values[0])
            row_value.append(imdb_result[2].values[0])
            row_value.append(imdb_result[3].values[0])
            row_value.append(imdb_result[4].values[0])
            movie_list.append(row_value)
            count = count + 1
    if len(movie_list)>0:
        movie_df = pd.DataFrame(movie_list,
                                columns=['No.', 'Title', 'Year', 'offers', 'Rating', 'Director', 'Actors', 'Genre',
                                         'Description'])
        print(movie_df['Description'].to_string())
        return movie_df
    else:
        return None

'''
# This is the main function of this file that connect the functions into an interactive program.

# Returns
# -------
# None.

'''
def main():
    
####################################################################################################
######################################### FIRST STAGE ##############################################
####################################################################################################

    name = input("Search by name: (Enter Done to exit.) ").lower().strip()
    
    while (name != "done"):
        data = get_jw_movies(name)
        movie_list = []
        count = 1
        for i in range(len(data)):
            movie_name = data.iloc[i]['title']
            movie_year = int(data.iloc[i]['original_release_year'])
            movie_offer = data.iloc[i]['offers']
            imdb_result = loadMovies(movie_name, movie_year)
            row_value = []
            if (imdb_result != None):
                row_value.append(count)
                row_value.append(movie_name)
                row_value.append(movie_year)    
                row_value.append(movie_offer)
                row_value.append(imdb_result[0].values[0])  
                row_value.append(imdb_result[1].values[0])
                row_value.append(imdb_result[2].values[0])  
                row_value.append(imdb_result[3].values[0])
                row_value.append(imdb_result[4].values[0])
                movie_list.append(row_value)
                count = count + 1

        
        # First stage result:        
        if (len(movie_list) == 0):
            print("Cannot find movie %s"%movie_name)
            print()
            name = input("Search by name: (Enter Done to exit.) ").lower().strip()
            continue
        
        else:
            movie_df = pd.DataFrame(movie_list, columns=['No.', 'Title', 'Year', 'offers', 'Rating', 'Director', 'Actors', 'Genre', 'Description'])
            print(movie_df[['No.', 'Title', 'Year', 'Rating','Genre']])
            plot_rating_graph(movie_df)
            

####################################################################################################
######################################## SECOND STAGE ##############################################
####################################################################################################
           
        row = input("Which one are you interested (No.): (Enter Back to return to search) ")
        if (row.lower() == "back"):
            print()
            name = input("Search by name: (Enter Done to exit.) ").lower().strip()
            continue
               
        try:
            row = int(row)
            movie_display = movie_df.iloc[row - 1]
            prices = get_jw_price(movie_display['offers'])
        
        except ValueError:
            print("Please use the Movie No.")
        
        
        # Second stage result:
        print ('Movie: %s - %s'%(movie_display['Title'], movie_display['Year']))
        print ('Rating: %s'%movie_display['Rating'])
        print ("Genre: %s"%movie_display['Genre'])
        print ('Director: %s'%movie_display['Director'])
        print ('Actors: %s'%movie_display['Actors'])
        print ('Description: %s'%movie_display['Description'])
        # WordCloud
        show_cloud_word(movie_display['Title'])
        
        # rent, buy and subscribe table
        rent_table = get_rent_table(prices)
        buy_table = get_buy_table(prices)
        subscribe_table = get_subscribe_table(prices)
        print(rent_table[['clear_name', 'currency', 'retail_price']].rename(columns={"clear_name": "Company", "currency": "Currency", "retail_price": "Price"}))
        print(buy_table[['clear_name', 'currency', 'retail_price']].rename(columns={"clear_name": "Company", "currency": "Currency", "retail_price": "Price"}))
        print(subscribe_table[['clear_name']].rename(columns={"clear_name": "Company"}))
        
        # plot rent and buy graph
        plot_rent_price(prices)
        plot_buy_price(prices)
        
            
        print ("You can choose to: ") 
        for i in prices['monetization_type'].drop_duplicates():
            if (i == "flatrate"):
                print('subscribe')
            else:
                print (i)

####################################################################################################
######################################## THIRD STAGE ###############################################
####################################################################################################
            
        choice = input("I want to (rent/ buy/ subscribe): ").lower()
        
        print ('%s Movie: %s - %s'%(choice, movie_display['Title'], movie_display['Year']))
        if (choice == 'rent'):
            print(rent_table[['clear_name', 'presentation_type', 'currency', 'retail_price', 'urls']].rename(columns={"clear_name": "Company", "presentation_type": "Quality", "currency": "Currency", "retail_price": "Price", "urls": "URL"}))
            
            
        if (choice == 'buy'):
            print(buy_table[['clear_name', 'presentation_type', 'currency', 'retail_price', 'urls']].rename(columns={"clear_name": "Company", "presentation_type": "Quality", "currency": "Currency", "retail_price": "Price", "urls": "URL"}))
            
        
        if (choice == 'subscribe'):
            print(subscribe_table[['clear_name']].rename(columns={"clear_name": "Company"}))
            
        name = input("Search by name: (enter DONE to exist)").lower()

if __name__ == '__main__':
    main()




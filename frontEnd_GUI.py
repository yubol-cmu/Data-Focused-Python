"""
95-888 Data Focused Python Final Project

@author: Pandas-Ningduo Zhao
"""
import tkinter as tk
import Oscar,new_hot,search
import numpy as np
from PIL import ImageTk, Image
#import tweeter
import pandas as pd
from pandastable import Table
from tkinter.font import Font

# create main window
window = tk.Tk()
window.title('Movie Master')
window.geometry('1000x1100')

# create searchbar label and searchbar text input field
searchLabel=tk.Label(window,text="Please use the search bar below to get UP-TO-DATE viewing options for your movie of choice")
searchLabel.place(x=220,y=0)
searchbar=tk.Entry(window,show=None)
searchbar.place(x=400,y=30)

'''
# generating the viewing options window for the movie that the user chose
'''
def get_viewing_options():
    global ViewingOptionsWindow
    ViewingOptionsWindow = create_window(searchResWindow, 1300, 800)
    userChoice = int(choicebar.get())
    global movie_display
    movie_display=movie_list_results.iloc[userChoice - 1]
    prices = search.get_jw_price(movie_display['offers'])

    # placing movie title, year, rating,genre,director,actors,description info on the upper left corner
    global titleYear
    titleYear=tk.StringVar()
    titleYear.set(str(movie_display['Title']) + " - " + str(movie_display['Year']))
    print(titleYear)
    titleYearLabel = tk.Label(ViewingOptionsWindow,textvariable=titleYear)
    titleYearLabel.place(x=50, y=50)
    global rating
    rating=tk.StringVar()
    rating.set("Rating: "+str(movie_display['Rating']))
    ratingLabel = tk.Label(ViewingOptionsWindow, textvariable=rating)
    ratingLabel.place(x=50, y=70)
    global genre
    genre=tk.StringVar()
    genre.set("Genre: "+str(movie_display['Genre']))
    genreLabel = tk.Label(ViewingOptionsWindow, textvariable=genre)
    genreLabel.place(x=50, y=90)
    global director
    director=tk.StringVar()
    director.set("Director: "+str(movie_display['Director']))
    directorLabel = tk.Label(ViewingOptionsWindow, textvariable=director )
    directorLabel.place(x=50, y=110)
    myFont = Font(family="Arial", size=12)
    global actors
    actors="Actors: "+str(movie_display['Actors'])
    actorsLabel = tk.Text(ViewingOptionsWindow, width=45,height=100)
    actorsLabel.place(x=50, y=130)
    actorsLabel.insert(tk.END,actors)
    actorsLabel.configure(font=myFont)
    global description
    description="Description: " + str(movie_display['Description'])
    descriptionLabel = tk.Text(ViewingOptionsWindow, width=45,height=100)
    descriptionLabel.place(x=50, y=200)
    descriptionLabel.insert(tk.END,description)
    descriptionLabel.configure(font=myFont)


    #placing word Cloud at the upper right corner
    search.show_cloud_word(str(movie_display['Title']))
    global wordCloudImg
    wordCloudImg = ImageTk.PhotoImage(Image.open("word-cloud.jpg"))
    global wordCloudCanvas
    wordCloudCanvas = tk.Canvas(ViewingOptionsWindow, width=600, height=500)
    wordCloudCanvas.place(x=680,y=0)
    wordCloudCanvas.create_image(0, 0, anchor='nw', image=wordCloudImg)

    #placing the rentting options table at the lower left corner
    rent_table = search.get_rent_table(prices)
    buy_table = search.get_buy_table(prices)
    subscribe_table = search.get_subscribe_table(prices)
    search.plot_rent_price(prices)
    search.plot_buy_price(prices)

    rentTableFrame = tk.Frame(ViewingOptionsWindow, height=300, width=500)
    rentTableFrame.place(x=50, y=500)
    rentTable = Table(rentTableFrame)
    rentTable.model.df = rent_table
    rentTable.height = 200
    rentTable.width = 500
    rentTable.show()

    # placing the buying options table at the lower right corner
    buyTableFrame = tk.Frame(ViewingOptionsWindow, height=300, width=500)
    buyTableFrame.place(x=680, y=500)
    buyTable = Table(buyTableFrame)
    buyTable.model.df = buy_table
    buyTable.height = 200
    buyTable.width = 500
    buyTable.show()

    rentingOptionLabel = tk.Label(ViewingOptionsWindow, text="Here is all the renting options:")
    rentingOptionLabel.place(x=50, y=480)

    buyingOptionLabel = tk.Label(ViewingOptionsWindow, text="Here is all the buying options:")
    buyingOptionLabel.place(x=680, y=480)

'''
# generating the movie search result window and let user to choose which on he/she wants to get the viewing options
'''
def search_movie():
    searchInput=searchbar.get()
    pd.options.display.max_colwidth=100

    # generating the movie search result table
    global movie_list_results
    movie_list_results=search.get_movie_list(searchInput)
    results_for_display=movie_list_results.drop('offers',axis=1).drop('Actors',axis=1).drop('Description',axis=1)
    global searchResWindow
    searchResWindow = create_window(window, 1000, 1000)
    movielistLabel = tk.Label(searchResWindow, text="Here is a list of movies that contains your search keyword:")
    movielistLabel.place(x=50, y=30)
    resultListFrame = tk.Frame(searchResWindow, height=600, width=800)
    resultListFrame.place(x=50, y=50)
    resultListTable = Table(resultListFrame)
    resultListTable.model.df = results_for_display
    resultListTable.height = 300
    resultListTable.width = 800
    resultListTable.show()

    # generate the choice field to let user select movie from the search result list
    movieChoiceLabel = tk.Label(searchResWindow,text="Which one are you interested in? (No.)")
    movieChoiceLabel.place(x=270, y=430)
    global choicebar
    choicebar = tk.Entry(searchResWindow, show=None,width=2)
    choicebar.place(x=510, y=430)
    knowMoreButton = tk.Button(searchResWindow, text='Get Viewing Options', width=15, height=1, command=get_viewing_options)
    knowMoreButton.place(x=550, y=430)

    # generate the movie rating plot of the search result list
    ratingGraphLabel = tk.Label(searchResWindow, text="Checkout the ratings of the movies listed above:")
    ratingGraphLabel.place(x=50, y=460)
    search.plot_rating_graph(movie_list_results)
    global Ratingimg
    Ratingimg = ImageTk.PhotoImage(Image.open("rating-comparison.jpg"))
    # global RatingCanvas
    RatingCanvas = tk.Canvas(searchResWindow, width=900, height=600)
    RatingCanvas.place(x=200, y=480)
    RatingCanvas.forget()
    RatingCanvas.create_image(0, 0, anchor='nw', image=Ratingimg)

# generate the search button on the main page
searchButton=tk.Button(window,text='Search', width=7,height=1,command=search_movie)
searchButton.place(x=600,y=30)

# display hot movie table on the main page
hotMovieLabel=tk.Label(window,text="Today's Top Hit Movie on Rotten Tomatoes:")
hotMovieLabel.place(x=50,y=70)
# call find_Hot Movie() method to get the updated hot movies information
hotMovies = new_hot.find_Hot_Movie()

hotMovieFrame=tk.Frame(window,height = 350, width = 800)
hotMovieFrame.place(x=220,y=100)
hotMovieTable=Table(hotMovieFrame)
hotMovieTable.model.df=hotMovies
hotMovieTable.height=300
hotMovieTable.show()

# display new movie table on the main page
newMovieLabel=tk.Label(window,text="Brand New Movies that Just Came Out on Rotten Tomatoes:")
newMovieLabel.place(x=50,y=460)
# call find_New Movie() method to get the updated new movies information
newMovies = new_hot.find_New_Movie()
newMovieFrame=tk.Frame(window,height = 350, width = 800)
newMovieFrame.place(x=220,y=490)
newMovieTable=Table(newMovieFrame)
newMovieTable.model.df=newMovies
newMovieTable.height=300
newMovieTable.show()

# display oscar section text labels
OscarLabel1=tk.Label(window,text="Didn't find anything you like up there?")
OscarLabel1.place(x=370,y=850)
OscarLabel2=tk.Label(window,text="Don't Worry! Checkout out our Oscar Section below to pick up some all-time classics.")
OscarLabel2.place(x=250,y=870)

'''
# generate top oscar winning ranking plot and top oscar nomination ranking plot
'''
def show_top_oscar_movie():
    oscar = pd.read_csv('the_oscar_award.csv')
    oscar = Oscar.data_cleansing(oscar)
    Oscar.top_awarding_nominated(oscar)
    global awardWinningImg
    awardWinningImg = ImageTk.PhotoImage(Image.open("top-10-award-winning-movies.jpg"))
    global topOscarWindow
    topOscarWindow = tk.Toplevel()
    topOscarWindow.title('Movie Master')
    topOscarWindow.geometry('1100x1000')
    # global awardWinningCanvas
    awardWinningCanvas = tk.Canvas(topOscarWindow, width=900, height=400)
    awardWinningCanvas.place(x=50, y=50)
    awardWinningCanvas.forget()
    awardWinningCanvas.create_image(0, 0, anchor='nw', image=awardWinningImg )
    global nominationImage
    nominationImage = ImageTk.PhotoImage(Image.open("top-10-nominated-movies.jpg"))
    # global nominatedCanvas
    nominatedCanvas = tk.Canvas(topOscarWindow, width=900, height=400)
    nominatedCanvas.place(x=100, y=500)
    nominatedCanvas.forget()
    nominatedCanvas.create_image(0, 0, anchor='nw', image=nominationImage)

'''
# show oscar awarding winning movies of a certain year
'''
def show_annual_winner_list():
    oscar = pd.read_csv('the_oscar_award.csv')
    oscar = Oscar.data_cleansing(oscar)
    year = int(annualOscarbar.get())
    certain_year_df = Oscar.winner_list_by_year(oscar, year)
    annualOscarWindow = tk.Toplevel()
    annualOscarWindow.title('Movie Master')
    annualOscarWindow.geometry('1200x1000')
    annualAwardFrame = tk.Frame(annualOscarWindow, height=600, width=800)
    annualAwardFrame.place(x=50, y=50)
    annualAwardTable = Table(annualAwardFrame)
    annualAwardTable.model.df = certain_year_df
    annualAwardTable.height = 600
    annualAwardTable.width = 900
    annualAwardTable.show()
    winnerListLabel = tk.Label(annualOscarWindow, text="Here is the Oscar winner list for the year you searched:")
    winnerListLabel.place(x=50, y=30)

# display the buttons for the Oscar section and their labels
topOscarButton=tk.Button(window,text='Show Top Nominated & Winning Movies', width=30,height=1,command=show_top_oscar_movie)
topOscarButton.place(x=180,y=890)

annualOscarLabel=tk.Label(window,text="Choose a year(1928-2020):")
annualOscarLabel.place(x=550,y=890)

annualOscarbar=tk.Entry(window,width=5,show=None)
annualOscarbar.place(x=730,y=890)

annualOscarButton=tk.Button(window,text='Show the winner list of the year', width=30,height=1,command=show_annual_winner_list)
annualOscarButton.place(x=550,y=920)

'''
# helper funtion to create new window
'''
def create_window(window,width,height):
    window2 = tk.Toplevel(window)
    window2.title('Movie Master')
    window2.geometry(str(width)+'x'+str(height))
    return window2



window.mainloop()
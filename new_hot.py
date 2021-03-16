#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
95-888 Data Focused Python Final Project

@author: Pandas-Yanwen Peng
"""
import requests 
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt



def find_New_Movie():
    
    # get data from Rotten Tomatto 
    # new movie = CERTIFIED FRESH MOVIES in theater   
    page = requests.get('https://www.rottentomatoes.com/browse/cf-in-theaters/')
    soup = BeautifulSoup(page.content, 'html.parser')
    
    page_main_content = soup.find(id="main_container")
    
    s = page_main_content.get_text()


    # Find first instance of "title", then move to the : after it

    i = s.find("title")

    i = s.find(":", i)
    
    all=list()
    for count in range(10):

        # find url; print from just beyond i to just before j
        tmp=list()
        j = s.find(",", i )
        tmp.append(s[i+2:j-1])
        

        # find "tomatoScore", then move to the : after it

        k = s.find("tomatoScore", j)

        k = s.find(":", k)

        # find "theaterReleaseDate"

        l = s.find("theaterReleaseDate", k)

        # print the tomatoScore
        tmp.append(s[k+1:l-2])
        
        #find then end point for tomatoScore
        l = s.find(":", l)
        #find then start point for theaterReleaseDate
        d = s.find(',', l)  
        tmp.append(s[l+2:d-1])  

        # Move i to the next instance of "title"
        i = s.find("title", l)
        i = s.find(":", i)

        all.append(tmp)
    df=pd.DataFrame(all,columns=['Title','Score','Date'])
    return df

def find_Hot_Movie():
    
    # get data from Rotten Tomatto 
        # hot movie = top box office    
    page = requests.get('https://www.rottentomatoes.com/browse/in-theaters')
    soup = BeautifulSoup(page.content, 'html.parser')
    
    page_main_content = soup.find(id="main_container")
    
    s = page_main_content.get_text()

    #print(s)

    # Find first instance of "title", then move to the : after it

    i = s.find("title")

    i = s.find(":", i)
    
    all=list()
    for count in range(10):

        # find url; print from just beyond i to just before j
        tmp=list()
        j = s.find(",", i )
        tmp.append(s[i+2:j-1])
        

        # find "tomatoScore", then move to the : after it

        k = s.find("tomatoScore", j)

        k = s.find(":", k)

        # find "theaterReleaseDate"

        l = s.find("theaterReleaseDate", k)

        # print the tomatoScore
        tmp.append(s[k+1:l-2])
        
        #find then end point for tomatoScore
        l = s.find(":", l)
        #find then start point for theaterReleaseDate
        d = s.find(',', l)  
        tmp.append(s[l+2:d-1])  

        # Move i to the next instance of "title"
        i = s.find("title", l)
        i = s.find(":", i)

        all.append(tmp)
    df=pd.DataFrame(all,columns=['Title','Score','Date'])
    return df

           

def main():
    # findNewMovie
    print('New Movie (CERTIFIED FRESH MOVIES in theater)')
    newMovies = find_New_Movie()

    
    # findHotMovie 
    print('\n\n\nHot Movie (top box office)')
    hotMovies = find_Hot_Movie()


    
if __name__ == '__main__':
    main()
    



    

# -*- coding: utf-8 -*-
"""
95-888 Data Focused Python Final Project

@author: Pandas-Yubo Li
"""
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


'''
# data_cleansing method to conduct data cleansing of a load data file.
# Formatting all string data in title case.
# return the cleaned data in pandas.dataframe
'''
def data_cleansing(oscar):
    #Data cleaning
    
    oscar['category']=oscar['category'].apply(lambda x:x.strip())
    oscar['name']=oscar['name'].apply(lambda x:x.strip().replace("(","").replace(")",""))
    oscar['film']=oscar['film'].apply(lambda x: np.NaN if str(x)=='nan' else str(x).strip())
    oscar['category']=oscar['category'].apply(lambda x:x.capitalize())
    
    category=oscar['category'].str.split('(',n=1,expand=True)
    category.columns=['category1','category2']
    category['category2']=category['category2'].apply(lambda x:str(x).capitalize().replace(")",""))
    oscar=pd.concat([oscar,category],axis=1)
    #print(oscar['name'])
    
    nameRole=oscar['name'].str.split(',',expand=True)
    nameRole=nameRole.rename(columns={0:'one_of_the_names'})
    nameRole['one_of_the_names']=nameRole['one_of_the_names'].apply(lambda x: x if x.find(":")< 0 else x[x.index(':')+1:] )
    oscar=pd.concat([oscar,nameRole['one_of_the_names']],axis=1)
    return oscar

'''
# Get the information of the top Oscar movies then form/save charts by using data manipulated
# Charts formed are supposed to be used in the Oscar feature-Top awarding/nominated part.
'''
def top_awarding_nominated(oscar):
    #Film information
    All_movie=oscar[['film','winner']].groupby(by='film').sum().sort_values(by='winner',ascending=False)
    All_movie['Awards']=All_movie['winner'].apply(lambda x:int(x))
    del All_movie['winner']
    All_movie['Nominations']=oscar[['film','winner']].groupby(by='film').count()
    All_movie['Winnin_rate']=All_movie['Awards']/All_movie['Nominations']
    print(All_movie.head(10))
    # Top 10 Nominated Movies
    nominated_movie=All_movie.sort_values(by='Nominations',ascending=False).head(10)
    nominated_movie['Diff']=nominated_movie['Nominations']-nominated_movie['Awards']
    nominated_movie=nominated_movie.sort_values(by='Nominations')
    vis1=plt.barh(nominated_movie.index.tolist(), nominated_movie['Awards'], 0.5,color = 'pink', label = 'Awards')
    vis1=plt.barh(nominated_movie.index.tolist(), nominated_movie['Diff'],0.5, color = 'c', left = nominated_movie['Awards'], label = 'Only nominated')
    
    plt.xlabel('Number Of Record')
    plt.ylabel('Movie')   
    plt.xticks(range(0,max(nominated_movie['Nominations']),2))
    plt.legend(loc='lower right',fontsize=8)
    plt.title('Top 10 Nominated Movies')
    # chart saving
    plt.savefig('top-10-nominated-movies.jpg',bbox_inches='tight')

    #Top 10 Award-winning Movies
    Award_winning_movie=All_movie.sort_values(by='Awards',ascending=False).head(10)
    Award_winning_movie=Award_winning_movie.sort_values(by='Awards')
    movie_name=Award_winning_movie.index.tolist()
    
    count_award=Award_winning_movie['Awards'].to_list()
    
    
    vis2= plt.barh(movie_name,count_award,height=0.5, color = 'pink')
    plt.xlabel('Number Of Record')
    plt.ylabel('Movie')
    plt.title('Top 10 Award-winning Movies')
    plt.xticks(range(0,max(Award_winning_movie['Awards'])+2,2))
    # chart saving
    plt.savefig('top-10-award-winning-movies.jpg',bbox_inches='tight')

'''
# Locate the Oscar winners list of a specific year user entered.
# Return the list in a pandas.dataframe 
'''
def winner_list_by_year(df,year):
    df= df[df['winner'] == True]
    df=df[df['year_ceremony']==year]
    df=df[['year_ceremony','ceremony','category','name','film']].copy()
    return df
    
'''
# Helper method which is not used in the main file. This is used to form a table of the winner list.
# The purpose of this method is to double check the result is correct 
# and in case user want to see a colorful table instead of a plain one.
'''  
def get_table(df):

    pattern = ["#FFFFB5","ivory","#FFD8BE"]*10
    columnSize = len(df.columns)
    rowSize =len(df)
    fig, ax = plt.subplots(dpi=800)
    color=[pattern[:columnSize]]*rowSize

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    table=plt.table(cellText=df.values, colLabels=df.columns, loc='center',cellColours=color,colColours=["#9DABDD"]*columnSize)
    fig.tight_layout()
    plt.show()   
    
def main():
    oscar = pd.read_csv('the_oscar_award.csv')
    oscar = data_cleansing(oscar)
    userinput = int(input('How Can I Help You? \n1. Show Top Nominated & Winning Movies\n2. Show the winner list of a year(1928-2020) \n3. Quit'))
    while(userinput!=3):
        if userinput == 1:
            top_awarding_nominated(oscar)
        elif userinput == 2:
            year = int(input("Enter the year (1928-2020):"))
            certain_year=winner_list_by_year(oscar,year)
            get_table(certain_year)
        else:
            print("Your input is invalid. Please try it again.")
        userinput = int(input('How Can I Help You? \n1. Show Top Nominated & Winning Movies\n2. Show the winner list of a year(1928-2020) \n3. Quit'))

if __name__ == '__main__':
    main() 
    
    
    
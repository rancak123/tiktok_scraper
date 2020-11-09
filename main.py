# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 11:25:22 2020

@author: Piyush
"""


import traceback
from TikTokApi.browser import set_async
from TikTokApi import TikTokApi
import pandas as pd
import time

#Remove this
import webbrowser


import os


columns = ['authorUsername',
 'authorId',
 'authorNickName',
 'followingCount',
 'followerCount',
 'heartCount',
 'videoCount',
 'averageHeart', 
 'diggCount',
 'heart', 
 'email']




def get_user_details(username, api):
    '''
    Create an API object by: api = TikTokApi() and pass it in the function
    '''
    D = {'authorNickName' : None, 'heart' : None, 'diggCount' : None, 
     'email' : None, 'followerCount' : None, 'folllowingCount' : None, 
     'heartCount' : None, 'videoCount' : None}
        
    results = api.getUser(username)
    D['authorNickName'] = results['user']['nickname']
    D['heart'] = results['stats']['heart']
    D['diggCount'] = results['stats']['diggCount']
    D['email'] = email_extractor(results['user']['signature'])
    D['followerCount'] = results['stats']['followerCount']
    D['followingCount'] = results['stats']['followingCount']
    D['heartCount'] = results['stats']['heartCount']
    D['videoCount'] = results['stats']['videoCount']
    
    return D



def get_description_and_bio(username, api):
    result = api.getUser(username)
    desc=  result['user']['signature']
    try:
        bio = result['user']['bioLink']['link']
    
    except KeyError:
        bio = None
        
    return {'bioLink' : bio, 'description' : desc}



def get_average_hearts(hearts, videos):
    if type(hearts) == str and type(videos) == str and hearts.isdigit() and videos.isdigit():
        return int(hearts) / int(videos)
    else:
        try:
            return hearts / videos
        
        except:
            return 

def email_extractor(text):
    import re
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
    if emails:
        return ', '.join(emails)
    
    else:
        return


def get_user_link(username):
    placeholder_url = 'https://www.tiktok.com/@%s?lang=en'
    webbrowser.open_new_tab(placeholder_url % username)

    return placeholder_url % username


def get_follower_details(num_trending, start_follower_count, end_follower_count = None):
    set_async()    
    api = TikTokApi()
    
    trending = api.trending(count = num_trending)
    
    return_list = list()
    for tiktok in trending:
#        print('followers are: ', tiktok['authorStats']['followerCount'])
        D = {'authorUsername' : None, 
             'authorId' : None, 
             'authorNickName' : None, 
             'followingCount' : None,
             'followerCount' : None,
             'heartCount' : None,
             'videoCount' : None,
             'averageHeart': None,
             'diggCount' : None, 
             'heart' : None, 
             'email' : None
             
             }
        
        followers = tiktok['authorStats']['followerCount']
        if followers >= start_follower_count and followers < end_follower_count + 1:
            description = tiktok['author']['signature']
            if email_extractor(description):
                D['email'] =email_extractor(description)
            D['authorId'] = tiktok['author']['id']           
            D['authorUniqueId'] = tiktok['author']['uniqueId']
            D['authorNickName'] = tiktok['author']['nickname']
            D['followingCount'] = tiktok['authorStats']['followingCount']
            D['followerCount'] = tiktok['authorStats']['followerCount']
            D['heartCount'] = tiktok['authorStats']['heartCount']
            D['diggCount'] = tiktok['authorStats']['diggCount']
            D['heart'] = tiktok['authorStats']['heart']
            D['videoCount'] = tiktok['authorStats']['videoCount']
            D['averageHeart'] = get_average_hearts(tiktok['authorStats']['heart'], 
             tiktok['authorStats']['videoCount'])
            
            #Making sure the tiktok user occurs only one and if again then skip it
            repeat = False
            for item in return_list:
                if item['authorId'] == tiktok['author']['id']:
                    ### REpeat shoudl be true
                    repeat = False
            if not repeat:
                return_list.append(D)
    return return_list
        



def get_details_from_discover(num, start_follower_count, end_follower_count = None, user_id = None):
    set_async()    
    api = TikTokApi()
    if user_id == None:
        user_id = best_1['id']
    details = api.getSuggestedUsersbyIDCrawler(count = num, startingId = user_id)
    
    return_list = list()
    for tiktok in details:
#        print('followers are: ', tiktok['authorStats']['followerCount'])
        D = {'authorId' : None, 
             'authorUsername' : None, 
             'authorNickName' : None, 
             'followingCount' : None,
             'followerCount' : None,
             'heartCount' : None,
             'videoCount' : None,
             'averageHeart': None,
             'diggCount' : None, 
             'heart' : None, 
             'email' : None
             
             }
        
        followers = tiktok['extraInfo']['fans']
        if followers >= start_follower_count and followers < end_follower_count + 1:
            description = tiktok['description']
            if email_extractor(description):
                D['email'] =email_extractor(description)
            D['authorId'] = tiktok['id']
            D['authorUsername'] = tiktok['link'].strip('/@')
#            D['authorNickName'] = tiktok['author']['nickname']
#            D['followingCount'] = tiktok['authorStats']['followingCount']
#            D['followerCount'] = tiktok['authorStats']['followerCount']
#            D['heartCount'] = tiktok['authorStats']['heartCount']
#            D['diggCount'] = tiktok['authorStats']['diggCount']
#            D['heart'] = tiktok['authorStats']['heart']
#            D['videoCount'] = tiktok['authorStats']['videoCount']
#            D['averageHeart'] = get_average_hearts(tiktok['authorStats']['heart'], 
#             tiktok['authorStats']['videoCount'])
            
            #Making sure the tiktok user occurs only one and if again then skip it
            repeat = False
            for item in return_list:
                if item['authorId'] == tiktok['id']:
                    ### REpeat shoudl be true
                    repeat = False
            if not repeat:
                return_list.append(D)
    return return_list
        
    
class CsvOperations:
    
    def __init__(self, file_name = None):
        if file_name == None:
            self.file_name ='tiktokusers.csv'
        self.username_column = 'authorUsername'
        if not self.check_file():
            self.create_file()
        
        pass
    
    def is_empty_csv(self):
        try:
            pd.read_csv(self.file_name)
            return False
        
        except:
            return True
        
        else:
            return False
        
    
    def check_file(self):
        files = os.listdir()
        if self.file_name in files:
            return True
        return False
        
    def create_file(self):
        df = pd.DataFrame(columns = columns)
        df.to_csv(self.file_name, index = False)
        
        
    def create_columns(self):
        try:
            df = pd.read_csv(self.file_name)
            print("Something is already in the dataframe!")
            
        except:
            df = pd.DataFrame(columns = columns)
            df.to_csv(self.file_name, index = False)
        
                
    
    def get_usernames(self):
        df = pd.read_csv(self.file_name)
        return df[self.username_column].tolist()
        
              
    def add_usersinfo_to_csv(self, List):
        if not self.is_empty_csv():
            users_in_csv = self.get_usernames()
            delete_indexes = list()
            for i in range(len(List)):
                username = List[i]['authorUsername']
                if username in users_in_csv:
                    delete_indexes.append(i)
            for index in delete_indexes:
                del(List[index])
        
        df2 = pd.DataFrame(List)
        try:
            df1 = pd.read_csv(self.file_name)
            
        except:
            self.create_columns()
            df1 = pd.read_csv(self.file_name)


        frames = [df1, df2]
        final_df = pd.concat(frames)
        final_df.to_csv(self.file_name, index = False)
        
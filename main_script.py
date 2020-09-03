#this script will collect comments and posts and analyze them
#will then update to respective db file

import reddit_crawler as rc 
import sql_cmds as sc
import text_parser as tp 

import sqlite3
import os.path
import time



#creates the uniqueMentions.db and perHour.db file
#DO NOT CREATE THEM MANUALLY 
def isCreated():
    if not sc.checkUM():
        sc.createUniqueMentionsdb()
        print('created uniqueMentions.db')
    if not sc.checkTS():
        sc.createTickerTimeSeriesDB()
        print('created time series db')


#list of subreddits to crawl
def createRecentHolder(): 
    list_of_subs = ['wallstreetbets', 
                    'pennystocks',
                    'investing',
                    'cryptocurrency',
                    'securityanalysis',
                    'robinhood', 
                    'investmentclub',
                    'stockmarket',
                    'stock_picks',
                    'forex',
                    'options',
                    'stocks',       
    ]
    #dictionary to hold most recent info for those subreddits
    recentInfo = {}
    for subredd in list_of_subs:
        recentInfo[subredd] = [0,'','']#(timestamp,author,postID)
    return recentInfo


#main function
def main():

    #checks to see if db is created, if not will create
    isCreated()

    #contains list of subreddits and also holds most recent (timestamp,author,postID)
    recentInfo = createRecentHolder()

    uniqueMentionsDic = {}
    nested_perHourDic = {'totalComments':{},'totalPosts':{},'uniqueComments':{},'uniquePosts':{}}
    count = 0
    while True:
        #collect comments from a sub every minute, posts every 30 minutes, updates database every hour
        if count == 9000:
            count = 0
        list_of_comments = []
        start_time = time.time()
        for sub in recentInfo.keys():
            recentInfo[sub][1],recentInfo[sub][0] = rc.get_comments_from_sub(sub,list_of_comments,recentInfo[sub][1],recentInfo[sub][0])
        for commentInfo in list_of_comments:
            author = commentInfo[0]
            ticker_list = tp.ticker_parse3(commentInfo[2])
            for ticker in ticker_list:
                if ticker not in uniqueMentionsDic.keys():
                    uniqueMentionsDic[ticker] = [author]
                else:
                    if author not in uniqueMentionsDic[ticker]:
                        uniqueMentionsDic[ticker].append(author)
                if ticker not in nested_perHourDic['totalComments'].keys():
                    nested_perHourDic['totalComments'][ticker] = 1
                else:
                    nested_perHourDic['totalComments'][ticker] += 1
                if author not in sc.getUniqueUsers(ticker):
                    if ticker not in nested_perHourDic['uniqueComments'].keys():
                        nested_perHourDic['uniqueComments'][ticker] = 1
                    else:
                        nested_perHourDic['uniqueComments'][ticker] += 1
        count += 1

        #every five minutes will also collect posts 
        
        if count % 5 == 0:
            list_of_posts = []
            for sub in recentInfo.keys():
                recentInfo[sub][2] = rc.get_posts_from_sub(sub,list_of_posts,recentInfo[sub][2])
            for postInfo in list_of_posts:
                author = postInfo[0]
                ticker_list = tp.ticker_parse3(postInfo[2])
                for ticker in ticker_list:
                    if ticker not in uniqueMentionsDic.keys():
                        uniqueMentionsDic[ticker] = [author]
                    else:
                        if author not in uniqueMentionsDic[ticker]:
                            uniqueMentionsDic[ticker].append(author)
                    if ticker not in nested_perHourDic['totalPosts'].keys():
                        nested_perHourDic['totalPosts'][ticker] = 1
                    else:
                        nested_perHourDic['totalPosts'][ticker] += 1
                    if author not in sc.getUniqueUsers(ticker):
                        if ticker not in nested_perHourDic['uniquePosts'].keys():
                            nested_perHourDic['uniquePosts'][ticker] = 1
                        else:
                            nested_perHourDic['uniquePosts'][ticker] += 1
        #every 10 minutes will update sql db and reset dictionaries
        if count % 10 == 0:
            print('uploading....')

            #removes duplicates from uniqueMentionsDic
            for ticker in uniqueMentionsDic.keys():
                uniqueMentionsDic[ticker] = list(set(uniqueMentionsDic[ticker]))
            sc.updateUniqueMentionsFile(uniqueMentionsDic)
            sc.updateTS(nested_perHourDic)
            uniqueMentionsDic = {}
            nested_perHourDic = {'totalComments':{},'totalPosts':{},'uniqueComments':{},'uniquePosts':{}}
        total_time_taken_for_one_loop = time.time() - start_time
        if count % 10 ==  0:
            print('long run took ' + str(total_time_taken_for_one_loop))
        if total_time_taken_for_one_loop >= 60:
            print('loop took over 60 seconds, breaking while loop....')
            break
        time.sleep(60-total_time_taken_for_one_loop)



if __name__ == '__main__':
    main()




#collects posts and comments from a subreddit and converts into tuple and adds to a dictionary of lists 
from redditSecret import secretDic
import praw
import time 

#reddit instance
r = praw.Reddit(client_id = secretDic['client_id'],
                client_secret = secretDic['client_secret'],
                user_agent = secretDic['user_agent'],
                username = secretDic['username'],
                password = secretDic['password'])


#given a subreddit str, dictionary of lists, most recent author and timestamp of a comment
#fills dictionary values with comments tuple, posts tuple
#returns most recent comment author, comment timestamp, postID
def gather_from_sub(subredd,infodict,recentCommentAuthor,recentCommentTimestamp,recentPostID): 
    sr = r.subreddit(subredd)
    return_ca,return_ct = get_comments_from_sub(sr,infodict['comments'],recentCommentAuthor,recentCommentTimestamp)
    return_pID = get_posts_from_sub(sr,infodict['posts'],recentPostID)
    return return_ca,return_ct,return_pID


#helper methods

#var to decide how many comments to obtain with each call
TOTAL_COMMENTS_TO_GET = 120
#given subreddit obj, list, recentCommentAuthor,recentCommentTimestamp
#adds tuple containing comment info(author,timestamp,commenttext) to list(dict['comments]) until it hits most recent
#returns updated recentCommentAuthor,recentCommentTimeStamp
def get_comments_from_sub(subredd,commentList,recentCA,recentCT):
    sr = r.subreddit(subredd)
    gen_list = sr.comments(limit = TOTAL_COMMENTS_TO_GET)
    is_updated = False

    return_timestamp = 0
    return_comment_author = ''

    reached_the_end = False

    for comment in gen_list:

        if comment.author is None:
            continue

        comment_Time = comment.created_utc
        comment_Author = comment.author.name
        comment_Text = comment.body 

        if is_updated == False:
            is_updated = True
            return_timestamp = comment_Time
            return_comment_author = comment_Author

        if comment_Author == recentCA and comment_Time == recentCT:
            reached_the_end = True
            break

        else:
            list_tuple = (comment_Author,comment_Time,comment_Text)
            commentList.append(list_tuple)
    if not reached_the_end:
        print('DID NOT GET ALL COMMENTS FROM ' + subredd)
    return return_comment_author,return_timestamp


    
#var to decide how many posts to obtain with each call
TOTAL_POSTS_TO_GET = 25
#given subreddit obj, dictionary of lists, recentPostID
#combines post title and post desc into one long string and adds it to dictionary of lists['post']
#returns recentPostID
def get_posts_from_sub(subredd,postList,recentPostID):
    sr = r.subreddit(subredd)
    gen_list = sr.new(limit = TOTAL_POSTS_TO_GET)
    is_updated = False

    return_ID = ''

    reached_the_end = False

    for post in gen_list:
        
        if post.author is None:
            continue

        post_Time = post.created_utc
        post_Author = post.author.name
        post_Text = post.title +'   '+ post.selftext 
        post_ID = post.id 

        if is_updated == False:
            is_updated = True
            return_ID = post_ID
        if recentPostID == post_ID:
            reached_the_end = True
            break
        else:
            list_tuple = (post_Author,post_Time,post_Text,post_ID)
            postList.append(list_tuple)
    if not reached_the_end:
        print('DID NOT GET ALL POSTS FROM ' + subredd)
    return return_ID


#helper function
#replaces " in the str with a space
#required so that sql db can process
def replaceQuotation(strinput):
    strinput = strinput.replace('"',' ')
    return strinput.replace("'"," ")




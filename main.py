import facebook
import os

access_token = os.environ['FB_TOKEN_BAS']

 #here goes your access token from http://maxbots.ddns.net/token
graph = facebook.GraphAPI(access_token)
msg = 'Hello facebook! This is my first bot made with Python!' #message for the post
comment_msg = 'This is a bot posted comment!' #message for the comment
post_id = graph.put_photo(image = open('monkey.jpg', 'rb'), message= msg)["post_id"] #photo got posted!
print('Photo has been uploaded to facebook!')
graph.put_comment(object_id = post_id, message = comment_msg)#comment got posted!

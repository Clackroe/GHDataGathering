import os, requests, json, traceback, shutil, re

from textUtils import *

GIT_ACCESS_TOKEN = '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' #'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' #replace with your own token


def validateLockedLinks(file_path):
    
    links = []
    
    
    try: 
        os.remove(f'{file_path}/validLinks.txt')
        print("Existing File Removed!")
    except:
        print("File not found")
    
    with open(f'ConstantData/heatedLinks.txt', 'r') as f: #retrieve heated links, that we got from the previous research papers, and modify them to their api counterparts
        for line in f:
            link = line.strip()
            url = link.replace("https://github.com", "https://api.github.com/repos")
            links.append(url)
            
        
    for url in links: #for each link, check if it has 3 or more comments, if it does, log it to a file
        
        try:
            response = requests.get(url, headers={"Authorization": f"Bearer {GIT_ACCESS_TOKEN}"}).json()
            
            if 'comments' not in response:
                pass      
            
            elif response["comments"] >= 3:
                with open(f'{file_path}/validLinks.txt', 'a') as file:
                    url = url.replace("https://api.github.com/repos", "https://github.com")
                    file.write(url + '\n')                
                    print(f'Logged Valid Link: {url}!')
                    
        except Exception as e:
            print("Error with URL: " + url + '\n \n Response: ' + str(response) + '\n \n Error:' + str(e))
            

def mineAdditionalIssues(file_path, depth_of_search):
    
    links = []
    
    lockCounter = 0
    unlockCounter = 0
    
    try:
        os.remove(f'{file_path}/unlockedLinks.txt')
        print("Existing File Removed!")
    except:
        print("File not found")
        
    try:
        os.remove(f'{file_path}/additionalLockedIssues.txt')
        print("Existing File Removed!")
    except:
        print("File not found")

    with open(f'ConstantData/heatedLinks.txt', 'r') as f:  #retrieve heated links, that we got from the previous research papers, and modify them to their api counterparts
        for line in f:
            link = line.strip()
            url = link.replace("https://github.com", "https://api.github.com/repos")
            issueNum = ''
            for char in reversed(url):
                if char == '/':
                    break
                else:
                    issueNum = char + issueNum
                    
            
            for i in range(depth_of_search):  #increment and decrement every link by 1-depth of search, and log them to a file
                urlDecremented = url.replace(issueNum, str(int(issueNum) - i))
                links.append(urlDecremented)
                urlIncremented = url.replace(issueNum, str(int(issueNum) + i))
                links.append(urlIncremented)
            
        
    
    for url in links: #check if the newly retrieved links have 3 or more comments, and are either heated or nonheated, log them to their respective files
        
        try:
            response = requests.get(url, headers={"Authorization": f"Bearer {GIT_ACCESS_TOKEN}"}).json()
            
            if 'comments' not in response:
                pass      
            
            elif response["comments"] >= 3 and response["locked"] == False:
                with open(f'{file_path}/unlockedLinks.txt', 'a') as file:
                    url = url.replace("https://api.github.com/repos", "https://github.com")
                    file.write(url + '\n')  
                    unlockCounter += 1              
                    print(f'Logged Unlocked URL {url}...')
            elif response["comments"] >= 3 and response["locked"] == True and response["active_lock_reason"] == "too heated":
                with open(f'{file_path}/additionalLockedIssues.txt', 'a') as file:
                    url = url.replace("https://api.github.com/repos", "https://github.com")
                    file.write(url + '\n')     
                    lockCounter += 1           
                    print(f'Logged Locked URL {url}...')
                
                    
        except Exception as e:
            print("Error with URL: " + str(url) + '\n \n Error:' + str(e) + '\n\nTraceback: ' + traceback.print_exc()) 
    
    return lockCounter, unlockCounter #return the number of locked and unlocked issues mined for use in the terminal
                
            

def gatherPostRawData(input_path):
    
    
    validLinks = []
    with open(input_path, 'r') as f:  #retrieve list of GitHub links from the file, and modify them to their api counterparts
        for line in f:
            link = line.strip()
            url = link.replace("https://github.com", "https://api.github.com/repos")
            validLinks.append(url)
            
    
        
    for url in validLinks: #Log the post and comment raw response data retrieved from GitHub's API for future use. Sorted into unique directories for each post. (Issue_<username>_<issue number>)
               
        
        try:
            
            response = requests.get(url, headers={"Authorization": f"Bearer {GIT_ACCESS_TOKEN}"}).json()
            
            id = 'Issue_' + response['user']['login'] + '_' + str(response['number'])
            
            try:
                shutil.rmtree(f'RawData/{id}')
            except:
                print("File not found")
            
                            
            os.makedirs(f'RawData/{id}')
            print("Created Directory")            
            with open(f'RawData/{id}/Post.json', 'w+') as file:
                json.dump(response, file, indent=4, sort_keys=True)
                print(f'Successfully Gathered Post Data For: {id}')
            
            response = requests.get(response['comments_url'], headers={"Authorization": f"Bearer {GIT_ACCESS_TOKEN}"}).json()
            with open(f'RawData/{id}/Comments.json', 'w+') as file:
                json.dump(response, file, indent=4, sort_keys=True)
                print(f'Successfully Gathered Comment Data For: {id}')
            
            
            
        except Exception as e:
            print("Error with URL: " + url + '\n \n Response: ' + str(response) + '\n \n Error:' + str(e) + '\n\nTraceback: ') 
            traceback.print_exc()
            
def formatConvoKit(file_path):
    
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
        print("Removed Existing Directory!")
            
        
        
    try:
        speakers = []
            
        speakerData = {}
        
        uttData = {}
        
        conversationData = {}
        
        dir = 'TextFiles'
        
        listDir = os.listdir('RawData')
        
        for dirIndex, dir in enumerate(listDir, start=0):
            
            postJson = json.load(open(f'RawData/{dir}/Post.json'))
            commentsJson = json.load(open(f'RawData/{dir}/Comments.json'))
            
            #Generate Utterences (And Speakers.txt)
            
            os.makedirs(file_path, exist_ok=True)
            
            heated = True if postJson['active_lock_reason'] == "too heated" else False
            
            #Update the Conversation data with a unique ID for each post, and the Meta Data we deem necessary.
            conversationData.update({f"ROOT{dirIndex}": {"title": postJson['title'], "locked": postJson['locked'], "state": postJson['state'], 
                                                        "state_reason": postJson['state_reason'] ,"heated": heated, "url": postJson['html_url'], 
                                                        "author": postJson['user']['login'], "comments": postJson['comments'], "repository": postJson['repository_url'].replace("https://api.github.com/repos/", ''), }})
                
            #Update the Utterance data, then update hte role to include (AUTHOR) for the utterances.jsonl file, and the text to include the title and body of the post. 
            #Append the utterance data to the utterances.jsonl file.
            uttData = updateUtteranceData(postJson, dirIndex)
            uttData.update({'role': uttData['role'] + " (AUTHOR)"})   
            uttData.update({'text': postJson['title'] + postJson['body']})  
            with open(f"{file_path}/utterances.jsonl", 'a+', encoding="utf-8") as file:
                    file.write(json.dumps(uttData) + '\n')
                    file.close()
            #Update the Speaker data, then append the speaker data to the speakers.json file.
            updatedSpeakers = updateSpeakerData(postJson, dirIndex, speakers)
            speakerData.update(updatedSpeakers[0])
            speakers = updatedSpeakers[1]
                
            for comIndex, comment in enumerate(commentsJson, start=0):
                
                #For each comment on the post, update the conversation data with a unique ID for each comment, and the Meta Data we deem necessary.
                #Also update the utterance and speaker data, then append the utterance data to the utterances.jsonl file.
                
                commentID = f"COM{dirIndex}_{comIndex}"
                
                updatedSpeakers = updateSpeakerData(comment, dirIndex, speakers)
                speakerData.update(updatedSpeakers[0])
                speakers = updatedSpeakers[1]
                
                
                if commentID == f"COM{dirIndex}_0":
                    prevCom = f"ROOT{dirIndex}"
                else:
                    prevCom = f"COM{dirIndex}_{comIndex-1}"
                      
                uttData = updateUtteranceData(comment, dirIndex)
                uttData.update({"id": commentID})
                uttData.update({"reply_to": prevCom})
                 
                with open(f"{file_path}/utterances.jsonl", 'a+', encoding="utf-8") as file:
                    file.write(json.dumps(uttData) + '\n')
                    file.close()
            
            
        with open(f'{file_path}/speakers.json', 'a+') as file:
                                    
            file.write(json.dumps(speakerData, indent=4))
            file.close()
            
                
        with open(f"{file_path}/conversations.json", 'w+', encoding="utf-8") as file:
            file.write(json.dumps(conversationData, indent=4))
            file.close()
            
        #Write the extra data needed for the corpus to work.
        writeExtraData(file_path)
        
            
    except Exception as e:
            print("Error: " + str(e) + '\n\nTraceback: ')
            traceback.print_exc()
            

def updateUtteranceData(postJson, dirIndex):
    
    utteranceData = {}
    
    
    postTime = postJson['created_at']
    body = (postJson['body'])
    
    #split body into replies where it matchse the regex of '< words \r'
    
        
    # p = re.compile(r'[ \n]?>\s*\w.*?(?:\n\n|\n\r\n|\r\r\n|\r\n|\n\r)')
    # directQuotes = re.findall(p, body)
    
    output = remove_block_quotes(body)
    
    directQuotes = output[1]
    
    body = output[0]
    
    # remove all of the directQuotes from the body
    for quote in directQuotes:
        if is_length_short(quote):
            directQuotes.remove(quote)
        
    for i, quote in enumerate(directQuotes, start=0):
        directQuotes[i] = filter_nontext(quote)
        
    
    #remove all of the '=', '-', '+', '_', and '#' from the body IF there are 3 or more consecutive of them.
    body = re.sub(r'.*={3,}.*', '', body)
    body = re.sub(r'.*-{3,}.*', '', body)
    body = re.sub(r'.*\+{3,}.*', '', body)
    body = re.sub(r'.*_{3,}.*', '', body)
    body = re.sub(r'.*#{3,}.*', '', body)
    
    
    
    #get all of the mentions in the body
    mentions = re.findall(r'@\w*', body)
    
    body = filter_nontext(body)
    
    
    
        
    postPosReactions = str(postJson['reactions']['+1'])
    postNegReactions = str(postJson['reactions']['-1'])
    
    name = postJson['user']['login'] 

    

    utteranceData.update({"id": f"ROOT{dirIndex}"})
    
    utteranceData.update({"role": postJson['author_association']})
    
    utteranceData.update({"user":name})
    utteranceData.update({"root": f"ROOT{dirIndex}"})
    
    utteranceData.update({"reply_to": None})
    
    utteranceData.update({"timestamp": postTime})
    
    utteranceData.update({"text": body})
    utteranceData.update({"meta": {"posReactions": postPosReactions, "negReactions": postNegReactions,
                                   "overallSentiment": str(int(postPosReactions) - int(postNegReactions)), 
                                   "numWords": str(len(body.split())), "numChars": str(len(body)), 
                                   "numDirectQuotes": str(len(directQuotes)), "directQuotes": directQuotes, 
                                   "mentions": mentions, "numMentions": str(len(mentions)), "pred_score": None,
                                   "prediction": None}})
    
    return utteranceData


def updateSpeakerData(json, dirIndex, speakers):
    
    speakerData = {}
    ID = "SP" + str(json['user']['id'])
    
    role = json['author_association']
    
    name = json['user']['login']
    if (name not in speakers):
                speakerData.update({name: {"id": ID, "role": role, "type": json['user']['type'], "url": json['user']['html_url'], "avatar": json['user']['avatar_url'],
                                           "site_admin": json['user']['site_admin']}})
                speakers.append(name)
    return speakerData, speakers


def writeExtraData(file_path):
    with open(f'{file_path}/corpus.json', 'w+', encoding="utf-8") as file:
            data = {}
            
            data.update({"from": "GitHubIssues", "numComments": "---", "numParticipants":"---"})
            
            file.write(json.dumps(data))
            file.close()
        
    with open(f'{file_path}/index.json', 'w+', encoding="utf-8") as file:
            
            data = {}
            
            data.update({"utterances-index": {"id": "<class 'str'>", "spID": "<class 'str'>", "rootID": "<class 'str'>", "previousComment": "<class 'str'>", "time": "<class 'str'>", "text": "<class 'str'>", "posReactions": "<class 'int'>", "negReactions": "<class 'int'>", "overallSentiment": "<class 'int'>", "numWords": "<class 'int'>", "numChars": "<class 'int'>"}})
            data.update({"speakers-index": {"id": "<class 'str'>", "role": "<class 'str'>", "type": "<class 'str'>", "url": "<class 'str'>", "avatar": "<class 'str'>", "site_admin": "<class 'bool'>"}})
            data.update({"conversations-index": {"title": "<class 'str'>", "locked": "<class 'bool'>", "state": "<class 'str'>", "state_reason": "<class 'str'>", "heated": "<class 'bool'>", "url": "<class 'str'>", "author": "<class 'str'>", "comments": "<class 'int'>", "repository": "<class 'str'>"}})
            data.update({"overall-index": {"repository": "<class 'str'>", "numComments": "<class 'int'>", "numParticipants": "<class 'int'>", }})
            data.update({"version": "1.0"})               
            
            
            file.write(json.dumps(data))
            file.close()
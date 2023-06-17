import requests
import os
import json
import shutil
import traceback
import time
import sys





def main():
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '-v' or sys.argv[1] == '--validate':
            validateLinks()
        elif sys.argv[1] == '-g' or sys.argv[1] == '--gather':
            gatherPostData()
        elif sys.argv[1] == '-j' or sys.argv[1] == '--jsonFormat':
            jsonFormat()
            
        elif sys.argv[1] == '-f' or sys.argv[1] == '--format':
            formatData()
        elif sys.argv[1] == '-a' or sys.argv[1] == '--all':
            validateLinks()
            gatherPostData()
            jsonFormatSingleCorp()
        elif sys.argv[1] == '-s' or sys.argv[1] == '--singleCorp':
            jsonFormatSingleCorp()
        elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print("Usage: python app.py [OPTION]")
            print("Options:")
            print("  -v, --validate\t\tValidate list of GitHub issue links")
            print("  -g, --gather\t\t\tGather raw post data from valid links")
            print("  -j, --jsonFormat\t\tFormat data into JSON")
            print("  -f, --format\t\t\tFormat data into alternative format (+++$+++)")
            print("  -a, --all\t\t\tRun all options (WITH JSON FORMATTING IN ONE LARGE CORPUS)")
            print("  -h, --help\t\t\tShow this help message")
        else:
            print("Please enter a valid command | Accepts 1 argument")

    else:
        print("Please enter a valid command | Accepts 1 argument")



        


def validateLinks():
    
    links = []
    
    
    try:
        os.remove('TextFiles/validLinks.txt')
        print("Existing File Removed!")
    except:
        print("File not found")
    
    with open('TextFiles/links.txt', 'r') as f:
        for line in f:
            link = line.strip()
            url = link.replace("https://github.com", "https://api.github.com/repos")
            links.append(url)
            
        
    for url in links:
        
        try:
            response = requests.get(url, headers={"Authorization": "Bearer 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"}).json()
            
            if 'comments' not in response:
                pass      
            
            elif response["comments"] >= 3:
                with open('TextFiles/validLinks.txt', 'a') as file:
                    url = url.replace("https://api.github.com/repos", "https://github.com")
                    file.write(url + '\n')                
                    print(f'Added {url}!')
                    
        except Exception as e:
            print("Error with URL: " + url + '\n \n Response: ' + str(response) + '\n \n Error:' + str(e))
        
        
        
        
def gatherPostData():
    
    
    validLinks = []
    with open('TextFiles/validLinks.txt', 'r') as f:
        for line in f:
            link = line.strip()
            url = link.replace("https://github.com", "https://api.github.com/repos")
            validLinks.append(url)
            
    for url in validLinks:
        
        
        
        try:
            
            response = requests.get(url, headers={"Authorization": "Bearer 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"}).json()
            
            id = 'Issue' + response['user']['login'] + str(response['number'])
            
            if (os.path.exists(f'JSONFiles/{id}')):
                os.remove(f'JSONFiles/{id}')
                print("Removed Existing Directory!")
                
            os.makedirs(f'JSONFiles/{id}')
            print("Created Directory")            
            with open(f'JSONFiles/{id}/Post.json', 'w+') as file:
                json.dump(response, file, indent=4, sort_keys=True)
                print(f'Successfully Gathered Post Data For: {id}')
            
            response = requests.get(response['comments_url'], headers={"Authorization": "Bearer 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"}).json()
            with open(f'JSONFiles/{id}/Comments.json', 'w+') as file:
                json.dump(response, file, indent=4, sort_keys=True)
                print(f'Successfully Gathered Comment Data For: {id}')
            
            
            
        except Exception as e:
            print("Error with URL: " + url + '\n \n Response: ' + str(response) + '\n \n Error:' + str(e) + '\n\nTraceback: ') 
            traceback.print_exc()
            
def formatData():
        
        div = "+++$+++"
        
        if os.path.exists('FormattedData'):
           shutil.rmtree('FormattedData')
           print("Removed Existing Directory!")
                
        
        
        try:
            for dirIndex, dir in enumerate(os.listdir('JSONFiles'), start=0):
                
                speakers = []
                
                postJson = json.load(open(f'JSONFiles/{dir}/Post.json'))
                commentsJson = json.load(open(f'JSONFiles/{dir}/Comments.json'))
                
                #Generate Utterences (And Speakers.txt)
                
                os.makedirs(f'FormattedData/COV{dirIndex}')
                with open(f'FormattedData/COV{dirIndex}/ReferenceData.txt', 'w+') as file:
                    file.write("URL: " + postJson['url'] + '\nNumber of Comments: ' + str(postJson['comments']))
                    file.close()
                    
                    
                
                    
                with open(f'FormattedData/COV{dirIndex}/Utterances.txt', 'a+', encoding="utf-8") as file:
                    
                    authID = "SP" + str(postJson['user']['id'])
                    postTime = postJson['created_at']
                    postBody = postJson['title'] + " " + postJson['body']
                    postPosReactions = str(postJson['reactions']['+1'])
                    postNegReactions = str(postJson['reactions']['-1'])
                    
                    authName = postJson['user']['login']
                    role = postJson['author_association'] + " " + "(AUTHOR)"
                    
                    
                    
                    data = f"ROOT {div} {authID} {div} ROOT {div} ROOT {div} {postTime} {div} {postBody} {div} {postPosReactions} {div} {postNegReactions}"
                    
                    file.write(data + "\n")
                    file.close()
                    
                    with open(f'FormattedData/COV{dirIndex}/Speakers.txt', 'w+') as file2:
                            file2.write(f"{authID} {div} {authName} {div} {role}\n")
                            speakers.append(authName)
                            print('Added Author!')
                    
                
                    
                    
                
                for comIndex, comment in enumerate(commentsJson, start=0):
                    speakerID = "SP" + str(comment['user']['id'])
                    speakerName = comment['user']['login']
                    role = comment['author_association']
                    
                    commentID = f"COM{comIndex}"
                    commentTime = comment['created_at']
                    commentBody = comment['body']
                    posReactions = str(comment['reactions']['+1'])
                    negReactions = str(comment['reactions']['-1'])
                    
                    if (comment['user']['login'] not in speakers):
                        
                        with open(f'FormattedData/COV{dirIndex}/Speakers.txt', 'a+') as file:
                            file.write(f"{speakerID} {div} {speakerName} {div} {role}\n")
                            file.close()
                        
                        print('Added New Speaker!')
                        speakers.append(comment['user']['login'])
                    
                    with open(f'FormattedData/COV{dirIndex}/Utterances.txt', 'a', encoding="utf-8") as file:
                        
                        
                        if commentID == "COM0":
                            prevCom = "ROOT"
                        else:
                            prevCom = f"COM{comIndex-1}"
                            
                            
                        
                        data = f"{commentID} {div} {speakerID} {div} ROOT {div} {prevCom} {div} {commentTime} {div} {commentBody} {div} {posReactions} {div} {negReactions}\n"
                        
                        file.write(data)
                        file.close()
                        print('Added New Utterance!')
                     
                
        except Exception as e:
            print("Error: " + str(e) + '\n\nTraceback: ')
            traceback.print_exc()
            
def jsonFormat():
    if os.path.exists('Corpuses'):
        shutil.rmtree('Corpuses')
        print("Removed Existing Directory!")
            
        
        
    try:
        for dirIndex, dir in enumerate(os.listdir('JSONFiles'), start=0):
            
            speakers = []
            
            speakerData = {}
            
            postJson = json.load(open(f'JSONFiles/{dir}/Post.json'))
            commentsJson = json.load(open(f'JSONFiles/{dir}/Comments.json'))
            
            
            
            #Generate Utterences (And Speakers.txt)
            
            os.makedirs(f'Corpuses/COR{dirIndex}')
            
            #Uneeded for corpuses
            # with open(f'Corpuses/COR{dirIndex}/ReferenceData.txt', 'w+') as file:
            #     file.write("URL: " + postJson['url'] + '\nNumber of Comments: ' + str(postJson['comments']))
            #     file.close()
                
                
            with open(f'Corpuses/COR{dirIndex}/conversations.json', 'w+', encoding="utf-8") as file:
                
                data = {}
                
                data.update({f"COR{dirIndex}": {"title": postJson['title'], "locked": postJson['locked'], "state": postJson['state'] }})
                
                file.write(json.dumps(data))
                file.close()
                
           
                
            
                
            with open(f'Corpuses/COR{dirIndex}/utterances.jsonl', 'a+', encoding="utf-8") as file:
                
                authID = "SP" + str(postJson['user']['id'])
                postTime = postJson['created_at']
                postBody = (postJson['title'] + " " + postJson['body']).replace('\n', ' ')
                postPosReactions = str(postJson['reactions']['+1'])
                postNegReactions = str(postJson['reactions']['-1'])
                
                authName = postJson['user']['login']
                role = postJson['author_association'] + " " + "(AUTHOR)"
                
                
                                
                data = {}
                
                data.update({"id": "ROOT"})
                data.update({"speaker": authName})
                data.update({"conversation_id": "ROOT"})
                data.update({"reply_to": "ROOT"})
                data.update({"timestamp": postTime})
                data.update({"text": postBody})
                data.update({"meta": {"posReactions": postPosReactions, "negReactions": postNegReactions}})
                              
                file.write(json.dumps(data) + "\n")
                file.close()
                
                    
                    
            speakerData.update({authName: {"id": authID, "role": role}})
            
            speakers.append(authName)
            print('Added Author!')
                
            
                
                
            
            for comIndex, comment in enumerate(commentsJson, start=0):
                speakerID = "SP" + str(comment['user']['id'])
                speakerName = comment['user']['login']
                role = comment['author_association']
                
                commentID = f"COM{comIndex}"
                commentTime = comment['created_at']
                commentBody = comment['body']
                posReactions = str(comment['reactions']['+1'])
                negReactions = str(comment['reactions']['-1'])
                
                if (comment['user']['login'] not in speakers):
                    

                    speakerData.update({speakerName: {"id": speakerID, "role": role}})
                        
                    
                    print('Added New Speaker!')
                    speakers.append(comment['user']['login'])
                
                with open(f'Corpuses/COR{dirIndex}/utterances.jsonl', 'a', encoding="utf-8") as file:
                    
                    
                    if commentID == "COM0":
                        prevCom = "ROOT"
                    else:
                        prevCom = f"COM{comIndex-1}"
                                        
                    data = {}
                    
                    data.update({"id": commentID})
                    data.update({"speaker": speakerName})
                    data.update({"conversation_id": "ROOT"})
                    data.update({"reply_to": prevCom})
                    data.update({"timestamp": commentTime})
                    data.update({"text": commentBody})
                    data.update({"meta": {"posReactions": posReactions, "negReactions": negReactions}})
                   
                    
                    
                    file.write(json.dumps(data) + "\n")
                    file.close()
                    print('Added New Utterance!')
                    
            with open(f'Corpuses/COR{dirIndex}/speakers.json', 'a+') as file:
                                            
                    file.write(json.dumps(speakerData, indent=4))
                    file.close()
                
                    
            with open(f'Corpuses/COR{dirIndex}/corpus.json', 'w+', encoding="utf-8") as file:
                
                data = {}
                
                data.update({"repository": postJson['repository_url'].replace("https://api.github.com/repos/", ""), "numComments": postJson['comments'], "numParticipants": len(speakers)})
                
                file.write(json.dumps(data))
                file.close()
                
            with open(f'Corpuses/COR{dirIndex}/index.json', 'w+', encoding="utf-8") as file:
                
                data = {}
                
                data.update({"utterances-index": {"id": "<class 'str'>", "spID": "<class 'str'>", "rootID": "<class 'str'>", "previousComment": "<class 'str'>", "time": "<class 'str'>", "text": "<class 'str'>", "posReactions": "<class 'int'>", "negReactions": "<class 'int'>"}})
                data.update({"speakers-index": {"id": "<class 'str'>", "role": "<class 'str'>"}})
                data.update({"conversations-index": {"title": "<class 'str'>", "locked": "<class 'bool'>", "state": "<class 'str'>"}})
                data.update({"overall-index": {"repository": "<class 'str'>", "numComments": "<class 'int'>", "numParticipants": "<class 'int'>"}})
                data.update({"version": "1.0"})               
                
                
                file.write(json.dumps(data))
                file.close()
                    
                    
    except Exception as e:
            print("Error: " + str(e) + '\n\nTraceback: ')
            traceback.print_exc()
            

def jsonFormatSingleCorp():
    
    if os.path.exists('MegaCorp'):
        shutil.rmtree('MegaCorp')
        print("Removed Existing Directory!")
            
        
        
    try:
        speakers = []
            
        speakerData = {}
        
        utteranceData = {}
        
        conversationData = {}
        
        corpusData = {}
        
        indexData = {}
        for dirIndex, dir in enumerate(os.listdir('JSONFiles'), start=0):
            
            
            
            
            
            postJson = json.load(open(f'JSONFiles/{dir}/Post.json'))
            commentsJson = json.load(open(f'JSONFiles/{dir}/Comments.json'))
            
            
            
            
            
            #Generate Utterences (And Speakers.txt)
            
            os.makedirs(f'MegaCorp', exist_ok=True)
            
            conversationData.update({f"ROOT{dirIndex}": {"title": postJson['title'], "locked": postJson['locked'], "state": postJson['state'] }})
                
            authID = "SP" + str(postJson['user']['id'])
            postTime = postJson['created_at']
            postBody = (postJson['title'] + " " + postJson['body']).replace('\n', ' ')
            postPosReactions = str(postJson['reactions']['+1'])
            postNegReactions = str(postJson['reactions']['-1'])
            
            authName = postJson['user']['login']
            role = postJson['author_association'] + " " + "(AUTHOR)"
            
            
                            
            
            utteranceData.update({"id": f"ROOT{dirIndex}"})
            utteranceData.update({"user": authName})
            utteranceData.update({"root": f"ROOT{dirIndex}"})
            utteranceData.update({"reply_to": None})
            utteranceData.update({"timestamp": postTime})
            utteranceData.update({"text": postBody})
            utteranceData.update({"meta": {"posReactions": postPosReactions, "negReactions": postNegReactions}})
            
            with open(f"MegaCorp/utterances.jsonl", 'a+', encoding="utf-8") as file:
                    file.write(json.dumps(utteranceData) + '\n')
                    file.close()
            
            if (authName not in speakers):
                speakerData.update({authName: {"id": authID, "role": role}})
                speakers.append(authName)
                
            for comIndex, comment in enumerate(commentsJson, start=0):
                speakerID = "SP" + str(comment['user']['id'])
                speakerName = comment['user']['login']
                role = comment['author_association']
                
                commentID = f"COM{dirIndex}{comIndex}"
                commentTime = comment['created_at']
                commentBody = comment['body']
                posReactions = str(comment['reactions']['+1'])
                negReactions = str(comment['reactions']['-1'])
                
                if (comment['user']['login'] not in speakers):
                    
                    speakerData.update({speakerName: {"id": speakerID, "role": role}})
                    speakers.append(comment['user']['login'])
                
                if commentID == f"COM{dirIndex}0":
                    prevCom = f"ROOT{dirIndex}"
                else:
                    prevCom = f"COM{dirIndex}{comIndex-1}"
                                    
                
                utteranceData.update({"id": commentID})
                utteranceData.update({"user": speakerName})
                utteranceData.update({"root": f"ROOT{dirIndex}"})
                utteranceData.update({"reply_to": prevCom})
                utteranceData.update({"timestamp": commentTime})
                utteranceData.update({"text": commentBody})
                utteranceData.update({"meta": {"posReactions": posReactions, "negReactions": negReactions}})
                
                 
                with open(f"MegaCorp/utterances.jsonl", 'a+', encoding="utf-8") as file:
                    file.write(json.dumps(utteranceData) + '\n')
                    file.close()
            
            
        with open(f'MegaCorp/speakers.json', 'a+') as file:
                                    
            file.write(json.dumps(speakerData, indent=4))
            file.close()
            
            
        with open(f'MegaCorp/corpus.json', 'w+', encoding="utf-8") as file:
            data = {}
            
            data.update({"from": "GitHubIssues", "numComments": "---", "numParticipants":"---"})
            
            file.write(json.dumps(data))
            file.close()
        
        with open(f'MegaCorp/index.json', 'w+', encoding="utf-8") as file:
                
                data = {}
                
                data.update({"utterances-index": {"id": "<class 'str'>", "spID": "<class 'str'>", "rootID": "<class 'str'>", "previousComment": "<class 'str'>", "time": "<class 'str'>", "text": "<class 'str'>", "posReactions": "<class 'int'>", "negReactions": "<class 'int'>"}})
                data.update({"speakers-index": {"id": "<class 'str'>", "role": "<class 'str'>"}})
                data.update({"conversations-index": {"title": "<class 'str'>", "locked": "<class 'bool'>", "state": "<class 'str'>"}})
                data.update({"overall-index": {"repository": "<class 'str'>", "numComments": "<class 'int'>", "numParticipants": "<class 'int'>"}})
                data.update({"version": "1.0"})               
                
                
                file.write(json.dumps(data))
                file.close()
        
        with open(f"MegaCorp/conversations.json", 'w+', encoding="utf-8") as file:
            file.write(json.dumps(conversationData, indent=4))
            file.close()
        
            
    except Exception as e:
            print("Error: " + str(e) + '\n\nTraceback: ')
            traceback.print_exc()
            
    
            
        

if __name__ == '__main__':
    main()
    
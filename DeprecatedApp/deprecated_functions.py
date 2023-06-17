import os, shutil, json, traceback

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
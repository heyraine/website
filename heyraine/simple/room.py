import requests
from requests_oauthlib import OAuth1
import json
import time #to make a delay
import sys
from watson_developer_cloud import ToneAnalyzerV3Beta

##import pyaudio
##import wave

#global variables - const
  #my auth key
auth = "NmQ5MGQ0NzYtOWI4OS00ODc1LTgyYmItZGE2YzdhMjU1OGM2NDQ0OWVhYmEtNGJl" 
headers = {"Authorization":"Bearer " + auth}

def main():
  print("running room.py")
  room_json = makeRoom()
  roomID = (room_json['id'])
  person_json = addPerson(roomID) #pass in personEmail as a paramater here
                                  #or as variable and pass it
  personID = (person_json['personId'])
  #personDisplayName = (person_json['personDisplayName'])
  
  count = 0
  sendFirstMessage(roomID)
  while (count < 3): #run 3 times. 3 responses from user,
                      #3 responses from Watson.
    messages_json = _getMessages(roomID, personID)    
    personMessage = (messages_json['items'][0]['text'])
    print("person: " + personMessage)#give personMessage to Watson
    sendMessage(roomID, personMessage)
    count += 1
    
  deleteRoom(roomID, room_json)


def makeRoom():
  url = "https://api.ciscospark.com/v1/rooms"
  req = requests.post(url,\
                    json = { "title" : "new room 1" },\
                    headers = headers)
  room_json = json.loads(req.text)
  return room_json


def addPerson(roomID):
  #personEmail will be given from the textbox of website
  personEmail = input("Please enter your email: ")
  print("\n")
  #personEmail will be given from the textbox of website

  url = "https://api.ciscospark.com/v1/memberships"
  req = requests.post(url,\
                    json = { "roomId": roomID,\
                             "personEmail": personEmail,\
                             "isModerator": "false" },\
                    headers = headers)
  person_json = json.loads(req.text)
  return person_json


def sendFirstMessage(roomID):
  url = "https://api.ciscospark.com/v1/messages"
  messageToSend = "Hello, I'm Raine. How are you?" #default greeting
  req = requests.post(url,\
                    json = { "roomId": roomID,\
                             "text": messageToSend },\
                    headers = headers)
  print("bot: " + messageToSend + '\n')


def sendMessage(roomID, personMessage):
  url = "https://api.ciscospark.com/v1/messages"
  topEmotionList = getWatsonResponse(personMessage)
  messageToSend = "I believe you are feeling " + topEmotionList[0] +\
                  " " + topEmotionList[1]
  
  req = requests.post(url,\
                    json = { "roomId": roomID,\
                             "text": messageToSend },\
                    headers = headers)  
  print("bot: " + messageToSend + '\n')


def getWatsonResponse(personMessage):
  tone_analyzer = ToneAnalyzerV3Beta(
    	username='994597b6-aacb-4b24-9235-4d8c1aa02a6a',
    	password='zXZydSF5i3VH',
    	version='2016-02-11')
  tone_output = json.dumps(tone_analyzer.tone\
                           (text = personMessage), indent = 2)
  tone_json = json.loads(tone_output)
  
  fiveEmotions = tone_json['document_tone']['tone_categories'][0]['tones']
  topEmotion = analyzeEmotion(fiveEmotions)
  
  fiveSocials = tone_json['document_tone']['tone_categories'][2]['tones']
  topSocial = analyzeSocial(fiveSocials)

  topEmotionList = [topEmotion, topSocial]
  return topEmotionList

def analyzeEmotion(fiveEmotions):
  maxEmote = fiveEmotions[0]['tone_name']
  maxEmoteScore = fiveEmotions[0]['score']
  for i in range(1, 5):
    if (fiveEmotions[i]['score'] > maxEmoteScore):
      maxEmoteScore = fiveEmotions[i]['score']
      maxEmote = fiveEmotions[i]['tone_name']
  return maxEmote


def analyzeSocial(fiveSocials):
  maxEmote = fiveSocials[0]['tone_name']
  maxEmoteScore = fiveSocials[0]['score']
  for i in range(1, 5):
    if (fiveSocials[i]['score'] > maxEmoteScore):
      maxEmoteScore = fiveSocials[i]['score']
      maxEmote = fiveSocials[i]['tone_name']
  return maxEmote


def _getMessages(roomID, personID): #calls getMessages()
                                    #to get json each time
  while(1):
    messages_json = getMessages(roomID)
    latestID = messages_json['items'][0]['personId']
    if(latestID == personID): #If msg came from the user
      break;
    time.sleep(1) #else wait 1 secs and try again
  return messages_json


def getMessages(roomID):
  url = "https://api.ciscospark.com/v1/messages"
  req = requests.get(url,\
                   params = { "roomId": roomID,\
                            "max": 1 },\
                   headers = headers)
  messages_json = json.loads(req.text)
  return messages_json


def deleteRoom(roomID, room_json):
  readyToDelete = input ("Press enter to delete the room and exit ")
  url = "https://api.ciscospark.com/v1/rooms/" + roomID
  req = requests.delete(url, json = room_json, headers = headers)


if __name__ == '__main__':
  main()

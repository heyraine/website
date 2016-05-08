import room
from simple.models import room as room_DB
print("hello")


#roomID = room_DB.roomID
roomID = args.r
#personID = room_DB.personID
personID = args.p
count = 0
room.sendFirstMessage(roomID)
while (count < 3): #run 3 times. 3 responses from user,
                    #3 responses from Watson.
    messages_json = room._getMessages(roomID, personID)
    personMessage = (messages_json['items'][0]['text'])
    room.sendMessage(roomID, personMessage)
    count += 1

"""
from heyraine import settings
from django.core.management import setup_environ
setup_environ(settings)
"""
import argparse # built-in
def parseCmdLineArgs(argv):
    """Function to process input args.
    The various input arguments are defined here. parser.add_argument
        creates a new argument. The function parses the various input
        args passed, and stores them in a list (args). The argparse
        library automatically takes care of the help command.
    Args:
        argv: the input arguments passed through commandline. Simply
            pass in sys.argv from the main function.
    Returns:
        args: a  populated namespace of all the inputted command-line arguments.
    """

    # parse args
    parser = argparse.ArgumentParser(
        description='IO Options')
    # add the arguments available to user
    parser.add_argument('-r', metavar='<roomID>', type=str,
                        help='roomID',
                        default='')
    parser.add_argument('-p', metavar='<personID>', type=str,
                        help='personID',
                        default='')
    # TODO add additional arguments: engine_name,
    # algorithm_name,axes_vars,conditions,config_path
    args = parser.parse_args()
    return args

def main(argv):
    args = parseCmdLineArgs(argv)

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

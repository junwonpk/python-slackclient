import random
import os
import time
from slackclient import SlackClient

BOT_ID = os.environ.get("BOT_ID")

AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

photos = ['http://web.stanford.edu/group/msande-news/cgi-bin/news/wp-content/uploads/2014/06/MValentinesClass_54_MG_8025-lower-res.jpg',
'https://cap.stanford.edu/profiles/viewImage?profileId=41754&type=square',
'https://explorecourses.stanford.edu/instructorPhoto?sunet=mav',
'https://msande.stanford.edu/newsletters/Summer2014/Stanford%20-%20Management%20Science%20&%20Engineering%20Newsletter_files/e288014f-f965-40cd-833a-8d561c5d5295.jpg',
'http://www.hbs.edu/doctoral/PublishingImages/profiles/640x360/valentine_640x360.jpg']

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Hi hi, I'm melbot built by Junwon and Chris!!! @market FB @graphiq south korea @forecast palo alto "
    rand = random.randint(0,4)
    image_url = photos[rand]
    print(image_url)
    attachments = attachments = [{"title": "Professor Valentine!!!",
                                  "image_url": image_url}]
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True, attachments=attachments)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("MelBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

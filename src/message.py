class Message:

    def __init__(self, sender, timestamp, content, msg_type):
        self.sender = sender
        self.timestamp = timestamp
        self.content = content
        self.msg_type = msg_type

    def print_message(self):
        print('type: ' + str(self.msg_type))
        print('sender: ' + str(self.sender))
        print('timestamp: ' + str(self.timestamp))
        print('content: ' + str(self.content))

class Message:

    def __init__(self, sender, timestamp, content):
        self.sender = sender
        self.timestamp = timestamp
        self.content = content

    def print_message(self):
        print('sender: ' + str(self.sender))
        print('timestamp: ' + str(self.timestamp))
        print('content: ' + str(self.content))

import re
from datetime import datetime
from src.message import Message
from src.chat_line_parser import ChatLineParser
import unicodedata


class Chat:
    messages = []
    participants = set()
    parser = ChatLineParser()

    def __init__(self, chat_file):
        self.msg_lines = open(chat_file, 'r', encoding='utf8').readlines()
        valid_regex = r'\d{1,2}\/\d{1,2}\/\d{1,2}\,\s\d{1,2}\:\d{1,2}\s[AP]M\s\-\s'
        last_valid = 0
        exclude_list = []

        for i in range(0, len(self.msg_lines)):
            self.msg_lines[i] = self.msg_lines[i].replace('\n', ' ').replace('\r', ' ')
            if not re.search(valid_regex, self.msg_lines[i]):
                self.msg_lines[last_valid] += self.msg_lines[i]
                exclude_list.append(i)
            else:
                last_valid = i

        self.msg_lines = [msg for msg in self.msg_lines if self.msg_lines.index(msg) not in exclude_list]

    def get_messages(self):
        for msg_line in self.msg_lines:
            msg_type = self.parser.get_type(msg_line)
            sender = self.parser.get_sender(msg_line)
            if sender != 'system':
                self.participants.add(sender)
            timestamp = self.parser.get_timestamp(msg_line)
            content = self.parser.get_content(msg_line)
            self.messages.append(Message(sender, timestamp, content, msg_type))

    def message_counts(self):
        counts = {}
        for p in self.participants:
            counts[p] = 0
        for msg in self.messages:
            if msg.sender != 'system':
                counts[msg.sender] += 1
        for key in counts.keys():
            print('Message count for ' + key + ' = ' + str(counts[key]))

    def word_counts(self):
        word_count = {}
        for p in self.participants:
            word_count[p] = 0
        for msg in self.messages:
            if msg.sender != 'system':
                word_count[msg.sender] += len(msg.content.split())
        for key in word_count.keys():
            print('Word count for ' + key + ' = ' + str(word_count[key]))

    def average_response_time(self):
        replies = []
        first = self.messages[0]
        for msg in self.messages[1:]:
            if msg.sender != first.sender:
                replies.append((first, msg))
            first = msg
        reply_time = {}
        reply_count = {}
        for p in self.participants:
            reply_time[p] = 0
            reply_count[p] = 0
        for r in replies:
            if r[1].sender != 'system':
                reply_count[r[1].sender] += 1
                reply_time[r[1].sender] += (r[1].timestamp - r[0].timestamp).total_seconds()
        for key in reply_time.keys():
            reply_time[key] = (reply_time[key]/reply_count[key]) / 60
        for key in reply_time.keys():
            print('Average reply time for ' + key + ' = ' + str(round(reply_time[key], 2)) + ' minutes')

    def chat_restarts(self, minutes_elapsed, double_reply):
        restarts_counts = {}
        for p in self.participants:
            restarts_counts[p] = 0

        first = self.messages[0]
        for msg in self.messages[1:]:
            elapsed_time = (msg.timestamp - first.timestamp).total_seconds() / 60
            if double_reply:
                if msg.sender == first.sender and msg.sender != 'system' and first.sender != 'system':
                    if elapsed_time > minutes_elapsed:
                        restarts_counts[msg.sender] += 1
            else:
                if elapsed_time > minutes_elapsed and msg.sender != 'system':
                    restarts_counts[msg.sender] += 1
            first = msg
        for key in restarts_counts.keys():
            print('Conversation restarts by ' + key + ' = ' + str(restarts_counts[key]))

    def media_messages(self):
        media_messages = {}
        for p in self.participants:
            media_messages[p] = 0
        for msg in self.messages:
            if '<Media omitted>' in msg.content and msg.sender != 'system':
                media_messages[msg.sender] += 1
        for key in media_messages.keys():
            print('Media messages count for ' + key + ' = ' + str(media_messages[key]))

    def emoticon_counts(self):
        emoticon_counts = {}
        for p in self.participants:
            emoticon_counts[p] = 0

        for msg in self.messages:
            content = list(msg.content)
            for c in content:
                if len(unicodedata.normalize('NFKD', c).encode('ascii', 'ignore').decode()) == 0:
                    if msg.sender != 'system':
                        emoticon_counts[msg.sender] += 1
        for key in emoticon_counts.keys():
            print('Emoticon count for ' + key + ' = ' + str(emoticon_counts[key]))

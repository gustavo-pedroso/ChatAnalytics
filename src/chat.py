import re
from src.message import Message
from src.chat_line_parser import ChatLineParser
import src.regex_file as rf
import unicodedata


class Chat:
    participants = set()
    system_messages = []
    admin_messages = []
    user_messages = []

    stats = {}

    parser = ChatLineParser()

    def __init__(self, chat_file):
        self.msg_lines = open(chat_file, 'r', encoding='utf8').readlines()
        last_valid = 0
        for i in range(0, len(self.msg_lines)):
            self.msg_lines[i] = self.msg_lines[i].replace('\n', ' ').replace('\r', ' ')
            if not re.search(rf.date_regex, self.msg_lines[i]):
                self.msg_lines[last_valid] += self.msg_lines[i]
            else:
                last_valid = i
        self.msg_lines = [msg for msg in self.msg_lines if re.search(rf.date_regex, msg) and len(msg.split()) < 200]

    def get_messages(self):
        messages = []
        for msg_line in self.msg_lines:
            msg_type = self.parser.get_type(msg_line)
            sender = self.parser.get_sender(msg_line)
            if msg_type == 'user':
                self.participants.add(sender)
            timestamp = self.parser.get_timestamp(msg_line)
            content = self.parser.get_content(msg_line)
            messages.append(Message(sender, timestamp, content, msg_type))
        self.system_messages = [msg for msg in messages if msg.msg_type == 'system']
        self.admin_messages = [msg for msg in messages if msg.msg_type == 'admin']
        self.user_messages = [msg for msg in messages if msg.msg_type == 'user']

    def get_stats(self, minutes_elapsed=1440, double_reply=False):
        self.stats['messages_count'] = self.get_messages_count()
        self.stats['words_count'] = self.get_words_count()
        self.stats['average_reply_time_minutes'] = self.get_average_reply_time_minutes()
        self.stats['chat_restarts'] = self.get_chat_restarts(minutes_elapsed, double_reply)
        self.stats['media_count'] = self.get_media_count()
        self.stats['emoticon_counts'] = self.get_emoticon_counts()

    def print_stats(self):
        for key in self.stats.keys():
            print('-------------------------------------------------------------------')
            for stat_key in sorted(self.stats[key].keys(), key=lambda x: -self.stats[key][x]):
                print(key + ' for ' + stat_key + ': ' + str(self.stats[key][stat_key]))

    def get_messages_count(self):
        counts = {}
        for p in self.participants:
            counts[p] = 0
        for msg in self.user_messages:
            counts[msg.sender] += 1
        return counts

    def get_words_count(self):
        word_count = {}
        for p in self.participants:
            word_count[p] = 0
        for msg in self.user_messages:
            word_count[msg.sender] += len(msg.content.split())
        return word_count

    def get_average_reply_time_minutes(self):
        replies = []
        first = self.user_messages[0]
        for msg in self.user_messages[1:]:
            if msg.sender != first.sender:
                replies.append((first, msg))
            first = msg
        reply_time = {}
        reply_count = {}
        for p in self.participants:
            reply_time[p] = 0
            reply_count[p] = 0
        for r in replies:
            reply_count[r[1].sender] += 1
            reply_time[r[1].sender] += (r[1].timestamp - r[0].timestamp).total_seconds()
        for key in reply_time.keys():
            reply_time[key] = round((reply_time[key]/reply_count[key]) / 60, 2)
        return reply_time

    def get_chat_restarts(self, minutes_elapsed, double_reply):
        restarts_counts = {}
        for p in self.participants:
            restarts_counts[p] = 0
        first = self.user_messages[0]
        for msg in self.user_messages[1:]:
            elapsed_time = (msg.timestamp - first.timestamp).total_seconds() / 60
            if double_reply:
                if msg.sender == first.sender:
                    if elapsed_time > minutes_elapsed:
                        restarts_counts[msg.sender] += 1
            else:
                if elapsed_time > minutes_elapsed and msg.sender != 'system':
                    restarts_counts[msg.sender] += 1
            first = msg
        return restarts_counts

    def get_media_count(self):
        media_messages = {}
        for p in self.participants:
            media_messages[p] = 0
        for msg in self.user_messages:
            if '<Media omitted>' in msg.content:
                media_messages[msg.sender] += 1
        return media_messages

    def get_emoticon_counts(self):
        emoticon_counts = {}
        for p in self.participants:
            emoticon_counts[p] = 0
        for msg in self.user_messages:
            content = list(msg.content)
            for c in content:
                if len(unicodedata.normalize('NFKD', c).encode('ascii', 'ignore').decode()) == 0:
                    emoticon_counts[msg.sender] += 1
        return emoticon_counts

import re
from datetime import datetime
import src.regex_file as rf


class ChatLineParser:

    def __init__(self):
        self.types = set()

    def get_type(self, msg_line):
        msg_line = re.sub(rf.date_regex, '', msg_line)
        if re.search(rf.system_msg_regex, msg_line):
            msg_type = 'system'
        elif re.search(rf.admin_msg_regex, msg_line):
            msg_type = 'admin'
        elif re.search(rf.user_msg_regex, msg_line):
            msg_type = 'user'
        else:
            msg_type = 'other'
        self.types.add(msg_type)
        return msg_type

    def get_sender(self, msg_line):
        msg_line = re.sub(rf.date_regex, '', msg_line)
        if self.get_type(msg_line) == 'system':
            return 'system'
        elif self.get_type(msg_line) == 'admin':
            return re.findall(rf.admin_msg_regex, msg_line)[0][0]
        elif self.get_type(msg_line) == 'user':
            return re.findall(rf.user_msg_regex, msg_line)[0][0].replace('\u202a', '').replace('\u202c', '')
        else:
            return None

    def get_content(self, msg_line):
        msg_line = re.sub(rf.date_regex, '', msg_line)
        if self.get_type(msg_line) == 'system':
            return msg_line
        elif self.get_type(msg_line) == 'admin':
            content = re.findall(rf.admin_msg_regex, msg_line)[0][1:]
            return ' '.join((' '.join(content)).split())
        elif self.get_type(msg_line) == 'user':
            return re.findall(rf.user_msg_regex, msg_line)[0][1]
        else:
            return None

    @staticmethod
    def get_timestamp(msg_line):
        timestamp = re.findall(rf.date_regex, msg_line)[0]
        day = timestamp[0].split('/')
        day = '/'.join(['0' + x if len(x) == 1 else x for x in day])
        hour = timestamp[1].strip().split(':')
        hour = (hour[0] if len(hour[0]) == 2 else '0' + hour[0]) + ':' + hour[1]
        timestamp = datetime.strptime(day + hour + timestamp[2], "%m/%d/%y%I:%M%p")
        return timestamp

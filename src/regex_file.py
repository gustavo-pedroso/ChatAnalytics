system_msg_regex = r"(You\swere\sadded|You're\snow\san\sadmin|Messages\sto\sthis\sgroup\sare\snow\ssecured\swith" \
                   r"\send-to-end\sencryption.\sTap\sfor\smore\sinfo.|Messages\sto\sthis\schat\sand\scalls\sare\snow" \
                   r"\ssecured\swith\send-to-end\sencryption.\sTap\sfor\smore\sinfo.|(.*)" \
                   r"\s(left|changed\stheir|changed\sto)|You\schanged\sthe\ssubject(.*))"

admin_msg_regex = r"(.*)\s(added|removed|created\sgroup|changed\sthe\ssubject)\s(.*)"

date_regex = r"(\d{1,2}\/\d{1,2}\/\d{2}),\s(\d{1,2}:\d{2})\s(AM|PM)\s\-\s"

user_msg_regex = r"([^:]*):\s(.*)"

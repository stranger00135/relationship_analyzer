from datetime import datetime
from collections import defaultdict


def parse_chat_history(lines):
    chat_by_month = defaultdict(list)
    first_message = None
    last_message = None
    total_messages = 0
    total_word_count = 0
    message_dates = []

    total_lines = len(lines)

    for i, line in enumerate(lines):
        if "]" in line and " - " not in line:
            try:
                timestamp_part, message_part = line.split("]", 1)
                timestamp_str = timestamp_part.strip("[")
                message = message_part.strip()

                timestamp = datetime.strptime(timestamp_str, '%d/%m/%y, %I:%M:%S %p')
                month_str = timestamp.strftime('%Y-%m')

                chat_by_month[month_str].append(message)
                message_dates.append(timestamp.date())
                total_messages += 1
                total_word_count += len(message.split())

                if first_message is None:
                    first_message = (timestamp_str, message)
                last_message = (timestamp_str, message)
            except (ValueError, IndexError):
                continue

    if message_dates:
        num_days = (max(message_dates) - min(message_dates)).days + 1
        avg_messages_per_day = total_messages / num_days
    else:
        num_days = 0
        avg_messages_per_day = 0

    return {
        'chat_by_month': chat_by_month,
        'first_message': first_message,
        'last_message': last_message,
        'total_messages': total_messages,
        'total_word_count': total_word_count,
        'avg_messages_per_day': avg_messages_per_day,
        'num_days': num_days
    }

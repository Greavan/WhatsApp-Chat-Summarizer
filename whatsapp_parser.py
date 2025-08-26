import re
import pandas as pd
from datetime import datetime

def parse_whatsapp_chat(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        chat_content = f.read()

    # Pattern to handle WhatsApp export format: date, time - sender: message
    message_pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{4}),\s*(\d{1,2}:\d{2}(?::\d{2})?\s*(?:am|pm)?)\s*-\s*([^:]+):\s*(.*)', re.MULTILINE | re.IGNORECASE)

    messages = []
    for line in chat_content.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        match = message_pattern.match(line)
        if match:
            date_str, time_str, sender, message = match.groups()
            
            # Handle 12-hour time format and convert to 24-hour
            if 'am' in time_str.lower() or 'pm' in time_str.lower():
                # Remove am/pm and get the time
                time_clean = time_str.lower().replace('am', '').replace('pm', '').strip()
                parts = time_clean.split(':')
                hour = int(parts[0])
                minute = parts[1] if len(parts) > 1 else '00'
                second = parts[2] if len(parts) > 2 else '00'
                
                # Convert to 24-hour format
                if 'pm' in time_str.lower() and hour != 12:
                    hour += 12
                elif 'am' in time_str.lower() and hour == 12:
                    hour = 0
                
                time_str = f"{hour:02d}:{minute}:{second}"
            
            # Ensure time has seconds
            if time_str.count(':') == 1:
                time_str += ':00'
            
            timestamp_str = f"{date_str} {time_str}"
            try:
                timestamp = datetime.strptime(timestamp_str, '%d/%m/%Y %H:%M:%S')
            except ValueError:
                timestamp = None
                
            messages.append({'timestamp': timestamp, 'sender': sender.strip(), 'message': message.strip()})
        elif messages:  # Append to the last message if it's a continuation line
            messages[-1]['message'] += '\n' + line.strip()

    df = pd.DataFrame(messages)
    return df

if __name__ == '__main__':
    # Test with the actual temp_chat.txt file
    try:
        df = parse_whatsapp_chat('temp_chat.txt')
        print("Parsed messages:")
        print(df.head(10).to_string())
        print(f"\nTotal messages parsed: {len(df)}")
    except FileNotFoundError:
        print("temp_chat.txt not found, testing with test_chat.txt")
        df = parse_whatsapp_chat('test_chat.txt')
        print(df.to_string())



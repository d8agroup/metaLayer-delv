import imaplib
import email

def extract_body(payload):
    if isinstance(payload,str):
        return payload
    else:
        return '\n'.join([extract_body(part.get_payload()) for part in payload])

def extract_email_subjects(user_name, password, count=20):
    return_data = []
    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    conn.login(user_name, password)
    conn.select()
    typ, data = conn.search(None, 'ALL')
    try:
        data = data[0].split()
        data.reverse()
        data = data[0:count] if len(data) > count else data
        for num in data:
            typ, msg_data = conn.fetch(num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    date = msg['date']
                    subject = msg['subject']                   
                    return_data.append({ 'subject':subject, 'date':date })
                    
                    #payload=msg.get_payload()
                    #body=extract_body(payload)
            typ, response = conn.store(num, '+FLAGS', r'(\Seen)')
    finally:
        try:
            conn.close()
        except:
            pass
        conn.logout()
        
    return return_data

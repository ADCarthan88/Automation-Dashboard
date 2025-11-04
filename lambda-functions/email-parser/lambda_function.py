import json
import re
from datetime import datetime

def lambda_handler(event, context):
    try:
        email_content = event.get('email_content', '')
        
        # Extract key information from email
        parsed_data = {
            'sender': extract_sender(email_content),
            'subject': extract_subject(email_content),
            'date': extract_date(email_content),
            'attachments': extract_attachments(email_content),
            'action_items': extract_action_items(email_content),
            'priority': determine_priority(email_content)
        }
        
        return {
            'statusCode': 200,
            'body': {
                'success': True,
                'parsed_data': parsed_data,
                'processed_at': datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {
                'success': False,
                'error': str(e)
            }
        }

def extract_sender(content):
    pattern = r'From:\s*([^\n]+)'
    match = re.search(pattern, content, re.IGNORECASE)
    return match.group(1).strip() if match else 'Unknown'

def extract_subject(content):
    pattern = r'Subject:\s*([^\n]+)'
    match = re.search(pattern, content, re.IGNORECASE)
    return match.group(1).strip() if match else 'No Subject'

def extract_date(content):
    pattern = r'Date:\s*([^\n]+)'
    match = re.search(pattern, content, re.IGNORECASE)
    return match.group(1).strip() if match else datetime.now().isoformat()

def extract_attachments(content):
    pattern = r'attachment[s]?:\s*([^\n]+)'
    matches = re.findall(pattern, content, re.IGNORECASE)
    return matches

def extract_action_items(content):
    patterns = [
        r'action item[s]?:\s*([^\n]+)',
        r'todo:\s*([^\n]+)',
        r'follow up:\s*([^\n]+)'
    ]
    
    action_items = []
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        action_items.extend(matches)
    
    return action_items

def determine_priority(content):
    high_priority_keywords = ['urgent', 'asap', 'critical', 'emergency']
    content_lower = content.lower()
    
    for keyword in high_priority_keywords:
        if keyword in content_lower:
            return 'high'
    
    return 'normal'
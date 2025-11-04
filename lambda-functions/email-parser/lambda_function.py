import json
import re
from datetime import datetime, timezone
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        logger.info(f"Processing email parse request: {context.aws_request_id}")
        
        if not event or 'email_content' not in event:
            raise ValueError("Missing required parameter: email_content")
            
        email_content = event.get('email_content', '')
        
        if not email_content.strip():
            raise ValueError("Email content cannot be empty")
        
        # Extract key information from email
        parsed_data = {
            'sender': extract_sender(email_content),
            'subject': extract_subject(email_content),
            'date': extract_date(email_content),
            'attachments': extract_attachments(email_content),
            'action_items': extract_action_items(email_content),
            'priority': determine_priority(email_content)
        }
        
        logger.info(f"Email parsing completed successfully: {context.aws_request_id}")
        
        return {
            'statusCode': 200,
            'body': {
                'success': True,
                'parsed_data': parsed_data,
                'processed_at': datetime.now(timezone.utc).isoformat()
            }
        }
        
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        return {
            'statusCode': 400,
            'body': {
                'success': False,
                'error': str(ve)
            }
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'success': False,
                'error': 'Internal server error'
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
    return match.group(1).strip() if match else datetime.now(timezone.utc).isoformat()

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
    try:
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            action_items.extend([match.strip() for match in matches if match.strip()])
    except re.error as e:
        logger.warning(f"Regex error in action items extraction: {e}")
    
    return list(set(action_items))  # Remove duplicates

def determine_priority(content):
    high_priority_keywords = ['urgent', 'asap', 'critical', 'emergency']
    content_lower = content.lower()
    
    for keyword in high_priority_keywords:
        if keyword in content_lower:
            return 'high'
    
    return 'normal'
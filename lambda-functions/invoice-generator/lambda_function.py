import json
from datetime import datetime, timedelta
import uuid

def lambda_handler(event, context):
    try:
        client_info = event.get('client_info', {})
        items = event.get('items', [])
        
        invoice = generate_invoice(client_info, items)
        
        return {
            'statusCode': 200,
            'body': {
                'success': True,
                'invoice': invoice,
                'generated_at': datetime.now().isoformat()
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

def generate_invoice(client_info, items):
    invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
    
    subtotal = sum(item.get('quantity', 0) * item.get('price', 0) for item in items)
    tax_rate = 0.08
    tax_amount = subtotal * tax_rate
    total = subtotal + tax_amount
    
    invoice = {
        'invoice_number': invoice_number,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'due_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
        'client': {
            'name': client_info.get('name', 'Unknown Client'),
            'email': client_info.get('email', ''),
            'address': client_info.get('address', '')
        },
        'items': items,
        'subtotal': round(subtotal, 2),
        'tax_rate': tax_rate,
        'tax_amount': round(tax_amount, 2),
        'total': round(total, 2),
        'status': 'pending'
    }
    
    return invoice
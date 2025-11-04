import json
from datetime import datetime, timedelta, timezone
import uuid
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        logger.info(f"Processing invoice generation: {context.aws_request_id}")
        
        if not event:
            raise ValueError("Missing event data")
            
        client_info = event.get('client_info', {})
        items = event.get('items', [])
        
        # Validate required fields
        if not client_info.get('name'):
            raise ValueError("Client name is required")
        
        if not items or not isinstance(items, list):
            raise ValueError("At least one invoice item is required")
        
        invoice = generate_invoice(client_info, items)
        
        logger.info(f"Invoice generated successfully: {invoice['invoice_number']}")
        
        return {
            'statusCode': 200,
            'body': {
                'success': True,
                'invoice': invoice,
                'generated_at': datetime.now(timezone.utc).isoformat()
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

def generate_invoice(client_info, items):
    try:
        invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
        
        # Validate and calculate totals
        validated_items = []
        subtotal = 0
        
        for item in items:
            quantity = float(item.get('quantity', 0))
            price = float(item.get('price', 0))
            
            if quantity <= 0 or price < 0:
                raise ValueError(f"Invalid quantity or price for item: {item.get('description', 'Unknown')}")
            
            validated_items.append({
                'description': item.get('description', 'No description'),
                'quantity': quantity,
                'price': price,
                'total': round(quantity * price, 2)
            })
            
            subtotal += quantity * price
        
        tax_rate = 0.08
        tax_amount = subtotal * tax_rate
        total = subtotal + tax_amount
        
        now = datetime.now(timezone.utc)
        
        invoice = {
            'invoice_number': invoice_number,
            'date': now.strftime('%Y-%m-%d'),
            'due_date': (now + timedelta(days=30)).strftime('%Y-%m-%d'),
            'client': {
                'name': client_info.get('name', 'Unknown Client'),
                'email': client_info.get('email', ''),
                'address': client_info.get('address', '')
            },
            'items': validated_items,
            'subtotal': round(subtotal, 2),
            'tax_rate': tax_rate,
            'tax_amount': round(tax_amount, 2),
            'total': round(total, 2),
            'status': 'pending'
        }
        
        return invoice
        
    except (ValueError, TypeError) as e:
        logger.error(f"Error generating invoice: {str(e)}")
        raise ValueError(f"Invoice generation failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in invoice generation: {str(e)}")
        raise
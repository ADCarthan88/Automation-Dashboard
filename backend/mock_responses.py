from datetime import datetime, timezone

def mock_email_parse():
    return {
        'success': True,
        'parsed_data': {
            'sender': 'sarah.johnson@techcorp.com',
            'subject': 'URGENT: Project Deadline Update - Action Required',
            'date': '2024-01-15 14:30:00',
            'attachments': ['project_specs.pdf', 'budget_draft.xlsx'],
            'action_items': [
                'Review the technical specifications by Friday',
                'Schedule a team meeting for next week',
                'Update the project timeline',
                'Finalize the budget proposal',
                'Contact the vendor for pricing',
                'Please confirm your availability for the meeting'
            ],
            'priority': 'high'
        },
        'processed_at': datetime.now(timezone.utc).isoformat()
    }

def mock_invoice_generate():
    return {
        'success': True,
        'invoice': {
            'invoice_number': 'INV-A7B9C2D1',
            'date': '2024-01-15',
            'due_date': '2024-02-14',
            'client': {
                'name': 'Acme Corporation',
                'email': 'billing@acmecorp.com',
                'address': '123 Business Avenue, Suite 500, New York, NY 10001'
            },
            'items': [
                {
                    'description': 'Web Application Development',
                    'quantity': 40,
                    'price': 125.00,
                    'total': 5000.00
                },
                {
                    'description': 'UI/UX Design Services',
                    'quantity': 20,
                    'price': 95.00,
                    'total': 1900.00
                },
                {
                    'description': 'Project Management',
                    'quantity': 10,
                    'price': 150.00,
                    'total': 1500.00
                }
            ],
            'subtotal': 8400.00,
            'tax_rate': 0.08,
            'tax_amount': 672.00,
            'total': 9072.00,
            'status': 'pending'
        },
        'generated_at': datetime.now(timezone.utc).isoformat()
    }

def mock_lead_score(company_size=1500):
    if company_size >= 1000:
        return {
            'success': True,
            'lead_score': {
                'score': 90,
                'quality': 'hot',
                'factors': [
                    'Large company (+30)',
                    'High-value industry: technology (+25)',
                    'High budget (+40)',
                    'High engagement (+20)',
                    'Decision maker (+15)'
                ],
                'lead_data': {
                    'company_size': company_size,
                    'industry': 'technology',
                    'budget': 250000,
                    'engagement_level': 'high',
                    'is_decision_maker': True
                }
            },
            'scored_at': datetime.now(timezone.utc).isoformat()
        }
    else:
        return {
            'success': True,
            'lead_score': {
                'score': 45,
                'quality': 'warm',
                'factors': [
                    'Medium company (+20)',
                    'High-value industry: finance (+25)'
                ],
                'lead_data': {
                    'company_size': company_size,
                    'industry': 'finance',
                    'budget': 75000,
                    'engagement_level': 'medium',
                    'is_decision_maker': False
                }
            },
            'scored_at': datetime.now(timezone.utc).isoformat()
        }
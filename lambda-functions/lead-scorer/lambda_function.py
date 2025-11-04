import json
from datetime import datetime

def lambda_handler(event, context):
    try:
        lead_data = event.get('lead_data', {})
        score_result = calculate_lead_score(lead_data)
        
        return {
            'statusCode': 200,
            'body': {
                'success': True,
                'lead_score': score_result,
                'scored_at': datetime.now().isoformat()
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

def calculate_lead_score(lead_data):
    score = 0
    factors = []
    
    company_size = lead_data.get('company_size', 0)
    if company_size > 1000:
        score += 30
        factors.append('Large company (+30)')
    elif company_size > 100:
        score += 20
        factors.append('Medium company (+20)')
    elif company_size > 10:
        score += 10
        factors.append('Small company (+10)')
    
    industry = lead_data.get('industry', '').lower()
    high_value_industries = ['technology', 'finance', 'healthcare']
    if industry in high_value_industries:
        score += 25
        factors.append(f'High-value industry: {industry} (+25)')
    
    budget = lead_data.get('budget', 0)
    if budget > 100000:
        score += 40
        factors.append('High budget (+40)')
    elif budget > 50000:
        score += 25
        factors.append('Medium budget (+25)')
    elif budget > 10000:
        score += 15
        factors.append('Low budget (+15)')
    
    engagement_level = lead_data.get('engagement_level', 'low')
    if engagement_level == 'high':
        score += 20
        factors.append('High engagement (+20)')
    elif engagement_level == 'medium':
        score += 10
        factors.append('Medium engagement (+10)')
    
    is_decision_maker = lead_data.get('is_decision_maker', False)
    if is_decision_maker:
        score += 15
        factors.append('Decision maker (+15)')
    
    if score >= 80:
        quality = 'hot'
    elif score >= 50:
        quality = 'warm'
    elif score >= 25:
        quality = 'cold'
    else:
        quality = 'unqualified'
    
    return {
        'score': score,
        'quality': quality,
        'factors': factors,
        'lead_data': lead_data
    }
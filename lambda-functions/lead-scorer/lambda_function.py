import json
from datetime import datetime, timezone
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        logger.info(f"Processing lead scoring: {context.aws_request_id}")
        
        if not event or 'lead_data' not in event:
            raise ValueError("Missing required parameter: lead_data")
            
        lead_data = event.get('lead_data', {})
        
        if not lead_data:
            raise ValueError("Lead data cannot be empty")
        
        score_result = calculate_lead_score(lead_data)
        
        logger.info(f"Lead scoring completed: {score_result['quality']} ({score_result['score']} points)")
        
        return {
            'statusCode': 200,
            'body': {
                'success': True,
                'lead_score': score_result,
                'scored_at': datetime.now(timezone.utc).isoformat()
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

def calculate_lead_score(lead_data):
    try:
        score = 0
        factors = []
        
        # Validate and score company size
        company_size = int(lead_data.get('company_size', 0))
        if company_size < 0:
            raise ValueError("Company size cannot be negative")
            
        if company_size > 1000:
            score += 30
            factors.append('Large company (+30)')
        elif company_size > 100:
            score += 20
            factors.append('Medium company (+20)')
        elif company_size > 10:
            score += 10
            factors.append('Small company (+10)')
        
        # Validate and score industry
        industry = str(lead_data.get('industry', '')).lower().strip()
        high_value_industries = ['technology', 'finance', 'healthcare']
        if industry in high_value_industries:
            score += 25
            factors.append(f'High-value industry: {industry} (+25)')
        
        # Validate and score budget
        budget = float(lead_data.get('budget', 0))
        if budget < 0:
            raise ValueError("Budget cannot be negative")
            
        if budget > 100000:
            score += 40
            factors.append('High budget (+40)')
        elif budget > 50000:
            score += 25
            factors.append('Medium budget (+25)')
        elif budget > 10000:
            score += 15
            factors.append('Low budget (+15)')
        
        # Validate and score engagement level
        engagement_level = str(lead_data.get('engagement_level', 'low')).lower().strip()
        valid_engagement_levels = ['low', 'medium', 'high']
        if engagement_level not in valid_engagement_levels:
            logger.warning(f"Invalid engagement level: {engagement_level}, defaulting to 'low'")
            engagement_level = 'low'
            
        if engagement_level == 'high':
            score += 20
            factors.append('High engagement (+20)')
        elif engagement_level == 'medium':
            score += 10
            factors.append('Medium engagement (+10)')
        
        # Score decision maker status
        is_decision_maker = bool(lead_data.get('is_decision_maker', False))
        if is_decision_maker:
            score += 15
            factors.append('Decision maker (+15)')
        
        # Determine quality based on score
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
            'lead_data': {
                'company_size': company_size,
                'industry': industry,
                'budget': budget,
                'engagement_level': engagement_level,
                'is_decision_maker': is_decision_maker
            }
        }
        
    except (ValueError, TypeError) as e:
        logger.error(f"Error calculating lead score: {str(e)}")
        raise ValueError(f"Lead scoring failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in lead scoring: {str(e)}")
        raise
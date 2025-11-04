# Troubleshooting Guide

## Common Issues and Solutions

### Backend Issues

#### 1. boto3 Import Warning
**Issue**: Import "boto3" could not be resolved
**Solution**: This is expected in demo mode. The application falls back to mock responses when AWS is not configured.
```bash
cd backend
pip install -r requirements.txt
```

#### 2. Backend Won't Start
**Solution**: Ensure Python dependencies are installed
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Issues

#### 1. npm Dependencies Missing
**Solution**: Install node modules
```bash
cd frontend
npm install
```

#### 2. Port Already in Use
**Solution**: Change the port in package.json or kill the process using the port
```bash
# Windows PowerShell
Stop-Process -Id (Get-NetTCPConnection -LocalPort 3003).OwningProcess -Force
```

#### 3. API Connection Failed
**Solution**: Ensure backend is running on port 8000
- Check `REACT_APP_API_BASE_URL` in `.env` file
- Verify CORS settings in `backend/main.py`

### Lambda Function Issues

#### 1. Timezone Warnings
**Solution**: All datetime objects now use timezone-aware UTC timestamps

#### 2. Performance Issues
**Solution**: Optimized keyword search and error handling implemented

### Security Issues

#### 1. CSRF Protection
**Status**: ✓ Fixed - CSRF token handling added to API client

#### 2. Input Validation
**Status**: ✓ Fixed - Comprehensive validation added to all endpoints

## Error Boundary

The application now includes an Error Boundary component that catches React errors and prevents complete app crashes.

## Best Practices

1. Always validate user input before sending to API
2. Use proper error handling in try-catch blocks
3. Check for null/undefined before accessing nested properties
4. Use timezone-aware datetime objects
5. Implement proper logging for debugging

## Testing

Run the demo:
```bash
# Windows
start-demo.bat

# Unix/Linux
./deploy.sh
```

## Support

For issues not covered here, check the application logs:
- Backend logs: Console where uvicorn is running
- Frontend logs: Browser Developer Console (F12)

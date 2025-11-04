# Dependency Update Guide

## Overview
This guide documents the dependency updates performed on November 4, 2024.

## Backend (Python) Updates

### Updated Dependencies

| Package | Old Version | New Version | Status |
|---------|------------|-------------|--------|
| fastapi | >=0.100.0 | >=0.115.0 | ✅ Updated |
| uvicorn | >=0.20.0 | >=0.32.0 | ✅ Updated |
| boto3 | >=1.30.0 | >=1.35.0 | ✅ Updated |
| pydantic | >=2.0.0 | >=2.9.0 | ✅ Updated |
| python-multipart | >=0.0.5 | >=0.0.12 | ✅ Updated |
| pydantic-settings | N/A | >=2.5.0 | ✅ Added |

### Key Changes
- **uvicorn**: Now includes `[standard]` extra for better performance with websockets support
- **pydantic-settings**: Added for better environment variable management
- **All versions**: Updated to latest stable releases compatible with Python 3.13

### Installation
```bash
cd backend
pip install -r requirements.txt --upgrade
```

## Frontend (React) Updates

### Updated Dependencies

| Package | Old Version | New Version | Notes |
|---------|------------|-------------|-------|
| react | ^18.2.0 | ^18.3.1 | Latest stable |
| react-dom | ^18.2.0 | ^18.3.1 | Latest stable |
| axios | ^1.6.0 | ^1.7.7 | Security fixes |
| react-router-dom | ^6.8.0 | ^6.28.0 | Major updates |
| @mui/material | ^5.15.0 | ^6.1.7 | Major version upgrade |
| @mui/icons-material | ^5.15.0 | ^6.1.7 | Major version upgrade |
| @emotion/react | ^11.11.0 | ^11.13.5 | Latest stable |
| @emotion/styled | ^11.11.0 | ^11.13.5 | Latest stable |
| web-vitals | N/A | ^4.2.4 | Added |

### Breaking Changes - MUI v6
Material-UI v6 includes some breaking changes. Key updates needed:

1. **Theme customization**: Some theme properties have changed
2. **Component props**: Some deprecated props removed
3. **Import paths**: Mostly unchanged

### Installation
```bash
cd frontend
npm install
```

**Note**: If you encounter peer dependency conflicts, use:
```bash
npm install --legacy-peer-deps
```

## Infrastructure (AWS CDK) Updates

### Updated Dependencies

| Package | Old Version | New Version | Notes |
|---------|------------|-------------|-------|
| aws-cdk | 2.87.0 | ^2.164.1 | Latest stable |
| aws-cdk-lib | 2.87.0 | ^2.164.1 | Latest stable |
| typescript | ~4.9.5 | ^5.7.2 | Major version upgrade |
| @types/node | 18.14.6 | ^22.10.0 | Node 22 support |
| @types/jest | ^29.4.0 | ^29.5.14 | Latest stable |
| jest | ^29.5.0 | ^29.7.0 | Latest stable |
| ts-jest | ^29.0.5 | ^29.2.5 | Latest stable |
| ts-node | ^10.9.1 | ^10.9.2 | Latest stable |
| constructs | ^10.0.0 | ^10.4.2 | Latest stable |

### Lambda Runtime Update
- **Changed from**: Python 3.9 (deprecated by AWS)
- **Changed to**: Python 3.13 (latest supported)
- **Added**: Memory size (256 MB) and environment variables

### Installation
```bash
cd infrastructure
npm install
```

## Deprecated Technologies Alert

### React Scripts (CRA)
**Status**: ⚠️ Create React App is no longer actively maintained

**Recommendation**: Consider migrating to Vite or Next.js in the future
- Vite offers faster build times and better DX
- Next.js provides SSR and better production features

**Current Action**: Keeping react-scripts 5.0.1 for stability
**Future Action**: Plan migration to Vite (recommended)

## Testing After Updates

### 1. Backend Testing
```bash
cd backend
python -m pytest  # Run tests
uvicorn main:app --reload  # Test server
```

### 2. Frontend Testing
```bash
cd frontend
npm test  # Run tests
npm start  # Test development server
npm run build  # Test production build
```

### 3. Infrastructure Testing
```bash
cd infrastructure
npm test  # Run tests
npm run build  # Test TypeScript compilation
```

## Known Compatibility Issues

### None Identified
All updates have been tested for compatibility with:
- Python 3.13.7
- Node.js 22.18.0
- Current codebase

## Rollback Instructions

If issues occur, revert using git:
```bash
git checkout HEAD~1 -- backend/requirements.txt
git checkout HEAD~1 -- frontend/package.json
git checkout HEAD~1 -- infrastructure/package.json
git checkout HEAD~1 -- infrastructure/lib/automation-stack.js
```

Then reinstall dependencies:
```bash
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
cd ../infrastructure && npm install
```

## Future Recommendations

1. **Automated Dependency Updates**: Consider using Dependabot or Renovate
2. **Security Scanning**: Implement Snyk or npm audit in CI/CD
3. **Version Pinning**: Consider exact versions for production
4. **Migration to Vite**: Plan migration away from Create React App
5. **Regular Updates**: Schedule quarterly dependency reviews

## Support

For issues related to these updates:
1. Check the [CHANGELOG.md](CHANGELOG.md)
2. Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. Check package changelogs on npm/PyPI

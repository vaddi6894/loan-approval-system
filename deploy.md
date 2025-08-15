# 🚀 Deployment Guide

## GitHub Repository Setup

### 1. Create GitHub Repository
1. Go to [GitHub.com](https://github.com)
2. Click "New repository"
3. Name: `loan-approval-system`
4. Description: `Advanced ML-powered loan approval prediction system with explainable AI`
5. Make it **Public** (for GitHub Pages)
6. Don't initialize with README (we already have one)

### 2. Connect Local Repository
```bash
git remote add origin https://github.com/YOUR_USERNAME/loan-approval-system.git
git branch -M main
git add .
git commit -m "Initial commit: Loan Approval System"
git push -u origin main
```

## Deployment Options

### Option 1: GitHub Pages (Frontend Only)
- **Pros**: Free, automatic deployment, good for demos
- **Cons**: Backend needs separate hosting
- **Best for**: Showcasing the UI/UX

### Option 2: Heroku (Full Stack)
- **Pros**: Easy deployment, supports Python backend
- **Cons**: Free tier discontinued, paid plans
- **Best for**: Full application deployment

### Option 3: Railway (Full Stack)
- **Pros**: Modern platform, good free tier, easy deployment
- **Cons**: Limited free tier
- **Best for**: Production applications

### Option 4: Vercel + Railway (Hybrid)
- **Pros**: Best of both worlds, optimized for each part
- **Cons**: More complex setup
- **Best for**: Professional deployments

## Recommended: GitHub Pages + Railway

### Frontend (GitHub Pages)
1. Repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` (auto-created by GitHub Actions)
4. Folder: `/ (root)`

### Backend (Railway)
1. Go to [Railway.app](https://railway.app)
2. Connect GitHub repository
3. Deploy backend folder
4. Set environment variables
5. Get production URL

## Environment Variables for Production

Create `.env` file in backend:
```env
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=your_production_db_url
SECRET_KEY=your_secret_key
```

## Update Frontend for Production

Update `frontend/script.js`:
```javascript
// Change API_BASE for production
const API_BASE = process.env.NODE_ENV === 'production' 
  ? 'https://your-railway-app.railway.app/api'
  : 'http://127.0.0.1:5000/api';
```

## Testing Deployment

1. **Frontend**: Visit `https://yourusername.github.io/loan-approval-system`
2. **Backend**: Test API endpoints
3. **Integration**: Verify frontend-backend communication

## Monitoring

- **GitHub Actions**: Check workflow runs
- **Railway**: Monitor app performance
- **GitHub Pages**: Check deployment status

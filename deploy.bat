@echo off
REM Loan Approval System - Deployment Script for Windows
REM This script automates the deployment process for GitHub Pages

echo 🚀 Starting Loan Approval System Deployment...

REM Check if we're in the right directory
if not exist "docs\index.html" (
    echo ❌ Error: docs\index.html not found. Please run this script from the project root.
    pause
    exit /b 1
)

REM Add all changes
echo 📝 Adding changes to git...
git add .

REM Commit changes
echo 💾 Committing changes...
git commit -m "Update deployment files"

REM Push to GitHub
echo ⬆️ Pushing to GitHub...
git push origin main

echo ✅ Deployment files pushed to GitHub!
echo.
echo 📋 Next Steps:
echo 1. Go to your GitHub repository: https://github.com/vaddi6894/loan-approval-system.git
echo 2. Navigate to Settings ^> Pages
echo 3. Set Source to 'Deploy from a branch'
echo 4. Select 'main' branch and '/docs' folder
echo 5. Click Save
echo.
echo 🌐 Your site will be available at: https://vaddi6894.github.io/loan-approval-system/
echo.
echo ⚠️  Remember: You still need to host the backend separately!
echo    Check DEPLOYMENT_GUIDE.md for backend hosting options.
echo.
pause

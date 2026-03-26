@echo off
echo ===================================
echo Clearing Django Static Files Cache
echo ===================================
echo.

echo Step 1: Removing staticfiles directory...
if exist staticfiles (
    rmdir /s /q staticfiles
    echo Staticfiles directory removed
) else (
    echo No staticfiles directory found
)
echo.

echo Step 2: Collecting static files...
python manage.py collectstatic --noinput --clear
echo.

echo ===================================
echo Cache cleared successfully!
echo ===================================
echo.
echo IMPORTANT: Now you must:
echo 1. Close your browser completely
echo 2. Reopen your browser
echo 3. Press Ctrl+Shift+Delete
echo 4. Select "All time"
echo 5. Check ALL boxes
echo 6. Click "Clear data"
echo 7. Go to http://127.0.0.1:8000/cted/
echo 8. Press Ctrl+Shift+R (hard refresh)
echo.
pause

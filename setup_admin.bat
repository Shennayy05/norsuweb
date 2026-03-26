@echo off
echo ================================================
echo Creating Super Admin Users
echo ================================================
echo.

python create_superuser.py

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo You can now login at:
echo http://127.0.0.1:8000/super-admin-login/
echo.
echo Credentials:
echo Username: superadmin
echo Password: admin123
echo.
pause

# Flash Arbitrage Bot - Windows Installation Guide

## 🖥️ Windows-Specific Setup Instructions

This guide will help you get the Flash Arbitrage Bot running on Windows systems, addressing common Python compatibility issues.

## ⚠️ Common Windows Issues Fixed

- **setuptools/pkg_resources compatibility errors**
- **Missing Flask and dependencies**
- **Python path and virtual environment issues**
- **Windows-specific file path problems**

## 🔧 Prerequisites

1. **Python 3.8 or higher** (recommended: Python 3.9-3.11)
   - Download from: https://python.org/downloads/
   - ✅ **IMPORTANT**: Check "Add Python to PATH" during installation

2. **Git for Windows** (optional, for cloning)
   - Download from: https://git-scm.com/download/win

## 🚀 Quick Start (Windows)

### Method 1: Automated Setup (Recommended)

1. **Download the repository**:
   ```cmd
   git clone https://github.com/LimitlessJacko/Flash-arb-anchor.git
   cd Flash-arb-anchor
   ```

2. **Run the Windows setup script**:
   ```cmd
   setup-windows.bat
   ```

3. **Start the bot**:
   ```cmd
   start-windows.bat
   ```

4. **Open your browser** to: http://localhost:5000

### Method 2: Manual Setup

1. **Create virtual environment**:
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   ```

2. **Upgrade pip and install dependencies**:
   ```cmd
   python -m pip install --upgrade pip setuptools wheel
   pip install -r requirements-windows.txt
   ```

3. **Start the Windows-compatible version**:
   ```cmd
   python app-windows.py
   ```

## 🛠️ Troubleshooting Windows Issues

### Issue 1: setuptools/pkg_resources Error
```
AttributeError: module 'pkgutil' has no attribute 'ImpImporter'
```

**Solution**:
```cmd
python -m pip install --upgrade pip setuptools==68.2.2 wheel
pip install --no-cache-dir flask flask-cors
```

### Issue 2: ModuleNotFoundError: No module named 'flask'
```
ModuleNotFoundError: No module named 'flask'
```

**Solution**:
```cmd
venv\Scripts\activate.bat
pip install flask flask-cors requests python-dotenv
```

### Issue 3: Virtual Environment Issues

**Solution**:
```cmd
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate.bat
pip install flask flask-cors
```

### Issue 4: Permission Errors

**Solution**:
- Run Command Prompt as Administrator
- Or use PowerShell with execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📁 Windows-Specific Files

- `setup-windows.bat` - Automated setup script
- `start-windows.bat` - Bot launcher
- `app-windows.py` - Windows-compatible Flask app
- `requirements-windows.txt` - Windows-compatible dependencies
- `README-WINDOWS.md` - This file

## ⚙️ Configuration

Your Solana wallet is pre-configured:
```
Wallet: 68Jxdxbe2GC86GoJGBwNeaRAqun1ttyEEntUSnBsokMK
```

To change settings:
1. Open the web dashboard at http://localhost:5000
2. Go to Configuration section
3. Update parameters as needed

## 🎯 Windows Demo Mode Features

The Windows version runs in demo mode with:
- ✅ Full web dashboard interface
- ✅ Configuration management
- ✅ Mock trading simulation
- ✅ Real-time statistics display
- ⚠️ Simulated arbitrage opportunities (for testing)

## 🔄 Updating the Bot

To update to the latest version:
```cmd
git pull origin main
setup-windows.bat
```

## 🐛 Still Having Issues?

### Check Python Version
```cmd
python --version
```
Should show Python 3.8 or higher.

### Check pip Version
```cmd
python -m pip --version
```

### Reinstall Dependencies
```cmd
venv\Scripts\activate.bat
pip uninstall -y flask flask-cors
pip install --no-cache-dir flask==2.3.3 flask-cors==4.0.0
```

### Alternative Python Installation
If you continue having issues, try:
1. Uninstall current Python
2. Download Python 3.9.18 from python.org
3. Install with "Add to PATH" checked
4. Run setup-windows.bat again

## 📞 Support

If you encounter issues:
1. Check this troubleshooting guide
2. Ensure Python 3.8+ is installed correctly
3. Try running as Administrator
4. Create an issue on GitHub with error details

## 🔐 Security Note

The Windows version includes the same security features:
- Wallet address protection
- Configuration validation
- Safe API endpoints

## 📈 Performance

Windows version performance:
- ✅ Web dashboard: Full speed
- ✅ Configuration: Real-time updates
- ⚠️ Trading engine: Demo mode (use Linux for production)

---

**Windows Setup Complete!** 🎉

Your Flash Arbitrage Bot is now ready to run on Windows with your configured wallet address.


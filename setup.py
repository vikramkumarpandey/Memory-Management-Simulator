"""
Setup script for Memory Management Simulator
Team CodeStorm
"""

try:
    import tkinter as tk
    print("✓ tkinter is available")
except ImportError:
    print("✗ tkinter is not available - please install Python with tkinter support")
    exit(1)

try:
    import psutil
    print(f"✓ psutil {psutil.__version__} is available")
except ImportError:
    print("✗ psutil is not available")
    print("Installing psutil...")
    import subprocess
    import sys

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        import psutil
        print(f"✓ psutil {psutil.__version__} installed successfully")
    except Exception as e:
        print(f"✗ Failed to install psutil: {e}")
        print("Please install psutil manually: pip install psutil")
        exit(1)

print("\n=== System Information ===")
try:
    vm = psutil.virtual_memory()
    print(f"Total Memory: {vm.total / (1024**3):.2f} GB")
    print(f"Available Memory: {vm.available / (1024**3):.2f} GB")
    print(f"CPU Count: {psutil.cpu_count()}")
    print(f"Platform: {psutil.os.name}")
    print("\n✓ All dependencies are working correctly!")
    print("\nYou can now run: python main.py")

except Exception as e:
    print(f"✗ Error testing system: {e}")

input("\nPress Enter to continue...")

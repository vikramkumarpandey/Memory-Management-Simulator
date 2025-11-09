# Memory Management Simulator
**Team CodeStorm - Operating Systems Project**

A comprehensive GUI-based simulator for visualizing and managing operating system memory allocation algorithms with real-time system monitoring.

## 🎯 Features

### Core Functionality
- **Memory Allocation Algorithms**: First Fit, Best Fit, Worst Fit, and Paging simulation
- **Real-time System Monitoring**: Live memory, CPU, and process statistics
- **Interactive GUI**: Easy-to-use Tkinter interface with visual feedback
- **Process Management**: Add, remove, and track allocated processes
- **Memory Visualization**: Graphical representation of memory blocks and usage

### Advanced Features
- **Auto-refresh**: Automatic updates of system statistics
- **Multi-platform Support**: Works on Windows and Linux
- **Process List**: Real-time monitoring of running processes
- **Memory Statistics**: Detailed memory, swap, and system information
- **Visual Memory Chart**: Pie chart representation of memory usage

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)
- psutil library

### Quick Setup
1. **Extract the ZIP file** to your desired location
2. **Install dependencies**:
   ```bash
   pip install psutil
   ```
   Or run the setup script:
   ```bash
   python setup.py
   ```
3. **Run the application**:
   ```bash
   python main.py
   ```

### VS Code Setup
1. Open the extracted folder in VS Code
2. Install the Python extension if not already installed
3. Open terminal in VS Code (Ctrl+`)
4. Install requirements: `pip install -r requirements.txt`
5. Run: `python main.py`

## 📁 Project Structure

```
MemoryManagementSimulator/
├── main.py              # Main application GUI and logic
├── algorithms.py        # Memory allocation algorithms
├── monitor.py          # System monitoring functions
├── setup.py            # Setup and dependency check
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔬 Memory Allocation Algorithms

### 1. First Fit
- Allocates the first available block that fits the process
- Fast allocation but can cause fragmentation

### 2. Best Fit
- Allocates the smallest block that fits the process
- Minimizes wasted space but slower than First Fit

### 3. Worst Fit
- Allocates the largest available block
- Leaves largest remaining fragments

### 4. Paging (Simulated)
- Simplified paging simulation
- Always successful allocation

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Windows 7+, Linux (Ubuntu 18.04+), macOS 10.14+
- **Python**: 3.7+
- **RAM**: 512 MB available
- **Storage**: 50 MB free space

### Recommended Requirements
- **OS**: Windows 10+, Linux (Ubuntu 20.04+), macOS 11+
- **Python**: 3.9+
- **RAM**: 2 GB available
- **Storage**: 100 MB free space

## 🎮 How to Use

### 1. Launch Application
```bash
python main.py
```

### 2. Monitor System
- View real-time memory, swap, and CPU statistics
- Monitor running processes with memory usage
- Enable auto-refresh for continuous updates

### 3. Simulate Memory Allocation
- Select an allocation algorithm (First Fit, Best Fit, Worst Fit, Paging)
- Enter Process ID and Memory Size
- Click "Add Process" to simulate allocation
- View visual representation of memory blocks
- Remove processes or reset simulation as needed

### 4. Analyze Results
- Check allocation status messages
- View memory block utilization
- Compare different algorithm performances

## 🐛 Troubleshooting

### Common Issues

**1. "No module named 'psutil'"**
```bash
pip install psutil
```

**2. "tkinter not found"**
- On Ubuntu/Debian: `sudo apt-get install python3-tk`
- On CentOS/RHEL: `sudo yum install tkinter`
- On macOS: Reinstall Python from python.org

**3. Permission denied errors**
- Run as administrator (Windows) or with sudo (Linux)
- Some system monitoring features require elevated privileges

**4. Application doesn't start**
- Check Python version: `python --version`
- Run setup script: `python setup.py`
- Check error messages in console

### Performance Tips
- Disable auto-refresh if system becomes slow
- Close other applications to free up memory
- Use smaller memory block sizes for faster simulation

## 👥 Team Information

**Team Name**: CodeStorm  
**Course**: Operating Systems  
**Project**: Memory Management Visualizer

### Team Members
1. **Khan Shoeb** (Team Lead) - 230211029
2. **Vikram Kumar Pandey** - [Student ID]
3. **Sachin Rawat** - [Student ID]  
4. **Mohammad Anas** - [Student ID]

## 📧 Support

For issues, questions, or contributions:
- Check the troubleshooting section
- Review code comments for technical details
- Test with the provided sample data

## 🏆 Academic Notice

This project is developed for educational purposes as part of an Operating Systems course. The implementation focuses on demonstrating memory management concepts rather than production-level optimization.

---

**© 2025 Team CodeStorm - All Rights Reserved**

*This project demonstrates memory allocation algorithms and system monitoring for educational purposes.*


# Memory Management Simulator (Animated)
**Team CodeStorm - Operating Systems Project (Phase 2 → Phase 3 Ready)**

A GUI-based simulator that **animates every step** of memory allocation like a *video*. Each block is highlighted as it is checked, selected, allocated, and deallocated. Perfect for a 5th-semester OS demo.

## Highlights
- **Step-by-step animation** for First Fit / Best Fit / Worst Fit
- **Video-like log** showing each step textually
- Smooth **fill animation** when a block is allocated/deallocated
- Real-time system monitoring using `psutil`
- Clean Tkinter GUI; Windows-friendly

## Run
```bash
pip install -r requirements.txt
python main.py
```

## Demo Tips
- Use `Step Speed` slider to slow down or speed up the animation.
- Add a process (e.g., PID `P1`, Size `150`) and watch blocks get checked and filled.
- Remove a process to see deallocation animation.


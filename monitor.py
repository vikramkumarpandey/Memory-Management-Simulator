"""
System monitoring functions using psutil
Team CodeStorm - Memory Management Simulator
"""

import psutil
import platform

def get_memory_stats():
    """Get comprehensive memory statistics"""
    try:
        # Virtual memory info
        vm = psutil.virtual_memory()

        # Swap memory info
        swap = psutil.swap_memory()

        # Format memory info
        memory_info = f"""Total: {vm.total / (1024**3):.1f} GB
Used: {vm.used / (1024**3):.1f} GB ({vm.percent:.1f}%)
Available: {vm.available / (1024**3):.1f} GB
Buffers: {getattr(vm, 'buffers', 0) / (1024**3):.1f} GB
Cached: {getattr(vm, 'cached', 0) / (1024**3):.1f} GB"""

        # Format swap info
        swap_info = f"""Total: {swap.total / (1024**3):.1f} GB
Used: {swap.used / (1024**3):.1f} GB ({swap.percent:.1f}%)
Free: {swap.free / (1024**3):.1f} GB"""

        # System details
        sys_info = f"""OS: {platform.system()} {platform.release()}
Architecture: {platform.architecture()[0]}
Processor: {platform.processor()[:30]}
CPU Cores: {psutil.cpu_count(logical=False)}
Logical CPUs: {psutil.cpu_count(logical=True)}
CPU Usage: {psutil.cpu_percent(interval=1):.1f}%"""

        return memory_info, swap_info, sys_info

    except Exception as e:
        error_msg = f"Error getting system stats: {str(e)}"
        return error_msg, error_msg, error_msg

def get_process_list(limit=10):
    """Get list of running processes with memory and CPU usage"""
    try:
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
            try:
                # Get process info
                pid = proc.info['pid']
                name = proc.info['name']
                memory_mb = proc.info['memory_info'].rss / (1024 * 1024)  # Convert to MB
                cpu_percent = proc.info['cpu_percent'] or 0.0

                processes.append([
                    str(pid),
                    name[:25],  # Truncate long names
                    f"{memory_mb:.1f}",
                    f"{cpu_percent:.1f}"
                ])

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Skip processes that can't be accessed
                continue

        # Sort by memory usage (descending) and return top processes
        processes.sort(key=lambda x: float(x[2]), reverse=True)
        return processes[:limit]

    except Exception as e:
        return [["Error", str(e)[:30], "0.0", "0.0"]]

def get_memory_values():
    """Get memory values for visualization"""
    try:
        vm = psutil.virtual_memory()
        total = vm.total / (1024**3)  # Convert to GB
        used = vm.used / (1024**3)
        available = vm.available / (1024**3)
        return total, used, available
    except:
        return 8.0, 4.0, 4.0  # Fallback values

def get_cpu_info():
    """Get detailed CPU information"""
    try:
        cpu_freq = psutil.cpu_freq()
        cpu_times = psutil.cpu_times()

        info = {
            'usage_percent': psutil.cpu_percent(interval=1),
            'core_count': psutil.cpu_count(logical=False),
            'thread_count': psutil.cpu_count(logical=True),
            'frequency_mhz': cpu_freq.current if cpu_freq else 0,
            'user_time': cpu_times.user,
            'system_time': cpu_times.system,
            'idle_time': cpu_times.idle
        }
        return info
    except:
        return {'usage_percent': 0, 'core_count': 4, 'thread_count': 8, 
                'frequency_mhz': 2400, 'user_time': 0, 'system_time': 0, 'idle_time': 0}

def get_disk_usage():
    """Get disk usage information"""
    try:
        disk_usage = psutil.disk_usage('/')
        return {
            'total': disk_usage.total / (1024**3),
            'used': disk_usage.used / (1024**3),
            'free': disk_usage.free / (1024**3),
            'percent': (disk_usage.used / disk_usage.total) * 100
        }
    except:
        return {'total': 500, 'used': 200, 'free': 300, 'percent': 40}

def format_bytes(bytes_value):
    """Format bytes into human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

# Test function
def test_monitoring():
    """Test monitoring functions"""
    print("=== Memory Management Simulator - System Monitor Test ===")
    print()

    # Test memory stats
    mem_info, swap_info, sys_info = get_memory_stats()
    print("Memory Info:")
    print(mem_info)
    print("\nSwap Info:")
    print(swap_info)
    print("\nSystem Info:")
    print(sys_info)

    # Test process list
    print("\nTop Processes:")
    processes = get_process_list(5)
    for proc in processes:
        print(f"PID: {proc[0]:<8} Name: {proc[1]:<25} Memory: {proc[2]:<8} MB CPU: {proc[3]:<6}%")

    # Test memory values
    total, used, available = get_memory_values()
    print(f"\nMemory Summary: {used:.1f}GB used / {total:.1f}GB total ({available:.1f}GB available)")

if __name__ == "__main__":
    test_monitoring()

#!/usr/bin/env python3
"""
System Health Monitor
A beginner DevOps project to monitor system health metrics
"""

import psutil
import json
import datetime
import time
import argparse
import sys
from typing import Dict, Any

class SystemHealthMonitor:
    def __init__(self, alert_thresholds: Dict[str, float] = None):
        """
        Initialize the system health monitor
        
        Args:
            alert_thresholds: Dictionary with threshold values for alerts
        """
        self.alert_thresholds = alert_thresholds or {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get basic system information"""
        try:
            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            return {
                'hostname': psutil.os.uname().nodename,
                'platform': psutil.os.uname().system,
                'architecture': psutil.os.uname().machine,
                'boot_time': boot_time.strftime('%Y-%m-%d %H:%M:%S'),
                'uptime_hours': round((time.time() - psutil.boot_time()) / 3600, 2)
            }
        except Exception as e:
            return {'error': f'Failed to get system info: {str(e)}'}
    
    def get_cpu_info(self) -> Dict[str, Any]:
        """Get CPU usage information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            return {
                'cpu_percent': cpu_percent,
                'cpu_count_logical': cpu_count,
                'cpu_count_physical': psutil.cpu_count(logical=False),
                'cpu_frequency_mhz': round(cpu_freq.current, 2) if cpu_freq else 'N/A',
                'load_average': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else 'N/A'
            }
        except Exception as e:
            return {'error': f'Failed to get CPU info: {str(e)}'}
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Get memory usage information"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'memory_total_gb': round(memory.total / (1024**3), 2),
                'memory_available_gb': round(memory.available / (1024**3), 2),
                'memory_used_gb': round(memory.used / (1024**3), 2),
                'memory_percent': memory.percent,
                'swap_total_gb': round(swap.total / (1024**3), 2),
                'swap_used_gb': round(swap.used / (1024**3), 2),
                'swap_percent': swap.percent
            }
        except Exception as e:
            return {'error': f'Failed to get memory info: {str(e)}'}
    
    def get_disk_info(self) -> Dict[str, Any]:
        """Get disk usage information"""
        try:
            disk_partitions = psutil.disk_partitions()
            disk_info = {}
            
            for partition in disk_partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info[partition.mountpoint] = {
                        'device': partition.device,
                        'filesystem': partition.fstype,
                        'total_gb': round(usage.total / (1024**3), 2),
                        'used_gb': round(usage.used / (1024**3), 2),
                        'free_gb': round(usage.free / (1024**3), 2),
                        'percent': round((usage.used / usage.total) * 100, 2)
                    }
                except PermissionError:
                    # Skip partitions we can't access
                    continue
            
            return disk_info
        except Exception as e:
            return {'error': f'Failed to get disk info: {str(e)}'}
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get network interface information"""
        try:
            network_stats = psutil.net_io_counters(pernic=True)
            network_info = {}
            
            for interface, stats in network_stats.items():
                network_info[interface] = {
                    'bytes_sent': stats.bytes_sent,
                    'bytes_recv': stats.bytes_recv,
                    'packets_sent': stats.packets_sent,
                    'packets_recv': stats.packets_recv,
                    'errors_in': stats.errin,
                    'errors_out': stats.errout
                }
            
            return network_info
        except Exception as e:
            return {'error': f'Failed to get network info: {str(e)}'}
    
    def get_process_info(self, top_n: int = 5) -> Dict[str, Any]:
        """Get information about top processes by CPU and memory usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage
            top_cpu = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:top_n]
            
            # Sort by memory usage
            top_memory = sorted(processes, key=lambda x: x['memory_percent'] or 0, reverse=True)[:top_n]
            
            return {
                'total_processes': len(processes),
                'top_cpu_processes': top_cpu,
                'top_memory_processes': top_memory
            }
        except Exception as e:
            return {'error': f'Failed to get process info: {str(e)}'}
    
    def check_alerts(self, health_data: Dict[str, Any]) -> list:
        """Check if any metrics exceed alert thresholds"""
        alerts = []
        
        # Check CPU
        if 'cpu_info' in health_data and 'cpu_percent' in health_data['cpu_info']:
            cpu_percent = health_data['cpu_info']['cpu_percent']
            if cpu_percent > self.alert_thresholds['cpu_percent']:
                alerts.append(f"HIGH CPU USAGE: {cpu_percent}% (threshold: {self.alert_thresholds['cpu_percent']}%)")
        
        # Check Memory
        if 'memory_info' in health_data and 'memory_percent' in health_data['memory_info']:
            memory_percent = health_data['memory_info']['memory_percent']
            if memory_percent > self.alert_thresholds['memory_percent']:
                alerts.append(f"HIGH MEMORY USAGE: {memory_percent}% (threshold: {self.alert_thresholds['memory_percent']}%)")
        
        # Check Disk
        if 'disk_info' in health_data:
            disk_info = health_data['disk_info']
            if isinstance(disk_info, dict):
                for mount_point, disk_data in disk_info.items():
                    if isinstance(disk_data, dict) and 'percent' in disk_data:
                        disk_percent = disk_data['percent']
                        if disk_percent > self.alert_thresholds['disk_percent']:
                            alerts.append(f"HIGH DISK USAGE: {mount_point} at {disk_percent}% (threshold: {self.alert_thresholds['disk_percent']}%)")
        
        return alerts
    
    def collect_all_metrics(self) -> Dict[str, Any]:
        """Collect all system health metrics"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        health_data = {
            'timestamp': timestamp,
            'system_info': self.get_system_info(),
            'cpu_info': self.get_cpu_info(),
            'memory_info': self.get_memory_info(),
            'disk_info': self.get_disk_info(),
            'network_info': self.get_network_info(),
            'process_info': self.get_process_info()
        }
        
        # Add alerts
        health_data['alerts'] = self.check_alerts(health_data)
        
        return health_data
    
    def save_to_file(self, data: Dict[str, Any], filename: str = None):
        """Save health data to JSON file"""
        if filename is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'system_health_{timestamp}.json'
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Health data saved to: {filename}")
        except Exception as e:
            print(f"Error saving to file: {str(e)}")
    
    def print_summary(self, data: Dict[str, Any]):
        """Print a summary of system health"""
        print("\n" + "="*50)
        print("SYSTEM HEALTH SUMMARY")
        print("="*50)
        print(f"Timestamp: {data['timestamp']}")
        
        # System Info
        if 'system_info' in data:
            sys_info = data['system_info']
            print(f"\nSystem: {sys_info.get('hostname', 'N/A')} ({sys_info.get('platform', 'N/A')})")
            print(f"Uptime: {sys_info.get('uptime_hours', 'N/A')} hours")
        
        # CPU Info
        if 'cpu_info' in data:
            cpu_info = data['cpu_info']
            print(f"\nCPU Usage: {cpu_info.get('cpu_percent', 'N/A')}%")
            print(f"CPU Cores: {cpu_info.get('cpu_count_logical', 'N/A')} logical, {cpu_info.get('cpu_count_physical', 'N/A')} physical")
        
        # Memory Info
        if 'memory_info' in data:
            mem_info = data['memory_info']
            print(f"\nMemory Usage: {mem_info.get('memory_percent', 'N/A')}%")
            print(f"Memory: {mem_info.get('memory_used_gb', 'N/A')} GB / {mem_info.get('memory_total_gb', 'N/A')} GB")
        
        # Disk Info Summary
        if 'disk_info' in data and isinstance(data['disk_info'], dict):
            print("\nDisk Usage:")
            for mount, disk_data in data['disk_info'].items():
                if isinstance(disk_data, dict):
                    print(f"  {mount}: {disk_data.get('percent', 'N/A')}% ({disk_data.get('used_gb', 'N/A')} GB / {disk_data.get('total_gb', 'N/A')} GB)")
        
        # Alerts
        if data.get('alerts'):
            print("\n⚠️  ALERTS:")
            for alert in data['alerts']:
                print(f"  • {alert}")
        else:
            print("\n✅ No alerts - system is healthy!")
        
        print("="*50)

def main():
    parser = argparse.ArgumentParser(description='System Health Monitor')
    parser.add_argument('--save', action='store_true', help='Save results to JSON file')
    parser.add_argument('--output', type=str, help='Output filename')
    parser.add_argument('--cpu-threshold', type=float, default=80.0, help='CPU alert threshold (default: 80%%)')
    parser.add_argument('--memory-threshold', type=float, default=85.0, help='Memory alert threshold (default: 85%%)')
    parser.add_argument('--disk-threshold', type=float, default=90.0, help='Disk alert threshold (default: 90%%)')
    parser.add_argument('--continuous', action='store_true', help='Run continuously (Ctrl+C to stop)')
    parser.add_argument('--interval', type=int, default=30, help='Interval in seconds for continuous monitoring (default: 30)')
    
    args = parser.parse_args()
    
    # Set up thresholds
    thresholds = {
        'cpu_percent': args.cpu_threshold,
        'memory_percent': args.memory_threshold,
        'disk_percent': args.disk_threshold
    }
    
    monitor = SystemHealthMonitor(thresholds)
    
    try:
        if args.continuous:
            print(f"Starting continuous monitoring (interval: {args.interval} seconds)")
            print("Press Ctrl+C to stop")
            
            while True:
                health_data = monitor.collect_all_metrics()
                monitor.print_summary(health_data)
                
                if args.save:
                    monitor.save_to_file(health_data, args.output)
                
                time.sleep(args.interval)
        else:
            # Single run
            health_data = monitor.collect_all_metrics()
            monitor.print_summary(health_data)
            
            if args.save:
                monitor.save_to_file(health_data, args.output)
    
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

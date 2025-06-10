System Health Monitor - DevOps Python Project

Overview
This is a beginner-friendly Python project designed for DevOps engineers. It monitors system health metrics including CPU, memory, disk usage, network stats, and running processes. The tool can run once or continuously, with customizable alert thresholds.

Features
- System Information: Hostname, platform, uptime
- CPU Monitoring: Usage percentage, core count, frequency
- Memory Monitoring: RAM and swap usage
- Disk Monitoring: Usage for all mounted partitions
- Network Monitoring: Interface statistics
- Process Monitoring: Top CPU and memory consuming processes
- Alert System: Customizable thresholds for CPU, memory, and disk
- Data Export: Save results to JSON files
- Continuous Monitoring: Run at specified intervals

Requirements

Create a `requirements.txt` file:
```
psutil>=5.9.0
```

Installation

1. Clone or download the project files
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

Usage Examples

Basic Usage
```bash
# Run a single health check
python system_health_monitor.py

# Save results to JSON file
python system_health_monitor.py --save

# Save to specific file
python system_health_monitor.py --save --output my_health_check.json
```

Continuous Monitoring
```bash
# Monitor every 30 seconds (default)
python system_health_monitor.py --continuous

# Monitor every 60 seconds
python system_health_monitor.py --continuous --interval 60

# Continuous monitoring with file saving
python system_health_monitor.py --continuous --save --interval 120
```

Custom Alert Thresholds
```bash
# Set custom thresholds
python system_health_monitor.py --cpu-threshold 70 --memory-threshold 80 --disk-threshold 85

# Continuous monitoring with custom thresholds
python system_health_monitor.py --continuous --cpu-threshold 60 --memory-threshold 75
```

Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--save` | Save results to JSON file | False |
| `--output` | Specify output filename | Auto-generated |
| `--cpu-threshold` | CPU alert threshold (%) | 80 |
| `--memory-threshold` | Memory alert threshold (%) | 85 |
| `--disk-threshold` | Disk alert threshold (%) | 90 |
| `--continuous` | Run continuously | False |
| `--interval` | Monitoring interval (seconds) | 30 |

Sample Output

```
==================================================
SYSTEM HEALTH SUMMARY
==================================================
Timestamp: 2024-06-10 15:30:45

System: my-server (Linux)
Uptime: 48.5 hours

CPU Usage: 25.3%
CPU Cores: 8 logical, 4 physical

Memory Usage: 67.2%
Memory: 5.4 GB / 8.0 GB

Disk Usage:
  /: 45.2% (18.1 GB / 40.0 GB)
  /home: 78.9% (157.8 GB / 200.0 GB)

✅ No alerts - system is healthy!
==================================================
```

Learning Objectives

This project helps you learn:

1. Python Fundamentals:
   - Classes and methods
   - Exception handling
   - Command-line argument parsing
   - File I/O operations

2. System Programming:
   - Using the `psutil` library
   - Monitoring system resources
   - Working with system processes

3. DevOps Concepts:
   - System monitoring
   - Alert thresholds
   - Data collection and logging
   - Continuous monitoring

4. Best Practices:
   - Error handling
   - Code organization
   - Documentation
   - Command-line interfaces

Extending the Project

Here are some ideas to extend this project:

1. Add Email Alerts: Send email notifications when thresholds are exceeded
2. Web Dashboard: Create a simple web interface using Flask
3. Database Storage: Store metrics in SQLite or PostgreSQL
4. Grafana Integration: Export metrics to Grafana for visualization
5. Remote Monitoring: Monitor multiple servers
6. Docker Support: Containerize the application
7. Configuration Files: Use YAML/JSON config files
8. Log Analysis: Monitor log files for errors
9. Service Monitoring: Check if specific services are running
10. API Endpoints: Create REST API for metrics

Troubleshooting

Common Issues

1. Permission Errors: Some system metrics require elevated privileges
   - Solution: Run with `sudo` on Linux/macOS or as Administrator on Windows

2. psutil Import Error: 
   - Solution: Ensure psutil is installed: `pip install psutil`

3. JSON File Access: 
   - Solution: Ensure write permissions in the current directory

Platform-Specific Notes

- Windows: Some features like load average may not be available
- macOS: Requires Xcode command line tools for some psutil features
- Linux: Most features work out of the box

Contributing

This is a learning project! Feel free to:
- Add new monitoring features
- Improve error handling
- Add unit tests
- Enhance the documentation
- Create configuration templates

Next Steps

Once you're comfortable with this project, consider:
1. Learning about monitoring tools like Prometheus, Nagios, or Zabbix
2. Exploring infrastructure as code (Terraform, Ansible)
3. Container orchestration (Docker, Kubernetes)
4. CI/CD pipelines (Jenkins, GitLab CI, GitHub Actions)
5. Cloud platforms (AWS, Azure, GCP)

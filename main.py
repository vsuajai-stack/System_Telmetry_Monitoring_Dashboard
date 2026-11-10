import os
import sys
import argparse
import time
import psutil
from rich.panel import Panel
from rich.console import Console
from rich.live import Live
import sqlite3

console =Console(force_terminal=True)

def get_system_telemetry():
    memo = psutil.virtual_memory()
    ram_total = memo.total/(1024**2)
    ram_used = memo.used/(1024**2)

    cpu_load = psutil.cpu_percent()

    disk_usage = psutil.disk_usage('C:\\')
    disk_total = disk_usage.total/(1024**2)
    disk_used = disk_usage.used/(1024**2)

    return {"ram_total": ram_total,
            "ram_used": ram_used,
            "cpu_load": cpu_load,
            "disk_total": disk_total,
            "disk_used": disk_used}

def create_telemetry_panel(stats):
  return Panel.fit(
      f"[bold green]CPU Load     : {stats['cpu_load']}%[/bold green]\n"
      f"[bold blue]RAM Used     : {stats['ram_used']:.2f} MB /"
      f" {stats['ram_total']:.2f} MB[/bold blue]\n"
      f"[bold cyan]Disk Used    : {stats['disk_used']:.2f} MB /"
      f" {stats['disk_total']:.2f} MB[/bold cyan]",
      title="[bold yellow]System Telemetry Dashboard[/bold yellow]",
      border_style="white",
  )

def init_db():
    conn=sqlite3.connect('telemetry.db')
    cursor=conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_logs (id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        cpu_load REAL,
        ram_used REAL,
        disk_used REAL
        )
        """)
    conn.commit()
    conn.close()

def log_telemetry(stats):
    conn=sqlite3.connect('telemetry.db')
    cursor=conn.cursor()
    cursor.execute("""INSERT INTO system_logs (cpu_load, ram_used, disk_used) VALUES (?, ?, ?)""",
                   (stats['cpu_load'], stats['ram_used'], stats['disk_used']))
    conn.commit()
    conn.close()

def print_session_summary():
    conn=sqlite3.connect('telemetry.db')
    cursor=conn.cursor()
    cursor.execute("""SELECT COUNT(*),AVG(cpu_load),AVG(ram_used),AVG(disk_used),MAX(cpu_load),MAX(ram_used) FROM system_logs""")
    row=cursor.fetchone()
    conn.close()
    if row and row[0] > 0:
        count,Average_cpu,Average_ram,Average_disk,Max_cpu,Max_ram = row
        summary_panel = Panel.fit(f"  Average CPU Load    : [yellow]{Average_cpu:.3f} %[/yellow]\n"
                                  f"  Average RAM Used    : [yellow]{Average_ram:.3f} MB[/yellow]\n"
                                  f"  Average Disk Used   : [yellow]{Average_disk:.3f} MB[/yellow]\n"
                                  f"  Peak CPU Load       : [red]{Max_cpu:.3f} %[/red]\n"
                                  f"  Peak RAM Used       : [red]{Max_ram:.3f} MB[/red]",
                                  title="[bold yellow]System Telemetry Dashboard[/bold yellow]",
                                  border_style="white")
        console.print(summary_panel)

def main():
    parser = argparse.ArgumentParser(description="System Telemetry Dashboard")
    parser.add_argument("-i", "--interval", type=int, default=2, help="Polling interval in seconds")
    args = parser.parse_args()
    try:
        with Live(create_telemetry_panel(stats1),refresh_per_second=4,)as live_panel:
            while True:
                time.sleep(args.interval)
                stats=get_system_telemetry()
                live_panel.update(create_telemetry_panel(stats))
                log_telemetry(stats)
    except KeyboardInterrupt:
        console.print("[red]\n       Session Stopped[/red]")
        print_session_summary()


psutil.cpu_percent(interval=None)
time.sleep(0.5)
stats1 = get_system_telemetry()

if __name__ == "__main__":
    init_db()
    main()




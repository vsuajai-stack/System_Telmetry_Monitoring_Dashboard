# System Telemetry & Resource Monitor Dashboard #
## A simple Python script to monitor you resources #

This simple script uses python to monitor your ram, cpu and disk and shows you how much load you cpu is facing, how much ram is being used up in megabytes 
### Library used ###
- argparse
- psutil
- rich 
- sqlite3

### Function and their Purpose ###
1. get_system_telemtry()
   - Uses psutil to fetch current status of resources and return a list containing total ram and disk, used ram and disk and cpu load.
   
2. create_telemetry_panel()
    - Uses Panel.fit() from rich library to create a clean panel containing the stats passed to it by main().
3. init_db()
    - Connect\create telemetry.db and in telemetry.db create system_logs containing add timestamp,cpu_load, ram_used, disk_used column.
   
4. log_telemetry()
    - adds the stats to the system_logs table 
5. print_session_summary()
 - prints the summary of session when the main function is stopped. summary contains average and peak value of ram and cpu usage during session, average value of disk used.
6. main()
    -continuously update the panel displaying the stats,decides the frequency of checkup when called and call the print_session summary() function when interrupted 
#### How to Run ####
In terminal write Python main.py --interval 5

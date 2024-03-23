from datetime import datetime, timedelta
import time
import subprocess

for times in range(1) : 
    current_time = datetime.now()
    one_hour_later = current_time + timedelta(hours=1)
    one_hour_later = one_hour_later.replace(minute=0, second=0, microsecond=0)
    wait_time = (one_hour_later - current_time).total_seconds()+5
    print(f"等候 : {wait_time} 秒")
    # time.sleep(wait_time)
    print(datetime.now())
    powershell_command = r'python3.11 post_index_update.py >> bat_result.txt'
    subprocess.run(powershell_command, shell=True)
    powershell_command = r'python3.11 post_database_update.py >> bat_result.txt'
    subprocess.run(powershell_command, shell=True)

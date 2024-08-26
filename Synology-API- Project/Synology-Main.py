import datetime
import time

import synology_dsm as synology
import configparser
import logging
import pandas as pd

logger = logging.getLogger()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

config = configparser.ConfigParser()
config_file = config.read("synology-api-config.ini")

dsm = synology.SynologyDSM(
    config['authentication']['server_ip'],
    5001,
    config['authentication']['username'],
    config['authentication']['password'],
    use_https=True,
    verify_ssl=False,
)
stats_ditct = {}


def check_login():
    global date
    global timestamp
    global next_run
    date = datetime.date.today()
    timestamp = datetime.datetime.now()
    next_run = (timestamp + (datetime.timedelta(minutes=30))).strftime("%H:%M")
    if dsm.login():
        return True
    else:
        return False

def system_information():
    logger.info("Gathering System Information")
    dsm.information.update()
    model_inf = dsm.information.model
    dev_temp = dsm.information.temperature
    uptime = dsm.information.uptime
    logger.info(f"System: {model_inf}")
    logger.info(f"Temerature: {dev_temp} C")
    logger.info(f"Uptime: {uptime} seconds")
    stats_ditct['Device Temperature'] = [dev_temp]
    stats_ditct['Uptime'] = [uptime]
    return dev_temp, uptime

def system_utilization():
    logger.info("Gathering Utilization Information")
    dsm.utilisation.update()
    cpu_load = dsm.utilisation.cpu_total_load
    ram_use = dsm.utilisation.memory_real_usage
    logger.info(f"CPU Total Load: {cpu_load}%")
    logger.info(f"RAM Usage: {ram_use}%")
    stats_ditct['CPU Load'] = [cpu_load]
    stats_ditct['RAM Usage'] = [ram_use]
    return cpu_load, ram_use

def storage_usage():
    dsm.storage.update()
    for volume in dsm.storage.volumes_ids:
        vol_stat = dsm.storage.volume_status(volume)
        vol_perc = dsm.storage.volume_percentage_used(volume)
        logger.info(f"Volume ID: {volume}")
        logger.info(f"Status: {vol_stat}")
        logger.info(f"Used: {vol_perc}%")
    stats_ditct[f'Status-{volume}'] = [f'{vol_stat}']
    stats_ditct[f'Percentage-{volume}'] = [f'{vol_perc}']
    return volume, vol_stat, vol_perc


def disk_info():
    logger.info("Gathering Disk Information")
    disk_dict = {}
    for disk in dsm.storage.disks_ids:
        disk_id = dsm.storage.disk_name(disk)
        disk_status = dsm.storage.disk_status(disk)
        disk_smart = dsm.storage.disk_smart_status(disk)
        disk_temp = dsm.storage.disk_temp(disk)
        logger.info(f"Disk ID: {disk_id}")
        logger.info(f"Disk Status: {disk_status}")
        logger.info(f"Disk SMART Status: {disk_smart}")
        logger.info(f"Disk Temp: {disk_temp}")
        disk_dict.update({disk: (disk_id,disk_status,disk_smart,disk_temp)})
        stats_ditct[f'Disk-Status-{disk_id}'] = [f"{disk_status}"]
        stats_ditct[f'Disk-Smart-Status-{disk_id}'] = [f"{disk_smart}"]
        stats_ditct[f'Disk Temperature-{disk_id}'] = [disk_temp]
    return disk_dict

def upgrade_check():
    logger.info("Checking for DSM Updates")
    dms_upgrade = dsm.upgrade
    dms_upgrade.update()
    upgrade = dms_upgrade.update_available
    if dms_upgrade.update_available:
        logger.warning(f"Update Available\nPlease Upgrade DSM Version to {dms_upgrade.available_version}")
        logger.warning(f"Upgrade available: {upgrade}")
        return upgrade
    else:
        logger.info("No Updates Available at this time.")
        logger.info(f"Upgrade available: {upgrade}")
        return upgrade

def available_api():
    for apis in dsm.apis:
        print(f"Available APIs are: {apis}")

def run_tasks():
    if check_login():
        logger.info("Starting Task")
        logger.info(f"Timestamp: {timestamp}")
        logger.info("Logged In")
        sys_inf = system_information()
        sys_util = system_utilization()
        vol = storage_usage()
        disk = disk_info()
        upgrade = upgrade_check()
        stats_ditct['Timestamp'] = [timestamp]
        stats_to_df(stats_ditct)
        #available_api()
    else:
        logger.error("Error with Login credentials")

def stats_to_df(dict):
    df = pd.DataFrame().from_dict(dict, orient='columns')
    try:
        df.to_csv("Synology-data.csv", index=False, mode='a', header=False)
    except Exception as e:
        logger.error(f'Error with CSV: {e}')
    logger.info("Synology CSV Data Updated")

if __name__ == "__main__":
    while True:
        run_tasks()
        if dsm.logout():
            logger.info("Logged Out")
            logger.info(f"Next run in 30 minutes at {next_run}")
            time.sleep(1800)
        else:
            break

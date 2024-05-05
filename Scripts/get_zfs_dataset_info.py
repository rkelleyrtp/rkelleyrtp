#!/usr/bin/python3

# ===============================================================================
# Python script to get ZFS details from zpools and datasets.  @RKelleyRTP
# This script requires the colorama plugin
#
# Usage:
# --------
# <command>        will display pool information for all datasets
# <command> <pool> will display pool information for a specific dataset
# ===============================================================================

import os
import re
import sys
from colorama import Fore
ZPOOL="/usr/sbin/zpool"
ZFS="/usr/sbin/zfs"
LOCAL_ZFS_POOL="127.0.0.1"

# =================================================================================
# Get a selection of ZFS dataset objects
# Note: the order of this variable determins the output order.  Adjust as needed.
# =================================================================================
ZFS_FIELDS="mountpoint,logicalused,usedbydataset,compressratio,compression,available,recordsize,primarycache,secondarycache,atime,relatime,xattr,logbias,refreservation,quota"


# ======================================================
# Get list of local data sets 
# ======================================================
local_zfs_dataset_list=[]
loc_command = os.popen(f"{ZFS} get -t filesystem -o all -H {ZFS_FIELDS} | egrep -v '@'")
localdataset = loc_command.readlines()
for item in localdataset:
    local_zfs_dataset_list.append(item.split()[0])
unique_localdataset=set(local_zfs_dataset_list)
unique_localdataset=set([i.split()[0] for i in localdataset])

localdataset_dict = { (x[0], x[1]): [x[2], x[3]] for x in [ i.split() for i in localdataset ]}

# ==============================================================
# Cycle through the dataset and ZFS_FIELDS.
# ==============================================================
def display_data(dataset):
    print(Fore.WHITE)
    print()
    print(f"ZFS Volume: {dataset}")
    print("===========================================================")
    print("   Attribute                Value                          ")
    print("===========================================================")
    for field in ZFS_FIELDS.split(","):
        field_string=field + ":"
        loc_entry=localdataset_dict[(dataset, field)]
    # ===========================================
    # Write some output
    # ===========================================
        if "refreservation" in field_string: field_string="Reservation"
        elif "quota" in field_string: field_string="Quota"
        elif "mountpoin" in field_string: field_string="Mount Point"
        elif "logicalused" in field_string: field_string="Logical space used"
        elif "usedbydataset" in field_string: field_string="Real space used"
        elif "compressratio" in field_string: field_string="Compression Ratio"
        elif "compression" in field_string: field_string="Compression Type"
        elif "recordsize" in field_string: field_string="Record Size"
        elif "primarycache" in field_string: field_string="Primary Cache type"
        elif "secondarycache" in field_string: field_string="Secondary Cache type"
        elif "logbias" in field_string: field_string="Log Bias"
        elif "available" in field_string: field_string="Dataset Space Available"
        field_string="   {0:<25}".format(field_string)
        print(Fore.GREEN  + f"{field_string}",end="")
        print(Fore.YELLOW + loc_entry[0],"\t\t")
    print()
# ----------------------------------------------------------------
# End of function
# ----------------------------------------------------------------


# ========================================================
# Main here
# ========================================================
arguments=len(sys.argv) - 1

if arguments == 0:
    # --------------------------------------------
    # No arguments passed - listing all datasets
    # --------------------------------------------
    for line in sorted(unique_localdataset):
        display_data(line)

else:
    # --------------------------------------------
    # Cycle through the arguments and try to match
    # a dataset with an argument using wildcards
    # --------------------------------------------
    position=1
    while (arguments >= position):
        arg=[sys.argv[position]]
        if not any(arg[0] in word for word in unique_localdataset):
            print(f"No matching dataset for: {arg[0]}")

        else:
            matches = [match for match in unique_localdataset if str(arg[0]) in match]
            for line in sorted(matches):
                display_data(line)
        position += 1


# ================================
# Reset the console colors
# ================================
print(Fore.RESET, end="")

sys.exit()

# ========================
# End of Script
# ========================
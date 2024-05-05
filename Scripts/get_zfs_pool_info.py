#!/usr/bin/python3

# ===============================================================================
# Python script to get ZFS pool details.  @RKelleyRTP
# This script requires the colorama plugin
#
# Usage:
# --------
# <command>        will display pool information for all pools
# <command> <pool> will display pool information for a specific pool
# ===============================================================================

import os
import re
import sys
from colorama import Fore
ZPOOL="/usr/sbin/zpool"
ZFS="/usr/sbin/zfs"


# ====================================================================================
# Select our fields to display
# Note: The order of this variable affects the display order.  Adjust accordingly.
# ====================================================================================
ZPOOL_FIELDS="size,allocated,free,capacity,fragmentation,ashift,health,autoexpand,autoreplace,autotrim,readonly"


# ======================================================
# Get list of pools
# ======================================================
tmp_zpool_list=os.popen(f"{ZPOOL} list -H | cut -f1")
zpool_list=set([i.split()[0] for i in tmp_zpool_list])

# ==============================================================
# Cycle through the dataset and ZFS_FIELDS.
# ==============================================================
def display_data(pool):
    pool.rstrip()

    local_zpool_list_details=[]

    local_command = os.popen(f"{ZPOOL} get -o all -H {ZPOOL_FIELDS} {pool} ")
    local_zpool_details = local_command.readlines()

    for item in local_zpool_details:
        local_zpool_list_details.append(item.split()[0])

    local_zpool_dict = { (x[0], x[1]): [x[2], x[3]] for x in [ i.split() for i in local_zpool_details ]}
    print(Fore.WHITE)
    print()

    print(f"ZPool: {pool}")
    print("===========================================================")
    print("   Attribute                Value                          ")
    print("===========================================================")
    for field in ZPOOL_FIELDS.split(","):
        field_string=field + ":"
        loc_entry=local_zpool_dict[(pool, field)]
    # ===========================================
    # Write some output
    # ===========================================
        if "size" in field_string: field_string="Total Pool Size"
        elif "allocated" in field_string: field_string="Space Allocated"
        elif "free" in field_string: field_string="Space Free"
        elif "capacity" in field_string: field_string="Capacity In Use"
        elif "fragmentation" in field_string: field_string="Fragmentation"
        elif "ashift" in field_string: field_string="ashift"
        elif "health" in field_string: field_string="health"
        elif "autoexpand" in field_string: field_string="autoexpand"
        elif "autoreplace" in field_string: field_string="autoreplace"
        elif "autotrim" in field_string: field_string="autotrim"
        elif "readonly" in field_string: field_string="readonly"
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
    for line in sorted(zpool_list):
        display_data(line)

else:
    # --------------------------------------------
    # Cycle through the arguments and try to match
    # a dataset with an argument using wildcards
    # --------------------------------------------
    position=1
    while (arguments >= position):
        arg=[sys.argv[position]]
        if not any(arg[0] in word for word in zpool_list):
            print(f"No matching dataset for: {arg[0]}")

        else:
            matches = [match for match in zpool_list if str(arg[0]) in match]
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
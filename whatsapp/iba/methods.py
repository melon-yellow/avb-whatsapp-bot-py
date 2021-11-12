
##########################################################################################################################

import datetime

##########################################################################################################################

# Get Timestamp from IBA
def timestamp(time: list[int]):
    date = datetime.datetime(
        microsecond=(time[0]*1000),
        second=time[1],
        minute=time[2],
        hour=time[3],
        day=time[4],
        month=time[5],
        year=time[6]
    )
    return date

##########################################################################################################################


##########################################################################################################################

from py_wapp import Bot
from . import status

##########################################################################################################################

# Check Cim-IO Status
def cimios(bot: Bot):

    # Update Timestamps
    status.update()

    # Check Values
    afs = status.nok('AFS')
    bof = status.nok('BOF')
    lcfp = status.nok('LCFP')

    # Check if Has Trigger
    cafs = afs and not status.fault['AFS']
    cbof = bof and not status.fault['BOF']
    clcfp = lcfp and not status.fault['LCFP']

    # Should Send Message
    should_send = cafs or cbof or clcfp

    # Assign Fault to History
    status.fault['AFS'] = afs
    status.fault['BOF'] = bof
    status.fault['LCFP'] = lcfp

    # If Should Send Message
    if should_send:
        # message
        msg = '*Atenção!* ⚠️ '
        # Check All
        if afs and bof and lcfp:
            msg += 'O PIMS está com problemas!'
        else:
            # Temp Array
            tar = []
            if afs: tar.append('do AF')
            if bof: tar.append('do LD')
            if lcfp: tar.append('do LC')

            # Get Length of Temp Array
            cnt = len(tar)

            # Temp Text
            txt = ''
            for i in range(cnt):
                txt += tar[i]
                if i < (cnt - 2): txt += ', '
                if i == (cnt - 2): txt += ' e '
            
            # Check For More Than One Issue
            if cnt == 1: msg += 'O Cim-IO {} está com problemas!'.format(txt)
            else: msg += 'Os Cim-IOs {} estão com problemas!'.format(txt)

        # Send Message
        bot.send('anthony', msg, 'py_mes_not_working')
        bot.send('antonio_carlos', msg, 'py_mes_not_working')
        # Conditional Contacts 
        if cafs: bot.send('wesley', msg, 'py_mes_not_working')
        if cbof or clcfp: bot.send('wanderson', msg, 'py_mes_not_working')
        
##########################################################################################################################

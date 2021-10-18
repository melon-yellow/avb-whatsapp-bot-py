##########################################################################################################################
#                                                   ONE MINUTE SCHEDULE                                                  #
##########################################################################################################################

def py_mes_check_cimios():
    # Update Timestamps
    pyMesCheck.update()

    # Check Values
    afs = pyMesCheck.nok('AFS')
    bof = pyMesCheck.nok('BOF')
    lcfp = pyMesCheck.nok('LCFP')

    # Check if Has Trigger
    cafs = afs and not pyMesCheck.fault['AFS']
    cbof = bof and not pyMesCheck.fault['BOF']
    clcfp = lcfp and not pyMesCheck.fault['LCFP']

    # Should Send Message
    should_send = cafs or cbof or clcfp

    # Assign Fault to History
    pyMesCheck.fault['AFS'] = afs
    pyMesCheck.fault['BOF'] = bof
    pyMesCheck.fault['LCFP'] = lcfp

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
        Avbot.bot.send('anthony', msg, 'py_mes_not_working')
        Avbot.bot.send('antonio_carlos', msg, 'py_mes_not_working')
        # Conditional Contacts 
        if cafs: Avbot.bot.send('wesley', msg, 'py_mes_not_working')
        if cbof or clcfp: Avbot.bot.send('wanderson', msg, 'py_mes_not_working')
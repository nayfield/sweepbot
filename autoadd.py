import sheets_test

# get sheetid, inrange, outrange, outfields
exec(open('config/sheetconfig.py').read())

def hdr_idx(hdr,fields):
    '''Take header (list) and field names (list) and return list of positions'''
    retval = {}
    for i in range(len(hdr)):
        for f in fields:
            if hdr[i] == f:
                retval[f] = i
    return retval

def spec_cols(tab, outidx):
    ''' take a table and return samme but only those fields'''
    retval = []
    for inrow in tab:
        outrow = []
        for x in outidx:
            if x >= len(inrow):
                outrow.append('')
            else:
                outrow.append(inrow[x])
        retval.append(outrow)
    return retval

def field_match(table, field, match):
    retval = []
    for r in table:
        if r[field] == match:
            retval.append(r)
    return retval

def print_stat(sname, scount):
    print('Step: {:30} Count:{:5d}'.format(sname, scount))


if __name__ == '__main__':
    # Get our input table (pop extra header row)
    intable = sheets_test.get_sheet_range(sheetid, inrange)
    intable.pop(0)
    inhdr = hdr_idx(intable[0], outfields)
    # don't pop real header

    # Make newtable with just the cols we want
    newtableraw = spec_cols(intable, inhdr.values())
    newhdr = hdr_idx(newtableraw[0], outfields)
    newtableraw.pop(0)

    print_stat('Input table', len(newtableraw))
    newtablechk = field_match(newtableraw, newhdr['AUTOADD'], 'TRUE')
    print_stat('Removing unchecked', len(newtablechk))

    outtable = sheets_test.get_sheet_range(sheetid, outrange)
    outtable.pop(0)
    outtable.pop(0)
    print_stat('Output table', len(outtable))
    havelist = []
    for r in outtable:
        havelist.append(r[0])

    uplist = []
    for r in newtablechk:
        if r[0] != '' and r[1] != '':
            if r[0] not in havelist:
                uplist.append(r)
    print_stat('Upload table', len(uplist))

    if uplist:
        cels = sheets_test.append_rows(sheetid, outrange, uplist)
    else:
        print('No upload.')




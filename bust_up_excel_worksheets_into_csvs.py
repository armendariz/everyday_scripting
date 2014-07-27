#!/usr/bin/env python


def excel_to_csv(excel_file, sheet_number):
    import xlrd
    book = xlrd.open_workbook(excel_file)
    sh = book.sheet_by_index(sheet_number)
    records = []
    for i in range(sh.nrows):
        elements = []
        for r in sh.row(i):
            if r.ctype == 3:
                # if ctype == 3, then it's a date. so use: xldate_as_tuple(xldate, datemode)
                date_pieces = xlrd.xldate_as_tuple(r.value, book.datemode)
                date = '%s-%s-%s' % (date_pieces[0], date_pieces[1], date_pieces[2])
                elements.append(date.encode("utf-8"))
            else:
                try:
                    e = '%s' % r.value.strip()
                except:
                    e = '%s' % r.value
                elements.append(e.encode("utf-8"))
        #print '|'.join(elements)
        records.append('|'.join(elements))
    #return '\n'.join(records)
    return records
    

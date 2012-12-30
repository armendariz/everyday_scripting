#!/usr/bin/env python
import requests # great library for doing stuff on the web
import os, fnmatch
import re

def all_files(root, patterns='*', single_level=False, yield_folders=False):
    # Taken from the O'Reilly Python Cookbook
    # Expand patterns form semicolon-separated string to list
    # example usage: thefiles = list(all_files('/tmp', '*.py;*.htm;*.html'))
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path, name)
                    break
        if single_level:
            break

def set_up():
    '''
    filings_dict is a dictionary. a python dictionary is made up of key/value pairs and is a very powerful way to store data.
    kp_public_affairs is a key in the filingd_dict dictionary and it's associated value is a list of links.
    i'll use the .items() method of the dictionary to loop through the key/value pairs to create a directory structure to download the PDF disclosure reports into
    '''
    filings_dict = {
        'kp_public_affairs': [
            'http://cal-access.ss.ca.gov/PDFGen/pdfgen.prg?filingid=1707953&amendid=0',
            'http://cal-access.ss.ca.gov/PDFGen/pdfgen.prg?filingid=1678917&amendid=0',
            'http://cal-access.ss.ca.gov/PDFGen/pdfgen.prg?filingid=1657226&amendid=0',
            'http://cal-access.ss.ca.gov/PDFGen/pdfgen.prg?filingid=1637112&amendid=0',
            'http://cal-access.ss.ca.gov/PDFGen/pdfgen.prg?filingid=1620449&amendid=0',
        ],
        'nielsen': [
            'http://cal-access.ss.ca.gov/PDFGen/pdfgen.prg?filingid=1708226&amendid=0',
            'http://cal-access.ss.ca.gov/PDFGen/pdfgen.prg?filingid=1678882&amendid=1',
            'http://cal-access.ss.ca.gov/PDFGen/pdfgen.prg?filingid=1656554&amendid=0',
            'http://cal-access.ss.ca.gov/PDFGen/pdfgen.prg?filingid=1636552&amendid=0',
        ],
        'lang': [
            'http://cal-access.ss.ca.gov/PDFGen/pdfgen.prg?filingid=1709975&amendid=0',
            'http://cal-access.ss.ca.gov/PDFGen/pdfgen.prg?filingid=1679100&amendid=1',
            'http://cal-access.ss.ca.gov/PDFGen/pdfgen.prg?filingid=1657179&amendid=1',
            'http://cal-access.ss.ca.gov/PDFGen/pdfgen.prg?filingid=1633568&amendid=0',
        ],
    }
    
    main_dir_name = 'lobbying_reports'
    if os.path.isdir(main_dir_name): # test to see if the folder exists
        try:
            cmd = 'rm -rf %s' % main_dir_name # try deleteing the folder the nix way
            os.system(cmd)
        except:
            cmd = 'rmdir /S %s' % main_dir_name # if the above fails try the Windows command line way. If both fail, the script fails
            os.system(cmd)
    
    os.mkdir(main_dir_name) # create or re-create the main directory
    for lobbyist,link_list in filings_dict.items(): # loop through the filings dict contents, assigning the key to the variable lobbyist and the value to the variable file_list
        lobbyist_folder_path = os.path.join(main_dir_name, lobbyist) # establish where the lobbying reports for this lobbyist will live
        os.mkdir(lobbyist_folder_path) # now create that folder
        i = 1 # get a counter variable ready to roll. i'm just gonna name the report like so: lobbyist_name_1, lobbyist_name_2, etc
        for link in link_list: # loop through the report links for this lobbyist
            
            remote_file_request = requests.post(link) # request the PDF from the server
            remote_file_content = remote_file_request.content # store the contents of the PDF file
            
            local_file_name = '%s_%s.pdf' % (lobbyist, i) # create a local file name to use
            outfile_path = os.path.join(lobbyist_folder_path, local_file_name) # establish the path to where that file will live
            outfile = open(outfile_path, 'wb') # open a file handle to write to
            outfile.write(remote_file_content) # write the contents of the file out to the file
            outfile.close() # close the file
            
            i += 1 # increase the report count by one

def textify():
    file_list = list(all_files('lobbying_reports', '*.pdf')) # use the all_files function to find all the pdf files and use the python list function to make it an actual list
    for file in file_list:
        cmd = 'pdftotext -layout %s' % file
        os.system(cmd)

def list_files(type):
    file_list = list(all_files('lobbying_reports', '*.%s' % type))
    return file_list

def look_for_bills_lobbied():
    # this is just an example of how you could troll through a directory of files looking for stuff
    # my 30 second solution to finding the bills could definitley be improved
    text_files = list_files('txt')
    for file in text_files:
        infile = open(file)
        lobbyist = file.split('/')[1]
        keep_going = False
        for line in infile:
            if keep_going == False:
                if re.search(r'Schedule\W+F625', line.strip()):
                    print '%s\t%s' % (lobbyist, line.strip())
                    keep_going = True
            elif keep_going == True:
                print line
            elif line == '\n':
                keep_going = False
            else:
                print '%s\t%s' % (lobbyist, line.strip())
        infile.close()

def do_it_do_it():
    try:
        set_up()
        print 'set up the directories and downloaded all the disclosure reports'
    except:
        print 'failed while trying to set_up'
    try:
        textify()
        print 'ripped the text out of the PDF files'
    except:
        print 'failed while trying to get the text out of the PDFs'
    
    print 'SEARCHING FOR BILLS LOBBIED\n\n'
    
    try:
        look_for_bills_lobbied()
    except:
        print 'failed while trying to find bills lobbied'

if __name__ == '__main__':
    do_it_do_it()
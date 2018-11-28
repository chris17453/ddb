import json
import os
from colors import *

def format_string(data,length,fill_character=' ',no_clip=False):
    if None == data:
        data=''
    data=data.replace('\t','       ')
    if False==no_clip:
        return data[:length-2].ljust(length-2,fill_character)
    else:
        return data.ljust(length-2,fill_character)

def format_data(format='term',width=10,no_clip=False,table=None):
    try:
        if None == table:
            raise Exception("No table to display")
        # defaults
        if None == format:
            format='term'
        if None == width:
            width='auto'
        if None == no_clip:
            no_clip=False

        if format=='json':
            print(json.dumps(table.results))
    
        if format=='term':
            tty_min_column_width=10
            tty_rows, tty_columns = os.popen('stty size', 'r').read().split()
            data_column_count=len(table.columns)
            # no columns to return
            if data_column_count==0:
                return ""
        
            if width=='auto':
                width_per_column=int(tty_columns)/data_column_count
                if width_per_column<tty_min_column_width:
                    width_per_column=tty_min_column_width
            else:
                width_per_column=int(width)
            total_width=width_per_column*data_column_count-1*data_column_count+1
            # header
            header=""
            header="{0}|{1}".format(bcolors.OKBLUE,bcolors.ENDC)
            for c in table.columns:
                if len(c.data.name)>width_per_column-2:
                    wall_color=bcolors.WARNING
                else:
                    wall_color=bcolors.OKBLUE
                if None == c.display.name:
                    display=c.data.name
                else:
                    display=c.display.name
                    
                header+="{3}{4}{0}{2}{1}|{2}".format(
                        format_string(display,width_per_column,' ',no_clip), #0
                        wall_color, #1
                        bcolors.ENDC, #2
                        bcolors.HEADER,#3
                        bcolors.UNDERLINE) #4
            print(header)
            index=0
            for line in table.results:
                columns="{0}|{1}".format(bcolors.OKBLUE,bcolors.ENDC)
                data_type='data'
                if len(line) == 1:
                    if not line[0]:
                        data_type='whitespace'
                    else:
                        if line[0][0] in table.delimiters.comment:
                            data_type='comment'
                
                if 'data' == data_type:
                    for c in line:
                        #print c
                        if len(c)>width_per_column-2:
                            wall_color=bcolors.WARNING
                        else:
                            wall_color=bcolors.OKBLUE
                        columns+="{0}{1}|{2}".format(format_string(c,width_per_column,no_clip=no_clip),wall_color,bcolors.ENDC)
                    if len(line) < data_column_count:
                        wall_color=bcolors.OKBLUE
                        for c in range(len(line),data_column_count):
                            columns+="{0}{1}|{2}".format(format_string("",width_per_column,no_clip=no_clip),wall_color,bcolors.ENDC)

                if 'comment' == data_type or 'whitespace' == data_type:
                    columns="{1}|{2}{0}{1}|{2}".format(format_string(line[0],total_width,no_clip=no_clip),wall_color,bcolors.OKGREEN)
                    

                print(columns)
                index+=1
                if index== int(tty_rows)-5:
                    index=0
                    print (header)
            print (header)
            print ("Error Count: {0}. Results: {1}".format(table.error_count,table.results_length()) )

    except Exception as ex:
        print "Formatting error: {}".format(ex)

def print_errors(table):
    for e in table.errors:
        print(e)
import sys
import select
import os
import tempfile
import curses

from .style import style
from .colors import *
from .config import table_config



class table:


    data_type=enum(COMMENT=1,ERROR=2,DATA=3,WHITESPACE=4)
    
        
    def __init__(self,args=None,data=None,single=True):
        self.style=style(single)
        self.data=data
        self.config=table_config()


        if None !=args:
            if args.column_width==-1:
                try:
                    self.stdscr = curses.initscr()
                    curses.cbreak()
                    curses.noecho()
                    self.stdscr.keypad(1)
                    self.config.row_height,self.config.column_width = self.stdscr.getmaxyx()
                finally:
                    curses.nocbreak()
                    self.stdscr.keypad(0)
                    curses.echo()
                    curses.endwin()
            else:
                self.config.row_height=args.row_height
                self.config.column_width=args.column_width

            self.args=args
            self.config.output=args.output
            self.config.no_color=args.no_color
            self.config.remove_quote=args.remove_quote
            self.config.block_quote==args.block_quote
                    
            self.config.header_on_line=args.header_on_line
            self.config.data_on_line=args.data_on_line
            self.config.hide_comments=args.hide_comments
            self.config.hide_errors=args.hide_errors
            self.config.hide_whitespace=args.hide_whitespace
            self.config.no_clip=False
            self.config.delimiters['field']=args.delimiter
            self.config.header=args.header
            self.config.footer=args.footer
            self.config.header_every=args.header_every
            self.config.file=args.file
            #auto name columns
            if args.column_count>-1:
                self.config.column_count=args.column_count
                self.config.columns=[]
                for n in range(0,self.config.column_count):
                    self.config.columns.append("column{}".format(n+1))

            # when specifically setting columns up... iverrides auto naming columns
            if None != args.columns:
                self.config.set_columns(args.columns)
            
            
            if args.page>-1 and args.length>1:
                self.config.starts_on=args.page*args.length+1
            if self.args.line>-1:
                self.config.starts_on=args.line
            self.config.length=args.length

        else:
            self.args=None

        self.config.is_temp_file=False
        self.results=[]

        if self.config.no_color is True or self.config.output !='ASCII':
            self.config.render_color=False

        self.format()


    def process_line(self,line,line_number=0):
        err=None
        line_data=None
        line=line.rstrip('\r\n')
        if self.config.data_on_line>line_number:
            line_type=self.config.data_type.COMMENT
            line_data=[line]
        else:
            line_type=self.data_type.DATA
            if True == line.isspace():
                line_type=self.data_type.WHITESPACE
                line_data=[line]
            else:
                if line[0] is self.config.delimiters['comment']:
                    line_data=[line]
                    line_type=self.data_type.COMMENT
        
        return {'data':line_data,'type':line_type,'error':err}


    def process_data(self,line,line_number):
        err=None
        line=line.strip()
        # ok its data. lets split it up and check for errors
        line_data=line.split(self.config.delimiters['field'])
        line_column_count=len(line_data)
        column_count=self.config.column_count

        # mark the row as an error and create a message if column counts are invalid, if there are column counts
        if None !=column_count:
            if line_column_count!=column_count:
                column_diff=column_count-line_column_count
                if column_diff>0:
                    err="Line #{0}, {1} extra Column(s)".format(line_number,column_diff)
                else:
                    err="Line #{0}, missing {1} Column(s)".format(line_number,column_diff*-1)
                
                line_type=self.data_type.ERROR
        # strip delimiters from field if block quoted (xlsx export to csv?)
        # if none just add the field
        if True == self.config.remove_quote:
            line_data_cleaned=[]
            for d in line_data:
                strip=False
                # block quote check, field must be > than 1 character
                if len(d)>1:
                    if d[0]=='"' and d[-1]=='"':
                        strip=True
                    else:
                        if d[0]=='\'' and d[-1]=='\'':
                            strip=True
                        else:
                            if None != self.config.block_quote:
                                if d[0]==self.config.block_quote and d[-1]==self.config.block_quote:
                                    strip=True

                if True==strip:
                    line_data_cleaned.append(d[1:-1])
                else:
                    line_data_cleaned.append(d)
            #swap ouyt the cleaned up row
            line_data=line_data_cleaned
        
        # update type if errored
        if None !=err:
            line_type=self.data_type.ERROR
        else:
            line_type=self.data_type.DATA

        return {'data':line_data,'type':line_type,'error':err}

    # loop through al lines in the stream and process
    def process_file(self):
        # offset dont get confused
        line_number=0
        visible_line=1
        buffer_length=0
        buffer=[]
        #print self.starts_on,self.length
        #exit(1)
        with open(self.config.file) as stream:
            for line in stream:
                line_number+=1

                # if columns are defined in the header, pull those
                if self.config.header_on_line==line_number:
                    results=self.process_line(line,line_number)
                    self.config.columns=results['data']
                    self.config.column_count=len(self.columns)
             
                #print self.starts_on,line_number
                # below visible window.. skip
                if  self.config.starts_on>line_number:
                    continue

                results=self.process_line(line,line_number)
                    
                #print line_number,results['type']
                # skip comments if asked to
                if results['type']==self.data_type.COMMENT and True == self.config.hide_comments: 
                    continue
                
                # skip errors if asked to
                if results['type']==self.data_type.ERROR and True == self.config.hide_errors: 
                    continue

                # skip errors if asked to
                if results['type']==self.data_type.WHITESPACE and True == self.config.hide_whitespace: 
                    continue

                #print -1 == self.length , self.starts_on<=line_number-1,line_number,self.starts_on
                if results['type']==self.data_type.DATA: 
                    # only process visible data. saves a lot of string manipulation
                    results=self.process_data(line,line_number)
                    # skip errors if asked to
                    if results['type']==self.data_type.ERROR and True == self.config.hide_errors: 
                        continue
                

                # ok everything reaching here is wanted and visible
                buffer_length+=1
                visible_line+=1
                
                # if we are past our collection point... jet, lets not waste time here
                if -1 !=self.config.length and buffer_length>self.config.length:
                    break

                #print line_number-1,self.starts_on,self.length
               
                #results['visible_line_number']=visible_line
                results['file_line_number']=line_number
                # only include raw it there is an error
                if results['error']!=None:
                    results['raw']=line

                buffer.append(results)


        return buffer
    
    
    def calculate_limits(self):
        tty_min_column_width=1
        # doesnt work with pipes. ugh
        # tty_rows, tty_columns = os.popen('stty size', 'r').read().split()
        # tty_rows=int(tty_rows)
        # tty_columns=int(tty_columns)
        # dev size
        # tty_rows=30
        # tty_columns=80

        
        data_column_count=self.config.column_count
        pad=data_column_count+1
        # no columns to return
        if data_column_count==0:
            self.config.column_character_width=-1
        else:
            if self.config.column_width!=-1:
                self.config.column_character_width=int(int(self.config.column_width-1-pad)/data_column_count)
                if self.config.column_character_width<tty_min_column_width:
                    self.config.column_character_width=tty_min_column_width
            #@else:
            #    print(self.config.column_width)
            #    self.config.column_character_width=int(self.config.width)


        self.config.total_width=self.config.column_character_width*data_column_count+data_column_count-1


    def build_header(self,footer=False,mid=False):
        # header

        if False==footer:
            base=self.style.characters.top
            column=self.style.characters.header
        else:
                base=self.style.characters.bottom
                column=self.style.characters.footer
        if mid==True:
                base=self.style.characters.center
                column=self.style.characters.mid_header
        header=base.left.render(use_color=self.config.render_color)

        column_pad=0
        if None!=column.left.text:
            column_pad+=1
        if None!=column.right.text:
            column_pad+=1

        if None != self.config.columns:
            index=0
            for c in self.config.columns:
                column_display=u''
                if None!=column.left.text:
                    column_display=column.left.render(use_color=self.config.render_color)

                column_display+=column.center.render(use_color=self.config.render_color,text=c,length=self.config.column_character_width-column_pad)
                #print self.column_character_width-column_pad

                if None!=column.right.text:
                    column_display+=column.right.render(use_color=self.config.render_color)
                

                header+=column_display

                # if we have overflow, change the column wall ont he right
                if index<len(self.config.columns)-1:
                    if len('{}'.format(c))>self.config.column_character_width-2:
                        header+=base.center.render(use_color=self.config.render_color,override=self.style.color.overflow)
                    else:
                        header+=base.center.render(use_color=self.config.render_color)
                index+=1
        header+=base.right.render(use_color=self.config.render_color)
        header+=u'{}'.format(reset.ALL)


        return header
            
    def build_rows(self,buffer):
        rows=[]
        index=0
        if True == isinstance(buffer,list):
            for line in buffer:
                columns=self.style.characters.walls.left.render(use_color=self.config.render_color)
                #print line
                
                if self.data_type.DATA == line['type']:
                    for c in line['data']:
                        columns+=self.style.color.data.render(c,use_color=self.config.render_color,length=self.config.column_character_width)
                        # if we have overflow, change the column wall on the right
                        if len('{}'.format(c))>self.config.column_character_width:
                            columns+=self.style.characters.walls.right.render(use_color=self.config.render_color,override=self.style.color.overflow)
                        else:
                            columns+=self.style.characters.walls.right.render(use_color=self.config.render_color)
                        
                    #only happend if we allow errored rows            
                    if len(line['data']) < self.config.column_count:
                        wall_color=bcolors.OKBLUE
                        for c in range(len(line['data']),self.config.column_count):
                            columns+=self.style.color.comment.render('',use_color=self.config.render_color,length=self.config.column_character_width)
                            columns+=self.style.characters.walls.right.render(use_color=self.config.render_color,override=self.style.color.error)
                            
                
                
                if self.data_type.COMMENT ==  line['type'] or self.data_type.WHITESPACE==line['type']:
                    left  =self.style.characters.walls.left.render(use_color=self.config.render_color)
                    center=self.style.color.comment.render(line['raw'],use_color=self.config.render_color,length=self.config.total_width)
                    right =self.style.characters.walls.right.render(use_color=self.config.render_color)
                    columns=u"{0}{1}{2}".format( left,
                                                center,
                                                right)
                
                if self.data_type.ERROR ==  line['type']:
                    left  =self.style.characters.walls.left.render(use_color=self.config.render_color)
                    center=self.style.color.error.render(line['raw'],use_color=self.config.render_color,length=self.config.total_width)
                    right =self.style.characters.walls.right.render(use_color=self.config.render_color)
                    columns=u"{0}{1}{2}".format( left,
                                                center,
                                                right)
                columns+=u'{}'.format(reset.ALL)

                rows.append(columns)
                index+=1
                #if index== int(tty_rows)-5:
                #    index=0
                #    rows.append(self.)
        else:
            raise Exception ("data is invalid: ->".format(buffer))

        return rows


                        
    # with no columns, everything will be run on, not well formated
    def format(self):

        #here we either pull data from a file or read it from stdio as a if someone is  "cat something|ft"
        #if its a pipe, lets shove it into a temp file
        if None ==self.data:
            if select.select([sys.stdin,],[],[],0.0)[0]:
                fd, temp_path = tempfile.mkstemp()
                line=sys.stdin.read()
                os.write(fd,line)
                os.close(fd)
                self.config.file=temp_path
                self.config.is_temp_file=True
            else:
                if None == self.config.file:
                    raise Exception("No input file available" )
                if False == os.path.exists(self.config.file):
                    raise Exception("file does not exist" )
                if False == os.path.isfile(self.config.file):
                    raise Exception("not a valid file")
            buffer=self.process_file()
        else:
            buffer=self.data
        #print(buffer)


        # now we have a file, from stdin or a file on the system that we can access    
        # print buffer
        self.calculate_limits()
        # print(buffer)
        #print(rows)
        if self.config.output=='ASCII':
            header=self.build_header()
            mid_header=self.build_header(mid=True)
            footer=self.build_header(footer=True)
            rows=self.build_rows(buffer)
            
            index=1

            if sys.version_info.major>2:
                encode=False
            else:
                encode=True


            if self.config.header==True:
                self.output(header,encode)

            for row in rows:
                self.output(row,encode)
                
                if self.config.header_every>0:                
                    # we want it every N, but not if it bunches up on the footer
                    if index%self.config.header_every==0 and len(buffer)-index>self.config.header_every :
                        self.output(mid_header,encode)
                index+=1
            if self.config.footer==True:
                self.output(footer,encode)
            return
        try:
            if self.config.output.upper()=='JSON':
                import json
                print( json.dumps({'rows':buffer,'header':self.config.columns}, ensure_ascii=False))

            if self.config.output.upper()=='YAML':
               import yaml
               yaml.dump({'rows':buffer,'header':self.config.columns}, sys.stdout)
        except Exception as ex:
            print (ex)

            
        
    
        #print ("Error Count: {0}. Results: {1}".format(table.error_count(),table.results_length()) )
    
    def output(self,text,encode):
        if encode:
            print(text.encode('utf-8'))
        else:
            print (text)


    def print_errors(table):
        for e in table.errors:
            print(e.encode('utf-8'))
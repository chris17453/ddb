# -*- coding: utf-8 -*-
# cython: linetrace=True

import sys
import os
from  subprocess import Popen


class tty_code:
 
    class attributes:
        BOLD         ='\033[{0}m'.format(1)
        DIM          ='\033[{0}m'.format(2)
        UNDERLINED   ='\033[{0}m'.format(4)
        BLINK        ='\033[{0}m'.format(5)
        REVERSE      ='\033[{0}m'.format(7)
        HIDDEN       ='\033[{0}m'.format(8)
        
    class reset:
        ALL          ='\033[{0}m'.format(0)
        BOLD         ='\033[{0}m'.format(21)
        DIM          ='\033[{0}m'.format(22)
        UNDERLINED   ='\033[{0}m'.format(24)
        BLINK        ='\033[{0}m'.format(25)
        REVERSE      ='\033[{0}m'.format(27)
        HIDDEN       ='\033[{0}m'.format(28)

    class foreground:
        DEFAULT      ='\033[{0}m'.format(39)
        BLACK        ='\033[{0}m'.format(30)
        RED          ='\033[{0}m'.format(31)
        GREEN        ='\033[{0}m'.format(32)
        YELLOW       ='\033[{0}m'.format(33)
        BLUE         ='\033[{0}m'.format(34)
        MAGENTA      ='\033[{0}m'.format(35)
        CYAN         ='\033[{0}m'.format(36)
        LIGHT_GRAY   ='\033[{0}m'.format(37)
        DARK_GRAY    ='\033[{0}m'.format(90)
        LIGHT_RED    ='\033[{0}m'.format(91)
        LIGHT_GREEN  ='\033[{0}m'.format(92)
        LIGHT_YELLOW ='\033[{0}m'.format(93)
        LIGHT_BLUE   ='\033[{0}m'.format(94)
        LIGHT_MAGENTA='\033[{0}m'.format(95)
        LIGHT_CYAN   ='\033[{0}m'.format(96)
        WHITE        ='\033[{0}m'.format(97)

    class background:
        DEFAULT      ='\033[{0}m'.format(49)
        BLACK        ='\033[{0}m'.format(40)
        RED          ='\033[{0}m'.format(41)
        GREEN        ='\033[{0}m'.format(42)
        YELLOW       ='\033[{0}m'.format(43)
        BLUE         ='\033[{0}m'.format(44)
        MAGENTA      ='\033[{0}m'.format(45)
        CYAN         ='\033[{0}m'.format(46)
        LIGHT_GRAY   ='\033[{0}m'.format(47)
        DARK_GRAY    ='\033[{0}m'.format(100)
        LIGHT_RED    ='\033[{0}m'.format(101)
        LIGHT_GREEN  ='\033[{0}m'.format(102)
        LIGHT_YELLOW ='\033[{0}m'.format(103)
        LIGHT_BLUE   ='\033[{0}m'.format(104)
        LIGHT_MAGENTA='\033[{0}m'.format(105)
        LIGHT_CYAN   ='\033[{0}m'.format(106)
        WHITE        ='\033[{0}m'.format(107)




class flextable:

    @staticmethod
    def colors(foreground,background,dim=None,bold=None):
        color=''
        if dim !=None:
            color+=tty_code.attributes.DIM
        if bold !=None:
            color+=tty_code.attributes.BOLD
            
        if None != foreground:
            if foreground.upper() == 'DEFAULT' :
                color+=tty_code.foreground.DEFAULT
            if foreground.upper() == 'BLACK' :
                color+=tty_code.foreground.BLACK
            if foreground.upper() == 'RED' :
                color+=tty_code.foreground.RED
            if foreground.upper() == 'GREEN' :
                color+=tty_code.foreground.GREEN
            if foreground.upper() == 'YELLOW' :
                color+=tty_code.foreground.YELLOW
            if foreground.upper() == 'BLUE' :
                color+=tty_code.foreground.BLUE
            if foreground.upper() == 'MAGENTA' :
                color+=tty_code.foreground.MAGENTA
            if foreground.upper() == 'CYAN' :
                color+=tty_code.foreground.CYAN
            if foreground.upper() == 'LIGHT GRAY' :
                color+=tty_code.foreground.LIGHT_GRAY
            if foreground.upper() == 'DARK GRAY' :
                color+=tty_code.foreground.DARK_GRAY
            if foreground.upper() == 'LIGHT RED' :
                color+=tty_code.foreground.LIGHT_RED
            if foreground.upper() == 'LIGHT GREEN' :
                color+=tty_code.foreground.LIGHT_GREEN
            if foreground.upper() == 'LIGHT YELLOW' :
                color+=tty_code.foreground.LIGHT_YELLOW
            if foreground.upper() == 'LIGHT BLUE' :
                color+=tty_code.foreground.LIGHT_BLUE
            if foreground.upper() == 'LIGHT MAGENTA' :
                color+=tty_code.foreground.LIGHT_MAGENTA
            if foreground.upper() == 'LIGHT CYAN' :
                color+=tty_code.foreground.LIGHT_CYAN
            if foreground.upper() == 'WHITE' :
                color+=tty_code.foreground.WHITE
        if None != background:
            if  background.upper() == 'DEFAULT' :
                color+=tty_code.background.DEFAULT
            if  background.upper() == 'BLACK' :
                color+=tty_code.background.BLACK
            if  background.upper() == 'RED' :
                color+=tty_code.background.RED
            if  background.upper() == 'GREEN' :
                color+=tty_code.background.GREEN
            if  background.upper() == 'YELLOW' :
                color+=tty_code.background.YELLOW
            if  background.upper() == 'BLUE' :
                color+=tty_code.background.BLUE
            if  background.upper() == 'MAGENTA' :
                color+=tty_code.background.MAGENTA
            if  background.upper() == 'CYAN' :
                color+=tty_code.background.CYAN
            if  background.upper() == 'LIGHT GRAY' :
                color+=tty_code.background.LIGHT_GRAY
            if  background.upper() == 'DARK GRAY' :
                color+=tty_code.background.DARK_GRAY
            if  background.upper() == 'LIGHT RED' :
                color+=tty_code.background.LIGHT_RED
            if  background.upper() == 'LIGHT GREEN' :
                color+=tty_code.background.LIGHT_GREEN
            if  background.upper() == 'LIGHT YELLOW' :
                color+=tty_code.background.LIGHT_YELLOW
            if  background.upper() == 'LIGHT BLUE' :
                color+=tty_code.background.LIGHT_BLUE
            if  background.upper() == 'LIGHT MAGENTA' :
                color+=tty_code.background.LIGHT_MAGENTA
            if  background.upper() == 'LIGHT CYAN' :
                color+=tty_code.background.LIGHT_CYAN
            if  background.upper() == 'WHITE' :
                color+=tty_code.background.WHITE
        return color

    class flextable_style:
        def __init__(self,style='rst'):
            self.whitespace=''
            self.line_ending='LRCF'
            self.color=flextable.modes()
            self.characters=flextable.characters(self.color.default,style)

        # Helper classes
    class color:
        def __init__(self,foreground=None,background=None,text=None,dim=None,bold=None,default=None):
            self.foreground=foreground
            self.background=background
            self.dim=dim
            self.bold=bold
            self.reset=tty_code.reset.ALL
            #override missing colors
            if None != default :
                if None== foreground:
                    foreground=default.foreground
                if None== background:
                    background=default.background
                if None== dim:
                    dim=default.dim
                if None == bold:
                    bold=default.bold
                    
            #print foreground,background,dim,bold
            self.color=flextable.colors(foreground=foreground,background=background,dim=dim,bold=bold)
            if None !=text:
                if text.isspace(): 
                    text=None
            self.text=text
                    
        
        def render(self,text=None, length=None,fill_character=' ',override=None,use_color=True):
            if text==None:
                text=self.text

    
            if None == text:
                text=''
                #TODO tabstop/tab
            
            # make safe
            #text='{0}'.format(text)
            # make sure its a string
            try:
                if isinstance(text,bool):
                    text=str(text)
                if isinstance(text,int):
                    text=str(text)
                elif not isinstance(text,unicode):
                    text=str(text)
            except:
                pass
            
            if text.find('\t')>-1:
                text=text.replace('\t','       ')
            
            text=text.rstrip()
            if length!=None:
                # because python data storage differes in 2&3 (float vs int)
                length=int(length)
                text=text[:length].ljust(length,fill_character)
            if use_color is False or use_color is None:
                return text
            if None!=override:
                return u"{0}{1}".format(override.color,text)    
            return u"{0}{1}{2}".format(self.color,text,self.reset)

    class modes:
        def __init__(self):
            self.default  =flextable.color('blue'      )
            self.error    =flextable.color('red'        ,bold=True,default=self.default)
            self.overflow =flextable.color('yellow'     ,default=self.default)
            self.comment  =flextable.color('yellow'     ,default=self.default)
            self.data     =flextable.color('light gray' ,default=self.default)
            self.active   =flextable.color('white'      ,default=self.default)
            self.edit     =flextable.color('cyan'       ,default=self.default)
            self.disabled =flextable.color('dark gray'  ,default=self.default)

    class characters:
        class char_walls:
            
            def __init__(self,default=None,style='rst'):
                if style=='single':
                    l=u'│'
                    r=u'│'
                    t=u'─'
                    b=u'─'
                elif style=='double':
                    l=u'║'
                    r=u'║'
                    t=u'═'
                    b=u'═'
                elif style=='rst':
                    l=u'|'
                    r=u'|'
                    t=u'-'
                    b=u'-'

                self.left   =flextable.color(text=l,default=default)
                self.right  =flextable.color(text=r,default=default)
                self.top    =flextable.color(text=t,default=default)
                self.bottom =flextable.color(text=b,default=default)
        class char_center:
            def __init__(self,default=None,style='rst'):
                if style=='single':
                    l=u'├'
                    c=u'┼'
                    r=u'┤'
                elif style=='double':
                    l=u'╠'
                    c=u'╬'
                    r=u'╣'
                elif style=='rst':
                    l=u'|'
                    c=u'|'
                    r=u'|'

                self.center = flextable.color(text=c,default=default)
                self.left   = flextable.color(text=l,default=default)
                self.right  = flextable.color(text=r,default=default)

        class char_rst:
            def __init__(self,default=None):
                self.edge   =flextable.color(text='+',default=default)
                self.space  =flextable.color(text=' ',default=default)
                self.header =flextable.color(text='=',default=default)
                self.row    =flextable.color(text='-',default=default)
                
        class char_bottom:
            def __init__(self,default=None,style='rst'):
                if style=='single':
                    l=u'└'
                    c=u'┴'
                    r=u'┘'
                elif style=='double':
                    l=u'╚'
                    c=u'╩'
                    r=u'╝'
                elif style=='rst':
                    l=u'+'
                    c=u'+'
                    r=u'+'

                self.left   = flextable.color(text=l,default=default)
                self.center = flextable.color(text=c,default=default)
                self.right  = flextable.color(text=r,default=default)
        class char_top:
            def __init__(self,default=None,style='rst'):
                if style == 'single':
                    l=u'┌'
                    c=u'┬'
                    r=u'┐'
                elif style=='double':
                    l=u'╔'
                    c=u'╦'
                    r=u'╗'
                elif style=='rst':
                    l=u'|'
                    c=u'|'
                    r=u'|'

                self.left   = flextable.color(text=l,default=default)
                self.right  = flextable.color(text=r,default=default)
                self.center = flextable.color(text=c,default=default)
        class char_header:
            def __init__(self,default=None,style='rst'):
                if style=='single':
                    l=u'┤'
                    c=u' '
                    r=u'├'
                elif style=='double':
                    l=u'╡'
                    c=u' '
                    r=u'╞'
                elif style=='rst':
                    l=u''
                    c=u' '
                    r=u''
                       
                self.left   = flextable.color(text=l,default=default,foreground='White')
                self.right  = flextable.color(text=r,default=default,foreground='White')
                self.center = flextable.color(text=c,default=default,foreground='green')
        class char_mid_header:
            def __init__(self,default=None,style='rst'):
                if style == 'single':
                    l=u'-'
                    c=u' '
                    r=u'-'
                elif style== 'double':
                    l=u'-'
                    r=u'-'
                    c=u' '
                elif style=='rst':
                    l=u'-'
                    c=u' '
                    r=u'-'

                self.left   = flextable.color(text=l,default=default,foreground='White')
                self.right  = flextable.color(text=r,default=default,foreground='White')
                self.center = flextable.color(text=c,default=default,foreground='green')
        class char_footer:
            def __init__(self,default=None,style='rst'):

                if style=='single':
                    l=u'['
                    c=u' '
                    r=u']'
                elif style=='double':
                    l=u'['
                    c=u' '
                    r=u']'
                elif style=='rst':
                    l=None
                    c=u' '
                    r=None
                self.left   = flextable.color(text=l,default=default,foreground='White') #╡
                self.right  = flextable.color(text=r,default=default,foreground='White') #╞
                self.center = flextable.color(text=c,default=default,foreground='green')

        def __init__(self,default=None,style='rst'):
            
            self.walls      =self.char_walls(default=default,style=style)
            self.center     =self.char_center(default=default,style=style)
            self.bottom     =self.char_bottom(default=default,style=style)
            self.top        =self.char_top(default=default,style=style)
            self.mid_header =self.char_mid_header(default=default,style=style)
            self.header     =self.char_header(default=default,style=style)
            self.footer     =self.char_footer(default=default,style=style)
            self.rst        =self.char_rst(default=default)



    class data_type:
        COMMENT=1
        ERROR=2
        DATA=3
        WHITESPACE=4
    
    def __init__(self,      data,
                            display_style='single',
                            column_count=0,
                            hide_comments=False,
                            hide_errors=False,
                            hide_whitespace=False,
                            columns=None,
                            length=None,
                            line=0,
                            page=0,
                            header=True,
                            footer=True,
                            header_every=-1,
                            tab_width=4,
                            tab_stop=8,
                            row_height=-1,
                            column_width=-1,
                            render_color=True,
                            output_stream='STDIO'
                        ):
        self.column_count=column_count
        self.hide_comments=hide_comments
        self.hide_errors=hide_errors
        self.hide_whitespace=hide_whitespace
        self.columns=columns
        self.length=length
        self.line=line
        self.page=page
        self.header=header
        self.footer=footer
        self.header_every=header_every
        self.tab_width=tab_width
        self.tab_stop=tab_stop
        self.row_height=row_height
        self.column_width=column_width
        self.render_color=render_color
        self.is_temp_file=False
        if display_style not in ['single','double','rst']:
            display_style='single'    
        self.display_style=display_style
        if output_stream=='STDIO':
            self.output_destination=None
        elif output_stream=='STRING':
            self.output_destination=[]
        else:
            self.output_destination=None

        if self.column_width==-1:
            pro=os.popen('stty -F /dev/tty size', 'r')
            try:

                self.row_height,self.column_width =pro.read().split()
                pro.close()
                
            except Exception, ex:
                print (ex)
                pro.close()
                self.row_height=25
                self.column_width=80
                pass
        #auto name columns
        if column_count>-1 and columns == None:
            self.columns=[]
            for n in range(0,self.column_count):
                self.columns.append("column{0}".format(n+1))

        # when specifically setting columns up... iverrides auto naming columns
        else:
            self.column_count=len(columns)
        
        
        if page>-1 and length:
            if length>0:
                self.starts_on=page*length+1
        if self.line>-1:
            self.starts_on=line

        if display_style=='rst':
            self.footer=False
            self.header_every=0
        self.style=self.flextable_style(style=self.display_style)
        self.results=[]
        self.data=data
        self.format()


    def calculate_limits(self):
        tty_min_column_width=1
        # doesnt work with pipes. ugh
        
        # tty_rows=int(tty_rows)
        # tty_columns=int(tty_columns)
        # dev size
        # tty_rows=30
        # tty_columns=80
        
        
        data_column_count=len(self.columns)

        pad=data_column_count+1
        # no columns to return
        if data_column_count==0:
            self.column_character_width=-1
        else:
            if self.column_width!=-1:
                self.column_character_width=int((int(self.column_width)-1-pad)/data_column_count)
                if self.column_character_width<tty_min_column_width:
                    self.column_character_width=tty_min_column_width
            #@else:
            #    print(self.column_width)
            #    self.column_character_width=int(self.width)


        self.total_width=self.column_character_width*data_column_count+data_column_count-1

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
        header=base.left.render(use_color=self.render_color)

        column_pad=0
        
        
        if column.left.text:
            column_pad+=1
        if column.right.text:
            column_pad+=1

        if None != self.columns:
            index=0
            for c in self.columns:
                column_display=''
                if column.left.text:
                    column_display=column.left.render(use_color=self.render_color)

                column_display+=column.center.render(use_color=self.render_color,text=c,length=self.column_character_width-column_pad)
                #print self.column_character_width-column_pad

                if column.right.text:
                    column_display+=column.right.render(use_color=self.render_color)
                

                header+=column_display

                # if we have overflow, change the column wall on the right
                if index<len(self.columns)-1:
                    if len('{0}'.format(c))>self.column_character_width-2:
                        header+=base.center.render(use_color=self.render_color,override=self.style.color.overflow)
                    else:
                        header+=base.center.render(use_color=self.render_color)
                index+=1
        header+=base.right.render(use_color=self.render_color)
        if self.render_color==True:
            header+='{0}'.format(tty_code.reset.ALL)


        return header
            
    def build_rows(self,buffer):
        rows=[]
        index=0
        if True == isinstance(buffer,list):
            for line in buffer:
                data_len=len(line['data'])
                columns=self.style.characters.walls.left.render(use_color=self.render_color)
                #print line
                
                if self.data_type.DATA == line['type']:
                    for c in line['data']:
                        columns+=self.style.color.data.render(c,use_color=self.render_color,length=self.column_character_width)
                        # if we have overflow, change the column wall on the right
                        if len('{0}'.format(c))>self.column_character_width:
                            columns+=self.style.characters.walls.right.render(use_color=self.render_color,override=self.style.color.overflow)
                        else:
                            columns+=self.style.characters.walls.right.render(use_color=self.render_color)
                        
                    #only happend if we allow errored rows            
                    if data_len < self.column_count:
                        wall_color=tty_code.background.LIGHT_BLUE
                        for c in range(data_len,self.column_count):
                            columns+=self.style.color.comment.render('',use_color=self.render_color,length=self.column_character_width)
                            columns+=self.style.characters.walls.right.render(use_color=self.render_color,override=self.style.color.error)
                
                
                elif self.data_type.COMMENT ==  line['type'] or self.data_type.WHITESPACE==line['type']:
                    left  =self.style.characters.walls.left.render(use_color=self.render_color)
                    center=self.style.color.comment.render(line['raw'],use_color=self.render_color,length=self.total_width)
                    right =self.style.characters.walls.right.render(use_color=self.render_color)
                    columns=u"{0}{1}{2}".format( left,
                                                center,
                                                right)
                
                elif self.data_type.ERROR ==  line['type']:
                    left  =self.style.characters.walls.left.render(use_color=self.render_color)
                    center=self.style.color.error.render(line['raw'],use_color=self.render_color,length=self.total_width)
                    right =self.style.characters.walls.right.render(use_color=self.render_color)
                    columns=u"{0}{1}{2}".format( left,
                                                center,
                                                right)
                if self.render_color==True:
                    columns+='{0}'.format(tty_code.reset.ALL)

                rows.append(columns)
                index+=1
                #if index== int(tty_rows)-5:
                #    index=0
                #    rows.append(self.)
        else:
            raise Exception ("data is invalid: -> {0}".format(buffer))

        return rows

    def build_row_seperator(self,header=None):
        index=0
        if header:
            char=self.style.characters.rst.header.text
        else:
            char=self.style.characters.rst.row.text
        row=self.style.characters.rst.edge.render()
        for i in range(0,self.column_count):
            row+=self.style.characters.rst.row.render('',fill_character=char,use_color=self.render_color,length=self.column_character_width)
            row+=self.style.characters.rst.edge.render()

        if self.render_color==True:
            row+='{0}'.format(tty_code.reset.ALL)

        return row
     
    def output(self,text,encode):
        if isinstance(self.output_destination,list):
            if encode:
                self.output_destination.append(text.encode('utf-8'))
            else:
                self.output_destination.append(text)
        else:
            if encode:
                print(text.encode('utf-8'))
            else:
                print (text)

    def print_errors(self,table):
        for e in table.errors:
            print(e.encode('utf-8'))
                        
    # with no columns, everything will be run on, not well formated
    def format(self):
        # now we have a file, from stdin or a file on the system that we can access    
        # print buffer
        self.calculate_limits()
        header=self.build_header()
        mid_header=self.build_header(mid=True)
        footer=self.build_header(footer=True)
        rows=self.build_rows(self.data)
        row_seperator=self.build_row_seperator()
        row_header_seperator=self.build_row_seperator(header=True)
        index=1

        try:
            if sys.version_info.major>2:
                encode=False
            else:
                encode=True
        except:
            encode=False
            pass

        self.output('',encode)

        if self.header==True:
            if self.display_style=='rst':
                self.output(row_seperator,encode)
            self.output(header,encode)
            if self.display_style=='rst':
                self.output(row_header_seperator,encode)

        
        for row in rows:
            self.output(row,encode)
            if self.display_style=='rst':
                self.output(row_seperator,encode)
            if self.header_every>0:                
                # we want it every N, but not if it bunches up on the footer
                if index%self.header_every==0 and index>0:
                    self.output(mid_header,encode)
            index+=1
        if self.footer==True:
            self.output(footer,encode)

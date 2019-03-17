# -*- coding: utf-8 -*-
import sys
import os

class flextable:

    def escape(c):
        return u'\033[{}m'.format(c)

    def enum(**enums):
        return type('Enum', (), enums)

    attributes=enum( BOLD    =escape(1),
                DIM          =escape(2),
                UNDERLINED   =escape(4),
                BLINK        =escape(5),
                REVERSE      =escape(7),
                HIDDEN       =escape(8))
        
    reset=enum( ALL          =escape(0),
                BOLD         =escape(21),
                DIM          =escape(22),
                UNDERLINED   =escape(24),
                BLINK        =escape(25),
                REVERSE      =escape(27),
                HIDDEN       =escape(28))

    fg=enum(    DEFAULT      =escape(39),
                BLACK        =escape(30),
                RED          =escape(31),
                GREEN        =escape(32),
                YELLOW       =escape(33),
                BLUE         =escape(34),
                MAGENTA      =escape(35),
                CYAN         =escape(36),
                LIGHT_GRAY   =escape(37),
                DARK_GRAY    =escape(90),
                LIGHT_RED    =escape(91),
                LIGHT_GREEN  =escape(92),
                LIGHT_YELLOW =escape(93),
                LIGHT_BLUE   =escape(94),
                LIGHT_MAGENTA=escape(95),
                LIGHT_CYAN   =escape(96),
                WHITE        =escape(97))

    bg=enum(    DEFAULT      =escape(49),
                BLACK        =escape(40),
                RED          =escape(41),
                GREEN        =escape(42),
                YELLOW       =escape(43),
                BLUE         =escape(44),
                MAGENTA      =escape(45),
                CYAN         =escape(46),
                LIGHT_GRAY   =escape(47),
                DARK_GRAY    =escape(100),
                LIGHT_RED    =escape(101),
                LIGHT_GREEN  =escape(102),
                LIGHT_YELLOW =escape(103),
                LIGHT_BLUE   =escape(104),
                LIGHT_MAGENTA=escape(105),
                LIGHT_CYAN   =escape(106),
                WHITE        =escape(107))

    @staticmethod
    def colors(foreground,background,dim=None,bold=None):
        color=''
        if dim !=None:
            color+=flextable.attributes.DIM
        if bold !=None:
            color+=flextable.attributes.BOLD
            
        if None != foreground:
            if foreground.upper() == 'DEFAULT' :
                color+=flextable.fg.DEFAULT
            if foreground.upper() == 'BLACK' :
                color+=flextable.fg.BLACK
            if foreground.upper() == 'RED' :
                color+=flextable.fg.RED
            if foreground.upper() == 'GREEN' :
                color+=flextable.fg.GREEN
            if foreground.upper() == 'YELLOW' :
                color+=flextable.fg.YELLOW
            if foreground.upper() == 'BLUE' :
                color+=flextable.fg.BLUE
            if foreground.upper() == 'MAGENTA' :
                color+=flextable.fg.MAGENTA
            if foreground.upper() == 'CYAN' :
                color+=flextable.fg.CYAN
            if foreground.upper() == 'LIGHT GRAY' :
                color+=flextable.fg.LIGHT_GRAY
            if foreground.upper() == 'DARK GRAY' :
                color+=flextable.fg.DARK_GRAY
            if foreground.upper() == 'LIGHT RED' :
                color+=flextable.fg.LIGHT_RED
            if foreground.upper() == 'LIGHT GREEN' :
                color+=flextable.fg.LIGHT_GREEN
            if foreground.upper() == 'LIGHT YELLOW' :
                color+=flextable.fg.LIGHT_YELLOW
            if foreground.upper() == 'LIGHT BLUE' :
                color+=flextable.fg.LIGHT_BLUE
            if foreground.upper() == 'LIGHT MAGENTA' :
                color+=flextable.fg.LIGHT_MAGENTA
            if foreground.upper() == 'LIGHT CYAN' :
                color+=flextable.fg.LIGHT_CYAN
            if foreground.upper() == 'WHITE' :
                color+=flextable.fg.WHITE
        if None != background:
            if  background.upper() == 'DEFAULT' :
                color+=flextable.bg.DEFAULT
            if  background.upper() == 'BLACK' :
                color+=flextable.bg.BLACK
            if  background.upper() == 'RED' :
                color+=flextable.bg.RED
            if  background.upper() == 'GREEN' :
                color+=flextable.bg.GREEN
            if  background.upper() == 'YELLOW' :
                color+=flextable.bg.YELLOW
            if  background.upper() == 'BLUE' :
                color+=flextable.bg.BLUE
            if  background.upper() == 'MAGENTA' :
                color+=flextable.bg.MAGENTA
            if  background.upper() == 'CYAN' :
                color+=flextable.bg.CYAN
            if  background.upper() == 'LIGHT GRAY' :
                color+=flextable.bg.LIGHT_GRAY
            if  background.upper() == 'DARK GRAY' :
                color+=flextable.bg.DARK_GRAY
            if  background.upper() == 'LIGHT RED' :
                color+=flextable.bg.LIGHT_RED
            if  background.upper() == 'LIGHT GREEN' :
                color+=flextable.bg.LIGHT_GREEN
            if  background.upper() == 'LIGHT YELLOW' :
                color+=flextable.bg.LIGHT_YELLOW
            if  background.upper() == 'LIGHT BLUE' :
                color+=flextable.bg.LIGHT_BLUE
            if  background.upper() == 'LIGHT MAGENTA' :
                color+=flextable.bg.LIGHT_MAGENTA
            if  background.upper() == 'LIGHT CYAN' :
                color+=flextable.bg.LIGHT_CYAN
            if  background.upper() == 'WHITE' :
                color+=flextable.bg.WHITE
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
            self.reset=flextable.reset.ALL
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
                if text.rstrip()=='': 
                    text=None
            self.text=text
                    
        
        def render(self,text=None, length=None,fill_character=' ',override=None,use_color=True):
            if text==None:
                text=self.text

    
            if None == text:
                text=''
                #TODO tabstop/tab
            
            # make safe
            text=u'{}'.format(text)
            text=text.replace(u'\t',u'       ')
            
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
                    h=u'='

                self.left   =flextable.color(text=l,default=default)
                self.right  =flextable.color(text=r,default=default)
                self.top    =flextable.color(text=t,default=default)
                self.bottom =flextable.color(text=b,default=default)
        class char_center:
            def __init__(self,default=None,style='rst'):
                if style=='single':
                    c=u'┼'
                    l=u'├'
                    r=u'┤'
                elif style=='double':
                    c=u'╬'
                    l=u'╠'
                    r=u'╣'
                elif style=='rst':
                    c=u'+'
                    l=u'+'
                    r=u'+'

                self.center = flextable.color(text=c,default=default)
                self.left   = flextable.color(text=l,default=default)
                self.right  = flextable.color(text=r,default=default)     
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
                    r=u'┐'
                    c=u'┬'
                elif style=='doubble':
                    l=u'╔'
                    r=u'╗'
                    c=u'╦'
                elif style=='rst':
                    l=u'+'
                    c=u'+'
                    r=u'+'

                self.left   = flextable.color(text=l,default=default)
                self.right  = flextable.color(text=c,default=default)
                self.center = flextable.color(text=r,default=default)
        class char_header:
            def __init__(self,default=None,style='rst'):
                if style=='single':
                    l=u'┤'
                    r=u'├'
                    c=u' '
                elif style=='double':
                    l=u'╡'
                    r=u'╞'
                    c=u' '
                elif style=='rst':
                    l=u''
                    r=u''
                    c=u' '
                       
                self.left   = flextable.color(text=l,default=default,foreground='White')
                self.right  = flextable.color(text=r,default=default,foreground='White')
                self.center = flextable.color(text=c,default=default,foreground='green')
        class char_mid_header:
            def __init__(self,default=None,style='rst'):
                if style == 'single':
                    l=u'-'
                    r=u'-'
                    c=u' '
                elif style== 'double':
                    l=u'-'
                    r=u'-'
                    c=u' '
                elif style=='rst':
                    l=u'-'
                    r=u'-'
                    c=u' '

                self.left   = flextable.color(text=l,default=default,foreground='White')
                self.right  = flextable.color(text=r,default=default,foreground='White')
                self.center = flextable.color(text=c,default=default,foreground='green')
        class char_footer:
            def __init__(self,default=None,style='rst'):

                if style=='single':
                    l=u'['
                    r=u']'
                    c=u' '
                elif style=='double':
                    l=u'['
                    r=u']'
                    c=u' '
                elif style=='rst':
                    l=''
                    r=''
                    c=' '
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



    data_type=enum(COMMENT=1,ERROR=2,DATA=3,WHITESPACE=4)
    
    def __init__(self,      data,
                            display_style='rst',
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
                            render_color=True
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


        if self.column_width==-1:
            self.row_height,self.column_width = os.popen('stty -F /dev/tty size', 'r').read().split()
        #auto name columns
        if column_count>-1 and columns == None:
            self.columns=[]
            for n in range(0,self.column_count):
                self.columns.append("column{0}".format(n+1))

        # when specifically setting columns up... iverrides auto naming columns
        else:
            self.column_count=len(columns)
        
        
        if page>-1 and length>1:
            self.starts_on=page*length+1
        if self.line>-1:
            self.starts_on=line

        self.style=self.flextable_style(style=display_style)
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
        if None!=column.left.text:
            column_pad+=1
        if None!=column.right.text:
            column_pad+=1

        if None != self.columns:
            index=0
            for c in self.columns:
                column_display=u''
                if None!=column.left.text:
                    column_display=column.left.render(use_color=self.render_color)

                column_display+=column.center.render(use_color=self.render_color,text=c,length=self.column_character_width-column_pad)
                #print self.column_character_width-column_pad

                if None!=column.right.text:
                    column_display+=column.right.render(use_color=self.render_color)
                

                header+=column_display

                # if we have overflow, change the column wall ont he right
                if index<len(self.columns)-1:
                    if len('{0}'.format(c))>self.column_character_width-2:
                        header+=base.center.render(use_color=self.render_color,override=self.style.color.overflow)
                    else:
                        header+=base.center.render(use_color=self.render_color)
                index+=1
        header+=base.right.render(use_color=self.render_color)
        header+=u'{0}'.format(flextable.reset.ALL)


        return header
            
    def build_rows(self,buffer,rst=None):
        rows=[]
        index=0
        if True == isinstance(buffer,list) or rst==True:
            for line in buffer:
                columns=self.style.characters.walls.left.render(use_color=self.render_color)
                #print line
                
                if self.data_type.DATA == line['type']:
                    for c in line['data']:
                        columns+=self.style.color.data.render(c,use_color=self.render_color,length=self.column_character_width)
                        # if we have overflow, change the column wall on the right
                        if len('{}'.format(c))>self.column_character_width:
                            columns+=self.style.characters.walls.right.render(use_color=self.render_color,override=self.style.color.overflow)
                        else:
                            columns+=self.style.characters.walls.right.render(use_color=self.render_color)
                        
                    #only happend if we allow errored rows            
                    if len(line['data']) < self.column_count:
                        wall_color=flextable.bg.LIGHT_BLUE
                        for c in range(len(line['data']),self.column_count):
                            columns+=self.style.color.comment.render('',use_color=self.render_color,length=self.column_character_width)
                            columns+=self.style.characters.walls.right.render(use_color=self.render_color,override=self.style.color.error)
                            
                
                
                if self.data_type.COMMENT ==  line['type'] or self.data_type.WHITESPACE==line['type']:
                    left  =self.style.characters.walls.left.render(use_color=self.render_color)
                    center=self.style.color.comment.render(line['raw'],use_color=self.render_color,length=self.total_width)
                    right =self.style.characters.walls.right.render(use_color=self.render_color)
                    columns=u"{0}{1}{2}".format( left,
                                                center,
                                                right)
                
                if self.data_type.ERROR ==  line['type']:
                    left  =self.style.characters.walls.left.render(use_color=self.render_color)
                    center=self.style.color.error.render(line['raw'],use_color=self.render_color,length=self.total_width)
                    right =self.style.characters.walls.right.render(use_color=self.render_color)
                    columns=u"{0}{1}{2}".format( left,
                                                center,
                                                right)
                columns+=u'{}'.format(flextable.reset.ALL)

                rows.append(columns)
                index+=1
                #if index== int(tty_rows)-5:
                #    index=0
                #    rows.append(self.)
        else:
            raise Exception ("data is invalid: ->".format(buffer))

        return rows
            
    def build_rst_spacer(self):
        row=self.style.characters.center.left.render(use_color=self.render_color)
        
        for c in range(0,self.column_count):
            row+=self.style.color.default.render('x',use_color=self.render_color,length=self.column_character_width)
            row+=self.style.characters.center.right.render(use_color=self.render_color)
        
        row+=u'{}'.format(flextable.reset.ALL)

        return row

    def output(self,text,encode):
        if encode:
            print(text.encode('utf-8'))
        else:
            print (text)

    def print_errors(table):
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
        rst_spacer=self.build_rst_spacer()

        index=1

        if sys.version_info.major>2:
            encode=False
        else:
            encode=True


        if self.header==True:
            self.output(header,encode)

        for row in rows:
            self.output(row,encode)
            if self.display_style=='rst':
                self.output(rst_spacer)
            if self.header_every>0:                
                # we want it every N, but not if it bunches up on the footer
                if index%self.header_every==0 and len(buffer)-index>self.header_every :
                    self.output(mid_header,encode)
            index+=1
        if self.footer==True:
            self.output(footer,encode)

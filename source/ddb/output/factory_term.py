# -*- coding: utf-8 -*-
import sys

class flextable:


    class style:
        def __init__(self,style='single'):
            self.whitespace=''
            self.line_ending='LRCF'
            self.color=modes()
            self.characters=characters(self.color.default,style)

        # Helper classes
    class color:
        def __init__(self,foreground=None,background=None,text=None,dim=None,bold=None,default=None):
            self.foreground=foreground
            self.background=background
            self.dim=dim
            self.bold=bold
            self.reset=reset.ALL
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
            self.color=colors(foreground=foreground,background=background,dim=dim,bold=bold)
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
            self.default  =color('blue'      )
            self.error    =color('red'        ,bold=True,default=self.default)
            self.overflow =color('yellow'     ,default=self.default)
            self.comment  =color('yellow'     ,default=self.default)
            self.data     =color('light gray' ,default=self.default)
            self.active   =color('white'      ,default=self.default)
            self.edit     =color('cyan'       ,default=self.default)
            self.disabled =color('dark gray'  ,default=self.default)


    class characters:
        class char_walls:
            
            def __init__(self,default=None,single=True):
                if single is True:
                    l=u'│'
                    r=u'│'
                    t=u'─'
                    b=u'─'
                else:
                    l=u'║'
                    r=u'║'
                    t=u'═'
                    b=u'═'
                self.left   =color(text=l,default=default)
                self.right  =color(text=r,default=default)
                self.top    =color(text=t,default=default)
                self.bottom =color(text=b,default=default)
        class char_center:
            def __init__(self,default=None,single=True):
                if single is True:
                    c=u'┼'
                    l=u'├'
                    r=u'┤'
                else:
                    c=u'╬'
                    l=u'╠'
                    r=u'╣'                        
                self.center = color(text=c,default=default)
                self.left   = color(text=l,default=default)
                self.right  = color(text=r,default=default)
        
        class char_bottom:
            def __init__(self,default=None,single=True):
                if single is True:
                    l=u'└'
                    c=u'┴'
                    r=u'┘'
                else:
                    l=u'╚'
                    c=u'╩'
                    r=u'╝'
                self.left   = color(text=l,default=default)
                self.center = color(text=c,default=default)
                self.right  = color(text=r,default=default)
        class char_top:
            def __init__(self,default=None,single=True):
                if single is True:
                    l=u'┌'
                    c=u'┐'
                    r=u'┬'
                else:
                    l=u'╔'
                    c=u'╗'
                    r=u'╦'
                self.left   = color(text=l,default=default)
                self.right  = color(text=c,default=default)
                self.center = color(text=r,default=default)
        class char_header:
            def __init__(self,default=None,single=True):
                if single is True:
                    l=u'┤'
                    r=u'├'
                    c=u' '
                else:
                    l=u'╡'
                    r=u'╞'
                    c=u' '            
                self.left   = color(text=l,default=default,foreground='White')
                self.right  = color(text=r,default=default,foreground='White')
                self.center = color(text=c,default=default,foreground='green')
        class char_mid_header:
            def __init__(self,default=None,single=True):
                if single is True:
                    l=u'-'
                    r=u'-'
                    c=u' '
                else:
                    l=u'-'
                    r=u'-'
                    c=u' '
                self.left   = color(text=l,default=default,foreground='White')
                self.right  = color(text=r,default=default,foreground='White')
                self.center = color(text=c,default=default,foreground='green')
        class char_footer:
            def __init__(self,default=None,single=True):
                if single is True:
                    l=u'['
                    r=u']'
                    c=u' '
                else:
                    l=u'['
                    r=u']'
                    c=u' '
                self.left   = color(text=l,default=default,foreground='White') #╡
                self.right  = color(text=r,default=default,foreground='White') #╞
                self.center = color(text=c,default=default,foreground='green')

        def __init__(self,default=None,style='single'):
            if style=='single':
                single=True
            else:
                single=False
            self.walls      =self.char_walls(default=default,single=single)
            self.center     =self.char_center(default=default,single=single)
            self.bottom     =self.char_bottom(default=default,single=single)
            self.top        =self.char_top(default=default,single=single)
            self.header     =self.char_header(default=default,single=single)
            self.mid_header =self.char_mid_header(default=default,single=single)
            self.footer     =self.char_footer(default=default,single=single)




    data_type=enum(COMMENT=1,ERROR=2,DATA=3,WHITESPACE=4)
    
    def __init__(self,      data,
                            style='single',
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
            self.row_height,self.column_width = os.popen('stty size', 'r').read().split()

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

        self.style=style()
        self.results=[]
        self.data=data
        self.format()



    def calculate_limits(self):
        tty_min_column_width=1
        # doesnt work with pipes. ugh
        # tty_rows, tty_columnstty_columns = os.popen('stty size', 'r').read().split()
        # tty_rows=int(tty_rows)
        # tty_columns=int(tty_columns)
        # dev size
        # tty_rows=30
        # tty_columns=80

        
        data_column_count=self.column_count
        pad=data_column_count+1
        # no columns to return
        if data_column_count==0:
            self.column_character_width=-1
        else:
            if self.column_width!=-1:
                self.column_character_width=int(int(self.column_width-1-pad)/data_column_count)
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
        header+=u'{0}'.format(reset.ALL)


        return header
            
    def build_rows(self,buffer):
        rows=[]
        index=0
        if True == isinstance(buffer,list):
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
                        wall_color=bcolors.OKBLUE
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
                columns+=u'{}'.format(reset.ALL)

                rows.append(columns)
                index+=1
                #if index== int(tty_rows)-5:
                #    index=0
                #    rows.append(self.)
        else:
            raise Exception ("data is invalid: ->".format(buffer))

        return rows

     
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
        rows=self.build_rows(buffer)
        
        index=1

        if sys.version_info.major>2:
            encode=False
        else:
            encode=True


        if self.header==True:
            self.output(header,encode)

        for row in rows:
            self.output(row,encode)
            
            if self.header_every>0:                
                # we want it every N, but not if it bunches up on the footer
                if index%self.header_every==0 and len(buffer)-index>self.header_every :
                    self.output(mid_header,encode)
            index+=1
        if self.footer==True:
            self.output(footer,encode)

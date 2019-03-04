class flextable_config:
    def __init__(self,      file=None,
                            remove_quote=True,
                            block_quote=None,
                            column_count=0,
                            hide_comments=False,
                            hide_errors=False,
                            hide_whitespace=False,
                            starts_on_line=1,
                            data_on_line=0,
                            header_on_line=0,
                            columns=None,
                            delimiter=None,
                            delimiters={'field':',',  'comment':'#'},
                            length=None,
                            line=0,
                            page=0,
                            starts_on=1,
                            header=True,
                            footer=True,
                            header_every=-1,
                            width='auto',
                            tab_width=4,
                            tab_stop=8,
                            row_height=-1,
                            column_width=-1,
                            width=0,
                            height=0,
                            output='ASCII',
                            render_color=True
                        ):
        self.file=file
        self.remove_quote=remove_quote
        self.block_quote=block_quote
        self.column_count=column_count
        self.hide_comments=hide_comments
        self.hide_errors=hide_errors
        self.hide_whitespace=hide_whitespace
        self.starts_on_line=starts_on_line
        self.data_on_line=data_on_line
        self.header_on_line=header_on_line
        self.columns=columns
        self.delimiter=delimiter
        self.delimiters=delimiters
        self.length=length
        self.line=line
        self.page=page
        self.starts_on=starts_on
        self.header=header
        self.footer=footer
        self.header_every=header_every
        self.width=width
        self.tab_width=tab_width
        self.tab_stop=tab_stop
        self.row_height=row_height
        self.column_width=column_width
        self.width=width
        self.height=height
        self.output=output
        self.render_color=render_color


        if self.column_width==-1:
            try:
                self.stdscr = curses.initscr()
                curses.cbreak()
                curses.noecho()
                self.stdscr.keypad(1)
                self.row_height,self.column_width = self.stdscr.getmaxyx()
            finally:
                curses.nocbreak()
                self.stdscr.keypad(0)
                curses.echo()
                curses.endwin()

        #auto name columns
        if column_count>-1 and columns == None:
            self.columns=[]
            for n in range(0,self.column_count):
                self.columns.append("column{0}".format(n+1))

        # when specifically setting columns up... iverrides auto naming columns
        else:
            self.set_columns(columns)
        
        
        if page>-1 and length>1:
            self.starts_on=page*length+1
        if self.line>-1:
            self.starts_on=line

        self.results=[]

    
    def set_columns(self,columns):
        if None != columns:
            self.columns=columns
            self.column_count=len(columns)
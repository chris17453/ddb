class table_config:
    def __init__(self):
        self.file=None
        self.remove_quote=True
        self.block_quote=None
        self.column_count=0
        self.hide_comments=False
        self.hide_errors=False
        self.hide_whitespace=False
        self.starts_on_line=1
        self.data_on_line=0
        self.header_on_line=0
        self.columns=None
        self.delimiter=None
        self.delimiters={'field':',',  'comment':'#'}
        self.length=None
        self.line=0
        self.page=0
        self.starts_on=1
        self.header=True
        self.footer=True
        self.header_every=-1
        self.width='auto'
        # TODO
        # exapanding from fixed point
        self.tab_width=4
        # TODO
        # comments align on tabstops
        self.tab_stop=8
        self.row_height=-1
        self.column_width=-1
        self.width=0
        self.height=0
        self.output='ASCII'
        self.no_color=False
        self.render_color=True #computed
    
    def set_columns(self,columns):
        if None != columns:
            self.columns=columns
            self.column_count=len(columns)
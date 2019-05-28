# cython: linetrace=True

class column_v1:

    def __init__(self, yaml=None):
        self.name = None
        self.display = None
        self.type = "string"
        self.default = None
        self.is_array = False
        self.has_default = False
        self.ordinal = -1
        self.visible = True
        self.fixed_width = True
        self.width = 100
        self.max_width = 0
        self.min_width = 0
        self.overflow = False
        self.search = False
        self.multi_search = False
        self.sort = False
        self.sort_ordinal = 0
        self.sort_default = False
        self.sort_default_asc = False
        self.data_ordinal = -1
        self.export = False
        self.options = {}
        if None != yaml:
            if 'name' in yaml:
                self.name = yaml['name']
            if 'display' in yaml:
                self.display = yaml['display']
            if 'type' in yaml:
                self.type = yaml['type']
            if 'default' in yaml:
                self.default = yaml['default']
            if 'is_array' in yaml:
                self.is_array = yaml['is_array']
            if 'has_default' in yaml:
                self.has_default = yaml['has_default']
            if 'ordinal' in yaml:
                self.ordinal = yaml['ordinal']
            if 'visible' in yaml:
                self.visible = yaml['visible']
            if 'fixed_width' in yaml:
                self.fixed_width = yaml['fixed_width']
            if 'width' in yaml:
                self.width = yaml['width']
            if 'max_width' in yaml:
                self.max_width = yaml['max_width']
            if 'min_width' in yaml:
                self.min_width = yaml['min_width']
            if 'overflow' in yaml:
                self.overflow = yaml['overflow']
            if 'search' in yaml:
                self.search = yaml['search']
            if 'multi_search' in yaml:
                self.multi_search = yaml['multi_search']
            if 'sort' in yaml:
                self.sort = yaml['sort']
            if 'sort_ordinal' in yaml:
                self.sort_ordinal = yaml['sort_ordinal']
            if 'sort_default' in yaml:
                self.sort_default = yaml['sort_default']
            if 'sort_default_asc' in yaml:
                self.sort_default_asc = yaml['sort_default_asc']
            if 'data_ordinal' in yaml:
                self.data_ordinal = yaml['data_ordinal']
            if 'export' in yaml:
                self.export = yaml['export']
            if 'options' in yaml:
                self.options = yaml['options']

    def to_v2(self):
        """convert a v1 column object to a v2 column object"""
        c2 = column_v2()
        c2.data   .name = self.name
        c2.data   .type = self.type
        c2.data   .is_array = self.is_array
        c2.data   .has_default = self.has_default
        c2.data   .default_value = self.default
        c2.data   .ordinal = self.data_ordinal
        c2.data   .export = self.export
        c2.data   .regex = ""
        c2.display.name = self.name
        c2.display.ordinal = self.ordinal
        c2.display.visible = self.visible
        c2.display.fixed_width = self.fixed_width
        c2.display.width = self.width
        c2.display.max_width = self.max_width
        c2.display.min_width = self.min_width
        c2.display.overflow = self.overflow
        c2.search .searchable = self.search
        c2.search .multi_search = self.multi_search
        c2.sort   .sortable = self.sort
        c2.sort   .ordinal = self.sort_ordinal
        c2.sort   .default = self.sort_default
        c2.sort   .default_asc = self.sort_default_asc
        return c2
        # not sure what i was doing with options. likely not used.


class column_v2:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        data_yaml = None
        search_yaml = None
        sort_yaml = None
        display_yaml = None

        if None != yaml:
            if 'data' in yaml:
                data_yaml = yaml['data']

            if 'search' in yaml:
                search_yaml = yaml['search']

            if 'sort' in yaml:
                sort_yaml = yaml['sort']

            if 'display' in yaml:
                display_yaml = yaml['display']

        self.data = column_data(yaml=data_yaml)
        self.display = column_display(yaml=display_yaml)
        self.search = column_search(yaml=search_yaml)
        self.sort = column_sort(yaml=sort_yaml)
        self.options = {}


class column_data:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.name = None
        self.type = "string"
        self.is_array = False
        self.has_default = False
        self.default_value = None
        self.ordinal = -1
        self.export = False
        self.regex = None

        if None != yaml:
            if 'name' in yaml:
                self.name = yaml['name']
            if 'type' in yaml:
                self.type = yaml['type']
            if 'is_array' in yaml:
                self.is_array = yaml['is_array']
            if 'has_default' in yaml:
                self.has_default = yaml['has_default']
            if 'default_value' in yaml:
                self.default_value = yaml['default_value']
            if 'ordinal' in yaml:
                self.ordinal = yaml['ordinal']
            if 'export' in yaml:
                self.export = yaml['export']
            if 'regex' in yaml:
                self.regex = yaml['regex']


class column_display:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.name = None
        self.ordinal = -1
        self.visible = True
        self.fixed_width = True
        self.width = 100
        self.max_width = 0
        self.min_width = 0
        self.overflow = False

        if None != yaml:
            if 'name' in yaml:
                self.name = yaml['name']
            if 'ordinal' in yaml:
                self.ordinal = yaml['ordinal']
            if 'visible' in yaml:
                self.visible = yaml['visible']
            if 'fixed_width' in yaml:
                self.fixed_width = yaml['fixed_width']
            if 'width' in yaml:
                self.width = yaml['width']
            if 'max_width' in yaml:
                self.max_width = yaml['max_width']
            if 'min_width' in yaml:
                self.min_width = yaml['min_width']
            if 'overflow' in yaml:
                self.overflow = yaml['overflow']


class column_search:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.searchable = False
        self.multi_search = False

        if None != yaml:
            if 'searchable' in yaml:
                self.searchable = yaml['searchable']
            if 'multi_search' in yaml:
                self.multi_search = yaml['multi_search']


class column_sort:
    def noop(self, *args, **kw):
        pass

    def __init__(self, yaml=None):
        self.sortable = False
        self.ordinal = 0
        self.default = False
        self.default_asc = False

        if None != yaml:
            if 'sortable' in yaml:
                self.sortable = yaml['sortable']
            if 'ordinal' in yaml:
                self.ordinal = yaml['ordinal']
            if 'default' in yaml:
                self.default = yaml['default']
            if 'default_asc' in yaml:
                self.default_asc = yaml['default_asc']

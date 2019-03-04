import argparse
from  os import environ

from .table import table

# table takes the data a s a file stream

def get_envvar(env_var,default=None):
    found=default
    if env_var in environ:
        found=environ['env_var']
    return found


def cli_main():
    parser = argparse.ArgumentParser("flextable", usage='%(prog)s [options]'
                    ,description=
                    """ascii table formatting with flexible columns, and styling
                    """, epilog="And that's how you flextable")

    # TODO
    # parser.add_argument('-ln'     ,'--line-numbers'         , help='show line numbers'                                  ,action='store_true', default=False)
    # parser.add_argument('-ls'     ,'--line-seperators'      , help='use line seperators for each column of data'        ,action='store_true', default=False)

    # data
    parser.add_argument('file' , nargs='?'         , default=get_envvar('FT_FILE'                    ), help='The input file to read'                                   )
    parser.add_argument('-c'   ,'--columns'        , default=get_envvar('FT_COLUMNS'                 ), help='column names'                                             , nargs='+')
    parser.add_argument('-cc'  ,'--column-count'   , default=get_envvar('FT_COLUMN_COUNT'   ,-1      ), help='column count, auto name columns 1-n'                      , type=int)
    parser.add_argument('-hol' ,'--header-on-line' , default=get_envvar('FT_HEADER_ON_LINE' ,-1      ), help='column names the specified line of input'                 , type=int,)
    parser.add_argument('-rq'  ,'--remove-quote'   , default=get_envvar('FT_REMOVE_QUOTE'   ,True    ), help='unwrap fields with block quotes'                          )
    parser.add_argument('-bq'  ,'--block-quote'    , default=get_envvar('FT_BLOCK_QUOTE'    ,None    ), help='field block quote identifier'                             )
    parser.add_argument('-ds'  ,'--data-on-line'   , default=get_envvar('FT_DATA_ON_LINE'   ,1       ), help='data starts on this line'                                 , type=int)
    parser.add_argument('-bs'  ,'--border-style'   , default=get_envvar('FT_BORDER_STYLE'   ,'SINGLE'), help='change table style, single,doubble, ascii'                )
    parser.add_argument('-nft' ,'--no-footer'      , default=get_envvar('FT_NO_FOOTER'      ,True    ), help='dont show the footer'                                     , action='store_false' , dest='footer')
    parser.add_argument('-nhd' ,'--no-header'      , default=get_envvar('FT_NO_HEADER'      ,True    ), help='dont show header'                                         , action='store_false' , dest='header')
    parser.add_argument('-ftc' ,'--footer-columns' , default=get_envvar('FT_FOOTER_COLUMNS' ,True    ), help='footer has column names'                                  , action='store_true'   )
    parser.add_argument('-hde' ,'--header-every'   , default=get_envvar('FT_HEADER_EVERY'   ,-1      ), help='show header every (n) rows'                               , type=int)
    parser.add_argument('-e'   ,'--error'          , default=get_envvar('FT_ERROR'          ,True    ), help='rows with invalid number of columns are considered errors', action='store_true')
    parser.add_argument('-cm'  ,'--comment'        , default=get_envvar('FT_COMMENT'        ,'#'     ), help='character that denotes line is comment, \'#\' default'    )
    parser.add_argument('-d'   ,'--delimiter'      , default=get_envvar('FT_DELIMITER'      ,','     ), help='field delimiter \',\' default'                            )
    parser.add_argument('-he'  ,'--hide-errors'    , default=get_envvar('FT_HIDE_ERRORS'    ,False   ), help='do not display errors'                                    , action='store_true')
    parser.add_argument('-hc'  ,'--hide-comments'  , default=get_envvar('FT_HIDE_COMMENTS'  ,False   ), help='do not display comments'                                  , action='store_true')
    parser.add_argument('-hw'  ,'--hide-whitespace', default=get_envvar('FT_HIDE_WHITESPACE',False   ), help='do not display whitespace'                                , action='store_true')
    parser.add_argument('-l'   ,'--line'           , default=get_envvar('FT_LINE'           ,-1      ), help='line number to start displaying data from in file'        , type=int)
    parser.add_argument('-len' ,'--length'         , default=get_envvar('FT_LENGTH'         ,-1      ), help='number of lines to show, hidden lines do not count'       , type=int)
    parser.add_argument('-p'   ,'--page'           , default=get_envvar('FT_PAGE'           ,-1      ), help='page to start displaying, requires length parameter'      , type=int)
    parser.add_argument('-ow'  ,'--width'          , default=get_envvar('FT_WIDTH'          ,-1      ), help='width of output in characters'                            , type=int, dest='column_width')
    parser.add_argument('-oh'  ,'--height'         , default=get_envvar('FT_HEIGHT'         ,-1      ), help='height of output window in characters'                    , type=int, dest='row_height')
    parser.add_argument('-nc'  ,'--no-color'       , default=get_envvar('FT_NO_COLOR'       ,False   ), help='disale color output'                                      , action='store_true')
    parser.add_argument('-o'   ,'--output'         , default=get_envvar('FT_OUTPUT'         ,'ASCII' ), help='ASCII, YAML, JSON, default=ASCII'                         )
    
    args=parser.parse_args()

    table(args)
    
if __name__ == "__main__":
    cli_main()

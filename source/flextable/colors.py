
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


def colors(foreground,background,dim=None,bold=None):
    color=''
    if dim !=None:
        color+=attributes.DIM
    if bold !=None:
        color+=attributes.BOLD
        
    if None != foreground:
        if foreground.upper() == 'DEFAULT' :
            color+=fg.DEFAULT
        if foreground.upper() == 'BLACK' :
            color+=fg.BLACK
        if foreground.upper() == 'RED' :
            color+=fg.RED
        if foreground.upper() == 'GREEN' :
            color+=fg.GREEN
        if foreground.upper() == 'YELLOW' :
            color+=fg.YELLOW
        if foreground.upper() == 'BLUE' :
            color+=fg.BLUE
        if foreground.upper() == 'MAGENTA' :
            color+=fg.MAGENTA
        if foreground.upper() == 'CYAN' :
            color+=fg.CYAN
        if foreground.upper() == 'LIGHT GRAY' :
            color+=fg.LIGHT_GRAY
        if foreground.upper() == 'DARK GRAY' :
            color+=fg.DARK_GRAY
        if foreground.upper() == 'LIGHT RED' :
            color+=fg.LIGHT_RED
        if foreground.upper() == 'LIGHT GREEN' :
            color+=fg.LIGHT_GREEN
        if foreground.upper() == 'LIGHT YELLOW' :
            color+=fg.LIGHT_YELLOW
        if foreground.upper() == 'LIGHT BLUE' :
            color+=fg.LIGHT_BLUE
        if foreground.upper() == 'LIGHT MAGENTA' :
            color+=fg.LIGHT_MAGENTA
        if foreground.upper() == 'LIGHT CYAN' :
            color+=fg.LIGHT_CYAN
        if foreground.upper() == 'WHITE' :
            color+=fg.WHITE
    if None != background:
        if  background.upper() == 'DEFAULT' :
            color+=bg.DEFAULT
        if  background.upper() == 'BLACK' :
            color+=bg.BLACK
        if  background.upper() == 'RED' :
            color+=bg.RED
        if  background.upper() == 'GREEN' :
            color+=bg.GREEN
        if  background.upper() == 'YELLOW' :
            color+=bg.YELLOW
        if  background.upper() == 'BLUE' :
            color+=bg.BLUE
        if  background.upper() == 'MAGENTA' :
            color+=bg.MAGENTA
        if  background.upper() == 'CYAN' :
            color+=bg.CYAN
        if  background.upper() == 'LIGHT GRAY' :
            color+=bg.LIGHT_GRAY
        if  background.upper() == 'DARK GRAY' :
            color+=bg.DARK_GRAY
        if  background.upper() == 'LIGHT RED' :
            color+=bg.LIGHT_RED
        if  background.upper() == 'LIGHT GREEN' :
            color+=bg.LIGHT_GREEN
        if  background.upper() == 'LIGHT YELLOW' :
            color+=bg.LIGHT_YELLOW
        if  background.upper() == 'LIGHT BLUE' :
            color+=bg.LIGHT_BLUE
        if  background.upper() == 'LIGHT MAGENTA' :
            color+=bg.LIGHT_MAGENTA
        if  background.upper() == 'LIGHT CYAN' :
            color+=bg.LIGHT_CYAN
        if  background.upper() == 'WHITE' :
            color+=bg.WHITE
    return color



    

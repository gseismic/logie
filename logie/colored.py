#/usr/bin/python
#-*- coding: utf-8 -*-
#   格式：\033[显示方式;前景色;背景色m
#   说明:
#
#   前景色            背景色            颜色
#   ---------------------------------------
#     30                40              黑色
#     31                41              红色
#     32                42              绿色
#     33                43              黃色
#     34                44              蓝色
#     35                45              紫红色
#     36                46              青蓝色
#     37                47              白色
#
#   显示方式           意义
#   -------------------------
#      0           终端默认设置
#      1             高亮显示
#      4            使用下划线
#      5              闪烁
#      7             反白显示
#      8              不可见
#
#   例子：
#   \033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
#   \033[0m          <!--采用终端默认设置，即取消颜色设置-->]]]
# ref: http://www.w2bc.com/Article/39141


STYLE = {
        'fore':
        {   # 前景色
            'black'    : 30,   #  黑色
            'red'      : 31,   #  红色
            'green'    : 32,   #  绿色
            'yellow'   : 33,   #  黄色
            'blue'     : 34,   #  蓝色
            'purple'   : 35,   #  紫红色
            'cyan'     : 36,   #  青蓝色
            'white'    : 37,   #  白色
        },

        'back' :
        {   # 背景
            'black'     : 40,  #  黑色
            'red'       : 41,  #  红色
            'green'     : 42,  #  绿色
            'yellow'    : 43,  #  黄色
            'blue'      : 44,  #  蓝色
            'purple'    : 45,  #  紫红色
            'cyan'      : 46,  #  青蓝色
            'white'     : 47,  #  白色
        },

        'style' :
        {   # 显示模式
            'mormal'    : 0,   #  终端默认设置
            'bold'      : 1,   #  高亮显示
            'underline' : 4,   #  使用下划线
            'blink'     : 5,   #  闪烁
            'invert'    : 7,   #  反白显示
            'hide'      : 8,   #  不可见
        },

        'default' :
        {
            'end' : 0,
        },
}


def colored(string, style = '', fore = '', back = ''):
    style  = '%s' % STYLE['style'][style] if style in STYLE['style'] else ''
    fore  = '%s' % STYLE['fore'][fore] if fore in STYLE['fore'] else ''
    back  = '%s' % STYLE['back'][back] if back in STYLE['back'] else ''
    style = ';'.join([s for s in [style, fore, back] if s])
    style = '\033[%sm' % style if style else ''
    end   = '\033[%sm' % STYLE['default']['end'] if style else ''
    return '%s%s%s' % (style, string, end)


def TestColor():
    print(colored('正常显示'))
    print('')

    print("测试显示模式")
    print(colored('高亮',   style = 'bold'))
    print(colored('下划线', style = 'underline'))
    print(colored('闪烁',   style = 'blink'))
    print(colored('反白',   style = 'invert'))
    print(colored('不可见', style = 'hide'))


    print("测试前景色")
    print(colored('黑色',   fore = 'black'))
    print(colored('红色',   fore = 'red'))
    print(colored('绿色',   fore = 'green'))
    print(colored('黄色',   fore = 'yellow'))
    print(colored('蓝色',   fore = 'blue'))
    print(colored('紫红色', fore = 'purple'))
    print(colored('青蓝色', fore = 'cyan'))
    print(colored('白色',   fore = 'white'))


    print("测试背景色")
    print(colored('黑色',   back = 'black'))
    print(colored('红色',   back = 'red'))
    print(colored('绿色',   back = 'green'))
    print(colored('黄色',   back = 'yellow'))
    print(colored('蓝色',   back = 'blue'))
    print(colored('紫红色', back = 'purple'))
    print(colored('青蓝色', back = 'cyan'))
    print(colored('白色',   back = 'white'))


if __name__ == '__main__':
    TestColor( )

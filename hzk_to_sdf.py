import fontforge
import binascii

KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

def Draw(font, ch, rect_list):

    gb2312 = ch.encode('gb2312')
    hex_str = binascii.b2a_hex(gb2312)
    result = str(hex_str, encoding='utf-8')
    area = eval('0x' + result[:2]) - 0x80
    index = eval('0x' + result[2:]) - 0x80

    ioj = (area << 8) + index
    # print(ch, gb2312, hex_str, result, ioj)

    glyph = font.createMappedChar(ioj)
    pen = glyph.glyphPen()

    y = 11
    max_x = 0
    for row in rect_list:
        y = y - 1
        x = -1
        for i in row:
            x = x + 1
            if i:
                pen.moveTo((100 * x , 100 * y ))
                pen.lineTo((100 * x , 100 * y + 100))
                pen.lineTo((100 * x + 100 , 100 * y + 100))
                pen.lineTo((100 * x + 100 , 100 * y ))
                pen.closePath()
                max_x = max(max_x,x)
                # print("#")
            # else:
                # print(" ")
        # print("\n")
       
    pen = None
    glyph.removeOverlap()
    glyph.width = max_x*100 + 200

def draw_glyph(ch):
    rect_list = [] * 12
    for i in range(12):
        rect_list.append([] * 16)

    # 获取中文的gb2312编码，一个汉字是由2个字节编码组成
    gb2312 = ch.encode('gb2312')
    # 将二进制编码数据转化为十六进制数据
    hex_str = binascii.b2a_hex(gb2312)
    # 将数据按unicode转化为字符串
    result = str(hex_str, encoding='utf-8')
    # 前两位对应汉字的第一个字节：区码，每一区记录94个字符
    area = eval('0x' + result[:2]) - 0xA0
    # 后两位对应汉字的第二个字节：位码，是汉字在其区的位置
    index = eval('0x' + result[2:]) - 0xA0
    # 汉字在HZK16中的绝对偏移位置，最后乘24是因为字库中的每个汉字字模都需要24字节
    offset = (94 * (area-1) + (index-1)) * 24
    font_rect = None
    # 读取HZK16汉字库文件
    with open("C:/Users/op/Downloads/HZK/HZK12", "rb") as f:
        # 找到目标汉字的偏移位置
        f.seek(offset)
        # 从该字模数据中读取24字节数据
        font_rect = f.read(24)

    # font_rect的长度是24，此处相当于for k in range(16)
    for k in range(len(font_rect) // 2):
        # 每行数据
        row_list = rect_list[k]
        for j in range(2):
            for i in range(8):
                asc = font_rect[k * 2 + j]
                # 此处&为Python中的按位与运算符
                flag = asc & KEYS[i]
                # 数据规则获取字模中数据添加到16行每行中16个位置处每个位置
                row_list.append(flag)

    return rect_list

def OpenGBK():
    f = open("C:/Users/op/Downloads/HZK/gb2312.txt", 'r', encoding='UTF-8')
    line = f.readline()

    for index, ch in enumerate(line):
        if ch == "\n":
            continue

        print(index, end=' ')
        print(ch)

    f.close()


sdf_path = "C:/Users/op/Downloads/HZK/HZK12.sfd"


def Start():

    font = fontforge.open(sdf_path)  # Open a font
    font.encoding = "gb2312"
    
    f = open("C:/Users/op/Downloads/HZK/gb2312.txt", 'r', encoding='UTF-8')
    
    line = f.readline()

    while line:
        for index, ch in enumerate(line):
            if ch == "\n":
                continue
            print(ch)
            rect = draw_glyph(ch)
            Draw(font, ch, rect)
        line = f.readline()

    font.save()
    f.close()

# OpenGBK():
Start()


#ffpython C:\Users\op\Downloads\HZK\font.py
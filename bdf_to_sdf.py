from bdflib import reader
from bdflib import writer
import fontforge

def OpenBDF(path):
    with open(path, "rb") as handle:
        return reader.read_bdf(handle)

def Start():

    bdf_font = OpenBDF("C:/Users/op/Downloads/HZK/mplus_jf12r.bdf")
    sdf_font = fontforge.open("C:/Users/op/Downloads/HZK/mplus_jf12r.sfd")

    for bdf_glyph in bdf_font.glyphs:
        # bdf_glyph = bdf_font[12321]
        x = -1
        y = 10

        print(bdf_glyph.codepoint)
        glyph = sdf_font.createMappedChar(bdf_glyph.codepoint)
        pen = glyph.glyphPen()

        for ch in bdf_glyph.__str__():
            if ch == '\n':
                y = y - 1
                x = -1
                print("")

            if ch == '#' :
                pen.moveTo((100 * x , 100 * y ))
                pen.lineTo((100 * x , 100 * y + 100))
                pen.lineTo((100 * x + 100 , 100 * y + 100))
                pen.lineTo((100 * x + 100 , 100 * y ))
                pen.closePath()
                print("#",end=" ")
            else:
                print(" ",end=" ")
            x = x + 1

        pen = None
        glyph.removeOverlap()

        # break
    
    sdf_font.save()

Start()
# not worth doing xml parsing... pls no injection ;)
#import xml.etree.ElementTree as ET
import html
import base64
import argparse
import subprocess
import os

FONTFORGE_PATH = '/usr/bin/fontforge'

FONT_NAME = 'hax'
WIDTH = 10000
UNITS_PER_EM = 1000

def gen_ligature(prefix, chrs=[]):
    
    # all empty characters
    empty = [f"<glyph unicode='{html.escape(chr(c))}' horiz-adv-x='0' d='M1 0z'/>" for c in range(0x20, 0x7e)]
    
    # ligatures to be made
    ligs = [f"<glyph unicode='{prefix}{html.escape(c)}' horiz-adv-x='{WIDTH}' d='M1 0z'/>" for c in chrs]
    
    # its ugly but it works :p
    return f'''<?xml version='1.0'?>
<svg>
<defs>
<font id='{FONT_NAME}' horiz-adv-x='0'>
<font-face units-per-em='{UNITS_PER_EM}'/>
{chr(10).join(empty)}
{chr(10).join(ligs)}
</font>
</defs>
</svg>'''

def make_woff(svg, filename):
    f = open('tmp.svg', 'w')
    f.write(svg)
    f.close()

    try:
        subprocess.run([FONTFORGE_PATH, 'script.fontforge', 'tmp.svg', filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove('tmp.svg')
        return True
    except:
        os.remove('tmp.svg')
        return False

def make_b64_woff(prefix, chrs=[]):
    svg = gen_ligature(prefix, chrs)
    make_woff(svg, 'tmp.woff')
    f = open('tmp.woff', 'rb')
    out = base64.b64encode(f.read()).decode()
    f.close()
    os.remove('tmp.woff')
    return out

def main():

    parser = argparse.ArgumentParser(description='creates a ligature font pack from input')
    parser.add_argument('chars', metavar='C', type=str, nargs='*', help='list chars for ligature')
    parser.add_argument('--prefix', '-p', default='', help='ligature prefix (default none)')
    parser.add_argument('--file', '-f', default='font.woff', help='output file for font (default ./font.woff)')
    parser.add_argument('--delete', '-d', action='store_true', help='do not create .woff file')
    parser.add_argument('--xml', '-x', action='store_true', help='print as xml instead of creating font')
    parser.add_argument('--base64', '-b64', action='store_true', help='print as base64 encoded woff instead of creating font')
    
    parser.add_argument('--name', '-n', help='font name (default "hax")')
    parser.add_argument('--width', '-w', help='font width in em (default 10000)')
    parser.add_argument('--units', '-u', help='font units per em (default 1000)')

    args = parser.parse_args()
    if args.name:
        FONT_NAME = args.name

    if args.width:
        WIDTH = args.width

    if args.units:
        UNITS_PER_EM = args.units


    xml = gen_ligature(args.prefix, args.chars)

    if args.xml:
        print(xml)

    # no need to error out if fontforge isn't installed
    if not args.base64 or args.delete:
        exit(0)

    if not make_woff(xml, args.file):
        print(f'Error: FontForge not found at {FONTFORGE_PATH}')
        exit(1)

    if args.base64:
        f = open(args.file, 'rb')
        print(base64.b64encode(f.read()).decode())
        if args.delete:
            os.remove(args.file)


if __name__ == "__main__":
    main()
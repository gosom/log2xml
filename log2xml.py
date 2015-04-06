#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import xml.etree.cElementTree as ET
import re

# REgex from: http://www.ibm.com/developerworks/library/wa-apachelogs/
COMBINED_LOGLINE_PAT = re.compile(
    r'(?P<origin>\d+\.\d+\.\d+\.\d+) '
    + r'(?P<identd>-|\w*) (?P<auth>-|\w*) '
    + r'\[(?P<date>[^\[\]:]+):(?P<time>\d+:\d+:\d+) (?P<tz>[\-\+]?\d\d\d\d)\] '
    + r'"(?P<method>\w+) (?P<path>[\S]+) (?P<protocol>[^"]+)" (?P<status>\d+) (?P<bytes>-|\d+)'
    + r'( (?P<referrer>"[^"]*")( (?P<client>"[^"]*")( (?P<cookie>"[^"]*"))?)?)?\s*\Z'
    )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help='Input file. Default stdin')
    parser.add_argument('output', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout, help='Output file. Default stdout')
    return parser.parse_args()


def parse_line(l):
    match_info = COMBINED_LOGLINE_PAT.match(l)
    if match_info:
        return dict(match_info.groupdict())
    return {}


def main():
    args = parse_args()
    root = ET.Element("logfile")
    for l in args.input:
        if l:
            data = parse_line(l)
            for key, value in data.iteritems():
                item = ET.SubElement(root, "item")
                ET.SubElement(item, "field", name=key).text = value
    tree = ET.ElementTree(root)
    tree.write(args.output, encoding='utf-8')


if __name__ == '__main__':
    main()
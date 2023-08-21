import sys
import re

def main():
    help_re = re.compile(r"^([a-zA-Zi_-]*:).*?##(.*)$")

    modules = sys.argv
    del modules[0]
    for m in modules:
        fin = open(m,'r')
        lines = fin.readlines()
        for l in lines:
            m = help_re.match(l)
            if m:
                item = m.group(1).strip()
                defn = m.group(2).strip()
                print("%-20s %s" %(item,defn))

main()

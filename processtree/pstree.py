#!/usr/bin/env python


l = [
    {'child': ['B', 'C', 'E'], 'name': 10, 'pid': 'A'},
    {'child': [], 'name': 11, 'pid': 'B'},
    {'child': ['D'], 'name': 12, 'pid': 'C'},
    {'child': [], 'name': 13, 'pid': 'D'},
    {'child': [], 'name': 14, 'pid': 'E'},
    {'child': ['G'], 'name': 15, 'pid': 'F'},
    {'child': ['H'], 'name': 16, 'pid': 'G'},
    {'child': [], 'name': 17, 'pid': 'H'},
    {'child': [], 'name': 19, 'pid': 'J'},
    {'child': [], 'name': 20, 'pid': 'K'},
    {'child': ['J', 'K'], 'name': 18, 'pid': 'I'},
    ]
    
def displayprocess(pid = 0, level = 0):
    for p in l:
        if (p['pid'] == pid):
            l.remove(p)
            print " "*level + p['pid']
            if (p['child'] != []):               
                for c in p['child']:
                    displayprocess(c, level+1)
        
    
while (len(l) > 0):
    displayprocess(l[0]['pid'])

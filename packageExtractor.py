#!/usr/bin/env python

'''A small script designed to help keep track of which packages are
being used in a LaTex project - AGB 16/09/11'''

import sys, subprocess as sub

if len(sys.argv)<2:
    print 'No input tex.log file to parse. Quittting'
    sys.exit(1)

log_file = open(sys.argv[1], 'r')

packages = []
p = False
for line in log_file.readlines():
    if line.strip() == "*File List*":
        p = True
        continue
    if line.strip() == "***********":
        p = False
    if p:
        packages.append(line.split()[0].strip())

# print packages

out_packs = [pack for pack in packages if (pack.split('.')[-1]=='cls' or pack.split('.')[-1]=='sty')]

# print out_packs
pack_files=[]
for p in out_packs:
    proc = sub.Popen(['kpsewhich', p], stdout=sub.PIPE, stderr=sub.PIPE)
    pack_files.append(proc.communicate()[0].strip('\n'))
print pack_files


rsync = raw_input('rsync these files to current directory(y/n)? ')
if rsync == 'y':
    for p in pack_files:
        sub.call(['rsync', '--progress' ,'-v',p,'.'])


print 'Done.'

mymap1 = {'linker':['boop']}

mymap1 = mymap1.get('compiler', {})

if mymap1:
    print "i exist"
else:
    print "no exisiting for me"
x = input()
y = input()
list1 = list(x.split(" "))
for xx in range(0,len(list1)):
    list1[xx]=int(list1[xx])
list2 = list(y.split(" "))
for yy in range(0,len(list1)):
    list2[yy]=int(list2[yy])
x1 = list1[0]
y1 = list1[1]
x2 = list1[2]
y2 = list1[3]
x3 = list2[0]
y3 = list2[1]
x4 = list2[2]
y4 = list2[3]
possiblex = [x4-x1, x2-x3, x2-x1, x4-x3]
possibley = [y4-y1, y2-y3, y2-y1, y4-y3]
maxx = 0
for xxx in possiblex:
    if xxx > maxx:
        maxx = xxx
maxy = 0
for yyy in possibley:
    if yyy > maxy:
        maxy = yyy
if maxx > maxy:
    print(maxx**2)
else:
    print(maxy**2)

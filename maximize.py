# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys
import itertools
import functools


def max (elements , expected_result): 
    elements = elements.splitlines()
    K, M = elements.pop(0).split(' ')

    elements = [[int(x) for x in e.split(' ')] for e in elements]
    num_elements = [e.pop(0) for e in elements]
    
    res = 0

    print("M: ", M)

    for e in itertools.product(*elements):
        acum = functools.reduce(lambda x, y: pow(x,2) + pow(y,2), e) % int(M)
        res = res if acum < res else acum
        # print("Res: ", res, "Acum: ", acum)


    print ("PASS\n" if res == expected_result else "FAIL\n", "result: ", res, "expected_result: ", expected_result, '\n\n')



ev = 974

el ="""3 998
6 67828645 425092764 242723908 669696211 501122842 438815206
4 625649397 295060482 262686951 815352670
3 100876777 196900030 523615865"""

max(el, ev)

ev = 0

el = """2 24
3 24 48 96
4 24 48 96 24"""

max(el, ev)


ev = 943

el = """7 952
6 386364143 56297585 479292050 782778989 177771725 945191156
7 458982242 957774948 25202756 357554307 248513713 506622954 769577156
3 109432676 494972174 914814315
1 49979276
2 491584479 103564062
1 25883738
1 460971693"""

max(el, ev)

ev = 763

el = """6 767
2 488512261 423332742
2 625040505 443232774
1 4553600
4 92134264 617699202 124100179 337650738
2 778493847 932097163
5 489894997 496724555 693361712 935903331 518538304"""

max(el, ev)

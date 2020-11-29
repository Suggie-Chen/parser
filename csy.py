FIRST = {}
FOLLOW = {}

global buffer

sentences = [
'E->TG',
'G->+TG',
'G->-TG',
'G->ε',
'T->FS',
'S->*FS',
'S->/FS',
'S->ε',
'F->(E)',
'F->i',]

N={'E','G','T','S','F'}
T={'+','-','*','/','ε','i','(',')'}

def isN(c):
    if c in N:
        return True
    else:
        return False

def isT(c):
    if c in T or c.isdigit():
        return True
    else:
        return False

#初始化 first 集 和follow集合字典的键值对中的 值 为空
def init():
    for str  in sentences :
        part_begin = str.split("->")[0]
        part_end = str.split("->")[1]
        FIRST[part_begin] = set()
        FOLLOW[part_begin] = set()
    FOLLOW['E'].add('$')#'#将$加入起始符的FOLLOW集中

def f(c):
    if isN(c):
        # print("FIRST[c]",FIRST[c])
        return FIRST[c];
    else:
        s=set()
        s.add(c)
        return s;

def error():
    print("error")

#求一个字符串的FIRST集
def ff(s):

    first=set()

    temp=set()
    temp = temp|f(s[0])
    temp.discard('ε')
    first = first | temp

    i = 1

    while ('ε' in f(s[i - 1])) and i < len(s):
        t=set()
        t = t|FIRST[s[i]]
        t.discard('ε')
        first = first | t
        i += 1
    if i == len(s) and 'ε' in f(s[i - 1]):
        first.add('ε')
    # print("FIRST(s)=",first)
    return first



def getFirst():
    # X->a X->ε
    def getFirst_1():
        while (1):
            test = FIRST
            for str in sentences:
                part_begin = str.split("->")[0]
                part_end = str.split("->")[1]
                if not part_end[0].isupper():  # ->号右边的第一个字符是终结符
                    FIRST[part_begin].add(part_end[0])
            if (test == FIRST):
                break;
        # print(FIRST)

    ##求first第二部分 针对 A -> B..型
    def getFirst_2():
        for str in sentences:
            part_begin = str.split('->')[0]
            part_end = str.split('->')[1]
            ##如果型如A ->B 则把B的first集加到A 的first集中去
            if isN(part_end[0]):  # ->右边第一符号是非终结符
                if len(part_end) == 1:  # ->右边只有一个符号，就是非终结符
                    FIRST[part_begin] = FIRST[part_begin] | FIRST[part_end[0]]
                else:
                    temp = set()
                    temp = temp | FIRST[part_end[0]]
                    temp.discard('ε')
                    FIRST[part_begin] = FIRST[part_begin] | temp

                    i = 1
                    while ('ε' in f(part_end[i - 1])) and i < len(part_end):
                        t = set()
                        t = t | FIRST[part_end[i]]
                        t.discard('ε')
                        FIRST[part_begin] = FIRST[part_begin] | t
                        i += 1
                    if i == len(part_end) and 'ε' in f(part_end[i - 1]):
                        FIRST[part_begin].add('ε')

    getFirst_1()

    getFirst_2()
    while(1):
        test = FIRST
        getFirst_2()
        if test == FIRST:
            break
    print("FIRST=",FIRST)

def getFOLLOW():
    def getFollow_1():
        for str in sentences:
            part_begin = str.split("->")[0]
            part_end = str.split("->")[1]
            for i in range(len(part_end)):
                e = part_end[i]
                if isN(e):  # 是非终结符
                    if i != len(part_end) - 1:  # 不是->右边最后一个A->aBβ
                        # temp为β的first集
                        temp = set()
                        temp = temp | ff(part_end[i + 1:])
                        if 'ε' in temp:
                            FOLLOW[e] = FOLLOW[e] | FOLLOW[part_begin]
                        # else:
                        temp.discard('ε')
                        FOLLOW[e] = FOLLOW[e] | temp
                    else:  # 是右边最后一个 A->aB
                        FOLLOW[e] = FOLLOW[e] | FOLLOW[part_begin]

    getFollow_1()
    while(1):
        test = FOLLOW
        getFollow_1()
        if test == FOLLOW:
            break
    print("FOLLOW=",FOLLOW)





def RecurCallPrediAnalysis():
    global buffer
    turn=[]
    p = 0
    # buffer = '6/3+(1-2)*5'
    length = len(buffer)

    def procE():
        nonlocal p, turn, length

        turn.append([])
        i = len(turn)
        turn[i - 1].append("E->")

        procT()
        turn[i - 1].append("T")

        if buffer[p] == '+' or buffer[p] == '-':
            turn[i - 1].append(buffer[p])
            if p == length - 1:
                return
            p = p + 1

            procE()
            turn[i - 1].append("E")
        return

    def procT():
        nonlocal p, turn, length

        turn.append([])
        i = len(turn)
        turn[i - 1].append("T->")

        procF()
        turn[i - 1].append("F")
        if buffer[p] == '*' or buffer[p] == '/':
            turn[i - 1].append(buffer[p])
            if p == length - 1:
                return
            p = p + 1

            procT()
            turn[i - 1].append("T")
        return

    def procF():
        nonlocal p, turn, length

        turn.append([])
        i = len(turn)
        turn[i - 1].append("F->")

        if buffer[p] == '(':
            turn[i - 1].append("(")
            if p == length - 1:
                return
            p = p + 1

            turn[i - 1].append("E")
            procE()
            if buffer[p] == ')':
                turn[i - 1].append(")")
                if p == length - 1:
                    return
                p = p + 1

            else:
                error()
        elif buffer[p].isdigit():
            turn[i - 1].append(buffer[p])
            if p == length - 1:
                return
            p = p + 1

        else:
            error()
        return


    print("递归调用预测分析：")
    procE()
    for i in range(len(turn)):
        turn[i]="".join(turn[i])
    print(turn)


def LL1():
    global buffer

    print("LL(1)预测分析：")
    init()
    getFirst()
    getFOLLOW()
    table = dict()

    def formTable():
        # 初始化预测分析表
        nonlocal table
        for n in N:
            temp=dict()
            for t in T:
                temp.setdefault(t,'')
            table.setdefault(n,temp)
        print("table=")

        #构造预测分析表
        for each in sentences:
            left=each.split("->")[0]
            right=each.split("->")[1]
            for t in ff(right):
                table[left][t]=each
            if 'ε'in ff(right):
                for b in FOLLOW[left]:
                    table[left][b]=each
        for i in N:
            print("{}:".format(i),table[i])

    # 构造预测分析程序
    def analyze():
        stack=['$','E']#列表尾是栈顶
        buf=buffer+'$'
        p=0 #输入指针
        while 1:

            X=stack[-1]
            a=buf[p]
            if isT(X) or X=='$':
                if(a.isdigit()):
                    a='i'
                if X==a :
                    stack.pop()
                    p=p+1
                else:
                    # error()
                    print("error1")
            else:#X是非终结符
                if a.isdigit():
                    a='i'
                sen=table[X][a]
                if sen!='':#查表发现相应位置不为空
                    string=sen.split("->")[1]
                    if string=='ε':
                        stack.pop()
                    else:
                        rev=string[::-1]
                        stack.pop()
                        stack.extend(list(rev))
                    print(sen)
                else:
                    # error()
                    print("error2")
            print("stack=", stack)
            if X=='$':
                break

    formTable()
    analyze()



buffer='6/3+(1-2)*5'#待分析的字符串
RecurCallPrediAnalysis()
LL1()


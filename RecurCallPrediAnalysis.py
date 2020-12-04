def RecurCallPrediAnalysis():
    global buffer
    turn=[]
    p = 0
    # buffer = '6/3+(1-2)*5'
    length = len(buffer)

    def error():
        print("error")

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

buffer='6/3+(1-2)*5'#待分析的字符串
RecurCallPrediAnalysis()
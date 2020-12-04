def LR0():
    regulations=["E->E+T",
	"E->E-T",
	"E->T",
    "F->(E)",
	"F->n",
	"T->T*F",
	"T->T/F",
	"T->F",
	]

    N={'E','F','T'}
    T={'+','-','*','/','n','(',')'}

    # s = '6/3+(1-2)*5'  # 待分析的字符串
    s="3/(1+9)*1/2"
    action=[]
    goto=[]

    def formTable():
        #init table
        for i in range(16):
            temp1 = dict()
            for t in T:
                temp1.setdefault(t, '')
            temp1.setdefault('$','')
            action.append(temp1)

            temp2=dict()
            for n in N:
                temp2.setdefault(n,'')
            goto.append(temp2)
        action[0]['(']="s4"
        action[0]['n']="s5"
        action[1]['$']='acc'
        action[1]['+']='s6'
        action[1]['-']='s7'
        action[2]['$']='r3'
        action[2][')']='r3'
        action[2]['*']='s8'
        action[2]['+']='r3'
        action[2]['-']='r3'
        action[2]['/']='s9'
        action[3]['$'] = 'r8'
        action[3][')'] = 'r8'
        action[3]['*'] = 'r8'
        action[3]['+'] = 'r8'
        action[3]['-'] = 'r8'
        action[3]['/'] = 'r8'
        action[4]['('] = 's4'
        action[4]['n'] = 's5'
        action[5]['$'] = 'r5'
        action[5][')'] = 'r5'
        action[5]['*'] = 'r5'
        action[5]['+'] = 'r5'
        action[5]['-'] = 'r5'
        action[5]['/'] = 'r5'
        action[6]['('] = 's4'
        action[6]['n'] = 's5'
        action[7]['('] = 's4'
        action[7]['n'] = 's5'
        action[8]['('] = 's4'
        action[8]['n'] = 's5'
        action[9]['('] = 's4'
        action[9]['n'] = 's5'
        action[10][')']='s15'
        action[10]['+']='s6'
        action[10]['-']= 's7'
        action[11]['$']='r1'
        action[11][')']='r1'
        action[11]['*']='s8'
        action[11]['+']='r1'
        action[11]['-']='r1'
        action[11]['/']='s9'
        action[12]['$'] = 'r2'
        action[12][')'] = 'r2'
        action[12]['*'] = 's8'
        action[12]['+'] = 'r2'
        action[12]['-'] = 'r2'
        action[12]['/'] = 's9'
        action[13]['$'] = 'r6'
        action[13][')'] = 'r6'
        action[13]['*'] = 'r6'
        action[13]['+'] = 'r6'
        action[13]['-'] = 'r6'
        action[13]['/'] = 'r6'
        action[14]['$'] = 'r7'
        action[14][')'] = 'r7'
        action[14]['*'] = 'r7'
        action[14]['+'] = 'r7'
        action[14]['-'] = 'r7'
        action[14]['/'] = 'r7'
        action[15]['$'] = 'r4'
        action[15][')'] = 'r4'
        action[15]['*'] = 'r4'
        action[15]['+'] = 'r4'
        action[15]['-'] = 'r4'
        action[15]['/'] = 'r4'


        goto[0]['E']=1
        goto[0]['F']=3
        goto[0]['T']=2
        goto[4]['E']=10
        goto[4]['F']=3
        goto[4]['T'] =2
        goto[6]['F'] = 3
        goto[6]['T'] = 11
        goto[7]['F'] = 3
        goto[7]['T'] = 12
        goto[8]['F'] = 13
        goto[9]['F'] = 14
        print(action)
        print(goto)


    formTable()


    stateStack=[]
    symbleStack=[]
    e=[]#有两个元素，第一个表示state,第二个表示symble
    buffer=s+'$'
    stateStack.append(0)
    symbleStack.append('')
    p=0

    while(1):
        S=stateStack[-1]
        a=buffer[p]
        # print(S)

        if(a.isdigit()):
            a='n'
        # print(a)
        if action[S][a].startswith('s'):
            num=int(action[S][a][1::])
            symbleStack.append(a)
            stateStack.append(num)
            p=p+1
        elif action[S][a].startswith('r'):
            value=action[S][a]
            index=int(value[1::])-1
            left=regulations[index].split("->")[0]
            right=regulations[index].split("->")[1]
            for i in range(len(right)):
                stateStack.pop()
                symbleStack.pop()
            S=stateStack[-1]
            symbleStack.append(left)
            stateStack.append(goto[S][left])
            print(regulations[index])
        elif action[S][a]=='acc':
            return
        else:
            print("error!")
        print(stateStack)
        print(symbleStack)

LR0()
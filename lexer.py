alph = ['_','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
kws = 'def,for,while,if'.split(',')
ops = '+,-,/,//,*,%,^'.split(',')
sps = ',*;*:'.split('*')
aops = '=,*=,/=,//=,%=,+=,-=,^='.split(',')
cops = '<,>,==,!=,<=,>='.split(',')
commentator = '#'

maths = ['^', '/', '*', '-', '+', '%', '<', '>', '=', '(', ')', '.', ',']
finders = '+,-,*,/,%,^,<,>,=,!'.split(',')
brs = '(,),[,],{,}'.split(',')

MATCH_UP = {'+':'[ADD]',
            '-':'[SUBSTR]',
            '/':'[DIV]',
            '//':'[LONG_DIV]',
            '*':'[MUL]',
            '%':'[MOD]',
            '^':'[POW]',
            ',':'[ARG_SEP]',
            '.':'[FLOAT_SEP]',
            ';':'[LINE_SEP]',
            ':':'[DEF_SEP]',
            '=':'[AOP]',
            '*=':'[MUL_AOP]',
            '/=':'[DIV_AOP]',
            '//=':'[LONG_DIV_AOP]',
            '%=':'[MOD_AOP]',
            '+=':'[ADD_AOP]',
            '-=':'[SUBSTR_AOP]',
            '^=':'[POW_AOP]',
            '<':'[LE_THAN]',
            '>':'[GR_THAN]',
            '==':'[EQ]',
            '!=':'[NOT_EQ]',
            '<=':'[LE_THAN_OR_EQ]',
            '>=':'[GR_THAN_OR_EQ]',
            'int':'[DEF_INT]',
            'float':'[DEF_FLOAT]',
            'string':'[DEF_STR]',
            'char':'[DEF_CHAR]',
            '(':'[LB_N]',
            ')':'[RB_N]',
            '[':'[LB_C]',
            ']':'[RB_C]',
            '{':'[LB_S]',
            '}':'[RB_S]'}

MATCH_DATA = {'[VAR_NAME]',
              '[FUNC_NAME]',
              '[FUNC_CALL]',}


def all_oper(string):
    ret = ''
    all_ = []
    c = 0
    for i in string:
        if i in finders:
            c = 1
            ret += i
        else:
            if c == 1:
                all_.append(ret)
                ret = ''
            c = 0
    return all_  

def errors(string):
    join = ops+aops+cops
    opers = all_oper(string)
    for i in opers:
        if not i in join:
            return 'Illegal Operand : "{}"'.format(i)
    if string.count("(") != string.count(")"):
        return "Mismatched Brackets"
    br = 0
    ls = len(string)
    for j in range(ls):
        i = string[j]
        if not (i in alph or i in maths or i.isnumeric()):
            return "Illegal Use of Characters : "+i
        if j > 0:
            pre = string[j-1]
        if j < ls-1:
            pos = string[j+1]
        if br < 0:
            return "Mismatched Brackets"
        if i == "(":
            br += 1
            if j > 0:
                if pre.isnumeric():
                    return "Incorrect Syntax"
        elif i == ")":
            br -= 1
            if j < ls-1:
                if pos.isnumeric():
                    return "Incorrect Syntax"
    if br != 0:
        return "Mismatched Brackets"

def prim_br(string):
    inds = []
    br = 0
    rev = 0
    for i in range(len(string)):
        rev = 0
        if string[i] == "(":
            br += 1
            if br == 1 and rev == 0:
                rev = 1
        elif string[i] == ")":
            br -= 1
            rev = 0
        if br == 1 and rev == 1:
            inds.append(i)
    return inds

def find(string):
    con = []
    fun = []
    seq = ""
    tog = 0
    for i in range(len(string)):
        c = string[i]
        if c in alph or c.lower() in alph:
            tog = 1
            seq += c
        else:
            if tog:
                acs = 1
                try:
                    if c == "(":
                        acs = 0
                except:
                    pass
                if acs:
                    if not seq in con:
                        con.append(seq)
                else:
                    if not seq in fun:
                        fun.append(seq)
                seq = ""
                tog = 0
    if seq!="":
        if not seq in con:
            con.append(seq)
    return con,fun

def get_op(string,index):
    try:
        if string[index] != "(":
            return False
    except:
        return False
    br = 0
    string = string[index:len(string)]
    for i in range(len(string)):
        if string[i] == "(":
            br += 1
        if string[i] == ")":
            br -= 1
        if br == 0:
            break
    return string[0:i+1]

def depthof(array):
    atypes=[tuple,list,set]
    max_ = 0
    for i in array:
        if type(i) in atypes:
            ndepth = depthof(i)+1
            if ndepth > max_:
                max_ = ndepth
    return max_


'''Code starts here. Those functions(except create_ast) will remain
useless until I complete abstract syntax tree function'''


def create_ast(line):
    complexity = line.count('(')+line.count('[')+line.count('{')
    if line.strip()[0] == commentator:
        return #checks for comments
    line = line.split(commentator)[0].strip() #erase comments
    nseries = ''
    belongsto = None
    get_type = ''
    ret = ''
    ast_arr = []
    norm = []
    for j in range(len(line)):
        i = line[j]
        if i in finders:
            if belongsto == 'finders':    #finder classification
                nseries += i              #dont ask me why 'finder'
            else:
                ast_arr.append(nseries)
                belongsto = 'finders'
                nseries = i
        elif i in brs:
            if belongsto == 'brs':        #bracket classification
                nseries += i              
            else:
                ast_arr.append(nseries)
                belongsto = 'brs'
                nseries = i
        elif i in alph:
            if belongsto == 'alph':       #looks for variable and function names
                nseries += i              #cannot identify variables and functions seperatly yet
            else:
                ast_arr.append(nseries)
                belongsto = 'alph'
                nseries = i
        elif i.isnumeric():
            if belongsto == 'num':       #numerical parts of the string
                nseries += i
            else:
                ast_arr.append(nseries)
                belongsto = 'num'
                nseries = i
        elif i == '.':
            if belongsto == 'dot':       #'dot' classifier is only defined for [FLOAT_SEP]
                nseries += i             #but it can be modified later on to classify [CLASS_SEP]
            else:
                ast_arr.append(nseries)
                belongsto = 'dot'
                nseries = i
        else:
            belongsto = None            #avoids spaces but it will also avoid 
            nseries = i                 #illegal chars instead of raising an error
            
    ast_arr.append(nseries)
    if ast_arr[0] == '':
        ast_arr = ast_arr[1:]

    for i in ast_arr:                       #uses the classification array to create
        if i[0] in brs:                     #type list of input
            narr = []
            for j in i:
                narr.append(MATCH_UP[j])
            norm += narr
        elif i[0].isnumeric():
            norm.append('[NUM]')            #Additional [NUM] type
        elif i[0] in alph:
            norm.append('[VARN]')           #Still identifies a function as variable
        else:
            norm.append(MATCH_UP[i])        #Matches for other conditions


    '''Function definitions and calls are not identified by the code at that stage
    [CLASS_SEP] is not defined yet but a way of detecting it could be looking for
    [VARN][FLOAT_SEP][VARN] in norm and replacing the sequence with
    [CLASS][CLASS_SEP][FUNCTION].'''
    
    return ast_arr,norm
         

for i in create_ast('da*=(366.5-2)*4'):
    print(i)

"""
 * @author: nhphung

 HV: Chu Xuan Tinh -1870583
"""

from AST import *
from Visitor import *
from Utils import Utils
from StaticError import *
from collections import defaultdict
import functools

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

def flatten(li):
    return sum(([x] if not isinstance(x, list) else flatten(x)
                for x in li), [])

class Symbol:
    def __init__(self,name,mtype,value=False):
        self.name = name
        self.mtype = mtype
        self.value = value
# init value : None or False
class StaticChecker(BaseVisitor,Utils):
    global_envi = [
        Symbol("getInt", MType([], IntType()), True),
        Symbol("putInt", MType([IntType()], VoidType()), True),
        Symbol("putIntLn", MType([IntType()], VoidType()), True),
        Symbol("getFloat", MType([], FloatType()), True),
        Symbol("putFloat", MType([FloatType()], VoidType()), True),
        Symbol("putFloatLn", MType([FloatType()], VoidType()), True),
        Symbol("putBool", MType([BoolType()], VoidType()), True),
        Symbol("putBoolLn", MType([BoolType()], VoidType()), True),
        Symbol("putString", MType([StringType()], VoidType()), True),
        Symbol("putStringLn", MType([StringType()], VoidType()), True),
        Symbol("putLn", MType([], VoidType()), True)
    ]

    def __init__(self,ast):
        self.ast = ast

    def check(self):
        self.visit(self.ast,[StaticChecker.global_envi[:]])

    def visitProgram(self,ast, c):
        g = c[0]
        for x in ast.decl:
            if type(x) is VarDecl:
                g.append(self.visit(x, c))
            else:
                if self.lookup(x.name.name,g,lambda x: x.name):
                    raise Redeclared(Function(),x.name.name)
                g.append(Symbol(x.name.name, MType([i.varType for i in x.param], x.returnType)))

        for x in ast.decl:
            if type(x) is FuncDecl:
                self.visit(x,c)
        # 2.7 No Entry Point here
        checkentry = self.lookup('main', g, lambda x: x.name)
        if not checkentry or not type(checkentry.mtype) is MType:
            raise NoEntryPoint()

        for x in g:
            if type(x.mtype) is MType:
                if (not x.value) and (x.name != 'main'):
                    raise UnreachableFunction(x.name)
        #c[-1] ~ g
        '''checkentry = self.lookup("main", res, lambda x: x.name.lower())
        if not checkentry or checkentry.mtype.partype != [] or not type(checkentry.mtype) is MType or not type(
                checkentry.mtype.rettype) is VoidType:
            raise NoEntryPoint()'''

    # ok
    def visitVarDecl(self, ast, c):
        c = c[0]
        if self.lookup(ast.variable, c, lambda x: x.name) is None:
            return Symbol(ast.variable, ast.varType)
        else:
            raise Redeclared(Variable(), ast.variable)

    # const
    c_functype = VoidType()
    c_inloop = False
    c_funcname = ''

    def visitFuncDecl(self,ast, c):
        self.c_functype = ast.returnType
        self.c_funcname = ast.name.name
        #local = reduce(lambda x, y: x + [self.visit(y, (x, True))], ast.local, param)
        local_env = [[]] + c
        check_return = True
        for x in ast.param:
            if self.lookup(x.variable,local_env[0],lambda x: x.name) is None:
                local_env[0]+=[self.visit(x,local_env)]
            else:
                raise Redeclared(Parameter(),x.variable)
        for x in ast.body.member:
            if type(x) is VarDecl:
                local_env[0]+=[self.visit(x,local_env)]
            else:
                self.visit(x,local_env)
        if not (type(ast.returnType) is VoidType):
            check_return = False or self.visit(ast.body,local_env)
        if not check_return:
            raise FunctionNotReturn(ast.name.name)
        self.c_funcname = ''
        self.c_functype = None

    def visitId(self, ast, c):
        for ids in c:
            lookid = self.lookup(ast.name, ids, lambda x: x.name)
            if lookid:
                return lookid.mtype
        raise Undeclared(Identifier(), ast.name)

    def visitBlock(self, ast, c):
        check_return = False
        c = [[]] + c
        for x in ast.member:
            if type(x) is VarDecl:
                c[0] += [self.visit(x, c)]
            else:
                check_return = self.visit(x, c) or check_return
        return check_return

    # expr:Expr
    # thenStmt:Stmt
    # elseStmt:Stmt
    # if type(x) is Return: check_then = True
    # ok
    def visitIf(self, ast, c):
        expr = self.visit(ast.expr, c)
        if type(expr) is not BoolType:
            raise TypeMismatchInStatement(ast)
        else:
            check_then = False
            check_else = False
            check_then = self.visit(ast.thenStmt, c)
            if ast.elseStmt is not None:
                check_else = self.visit(ast.elseStmt, c)
                if check_else is True and check_then is True:
                    return True
                else:
                    return False
            return (check_then and check_else) # or []

    def visitReturn(self, ast, c):
        if ast.expr == None:
            if not (type(self.c_functype) is VoidType):
                raise TypeMismatchInStatement(ast)
        else:
            retStmtType = self.visit(ast.expr, c)
            if (type(self.c_functype) is FloatType) and (type(retStmtType) is IntType):
                pass
            elif type(self.c_functype) is ArrayPointerType:
                if ((not (type(retStmtType) is ArrayType)) and (not (type(retStmtType) is ArrayPointerType))) \
                        or (type(self.c_functype.eleType) != type(retStmtType.eleType)):
                    raise TypeMismatchInStatement(ast)
            else:
                if type(self.c_functype) != type(retStmtType):
                    raise TypeMismatchInStatement(ast)
        return True

    #     expr1:Expr
    #     expr2:Expr
    #     expr3:Expr
    #     loop:Stmt
    #     ok
    def visitFor(self, ast, c):
        expr1 = self.visit(ast.expr1, c)
        expr2 = self.visit(ast.expr2, c)
        expr3 = self.visit(ast.expr3, c)
        if type(expr1) is not IntType or type(expr2) is not BoolType or type(expr3) is not IntType:
            raise TypeMismatchInStatement(ast)
        try:
            self.visit(ast.loop, c)
        except BreakNotInLoop:
            pass
        except ContinueNotInLoop:
            pass
        return None

    # sl:List[Stmt]
    # exp: Expr
    def visitDowhile(self, ast, c):
        exp = self.visit(ast.exp, c)
        if type(exp) is not BoolType:
            raise TypeMismatchInStatement(ast)
        check_return = False
        try:
            for stmt in ast.sl:
                check_return = self.visit(stmt, c)
            return check_return
        except BreakNotInLoop:
            pass
        except ContinueNotInLoop:
            pass
        return None

    # ok

    def visitArrayCell(self, ast, c):
        # arr:Expr
        # idx:Expr
        arr = self.visit(ast.arr, c)
        idx = self.visit(ast.idx, c)
        if type(arr) is not ArrayType or type(idx) is not IntType:
            raise TypeMismatchInExpression(ast)
        else:
            return arr.eleType

    def visitBinaryOp(self,ast,c):
        lefttype = self.visit(ast.left, c)
        righttype = self.visit(ast.right, c)
        if ast.op is "=":
            if type(ast.left) is not Id and type(ast.left) is not ArrayCell:
                raise NotLeftValue(ast.left)
            if type(ast.left) is VoidType or type(ast.left) is ArrayPointerType or type(ast.left) is ArrayType:
                raise TypeMismatchInExpression(ast)
        if type(lefttype) is IntType:
            if type(righttype) is IntType:
                if ast.op in ['+','-','*','/', '%', '=']:
                    return IntType()
                elif ast.op == '/':
                    return FloatType()
                elif ast.op in ['<','<=','>','>=','!=','==']:
                    return BoolType()
                else:
                    raise TypeMismatchInExpression(ast)
            elif type(righttype) is FloatType:
                if ast.op in ['+','-','*','/', '%']:
                    return FloatType()
                elif ast.op in ['<','<=','>','>=','!=','==']:
                    return BoolType()
                else:
                    raise TypeMismatchInExpression(ast)
            else:
                raise TypeMismatchInExpression(ast)
        elif type(lefttype) in [FloatType]:
            if type(righttype) in [IntType, FloatType]:
                if ast.op in ['+','-','*','/','=']:
                    return FloatType()
                elif ast.op in ['<','<=','>','>=']:
                    return BoolType()
                else:
                    raise TypeMismatchInExpression(ast)
            else:
                raise TypeMismatchInExpression(ast)
        elif type(lefttype) is BoolType:
            if type(righttype) is BoolType:
                if ast.op in ['&&','||',"==" , "!=", "="]:
                    return BoolType()
                else:
                    raise TypeMismatchInExpression(ast)
            else:
                raise TypeMismatchInExpression(ast)
        elif type(lefttype) is StringType:
            if ast.op == "=":
                return StringType()
            else:
                raise TypeMismatchInExpression(ast)
        else:
            raise TypeMismatchInExpression(ast)

    #ok
    def visitUnaryOp(self, ast, c):
        env = c
        expr = self.visit(ast.body, env)
        if ast.op == '!':
            if type(expr) == type(BoolType()):
                return BoolType()
            else:
                raise TypeMismatchInExpression(ast)
        elif ast.op == '-':
            if type(expr) == type(IntType()):
                return IntType()
            elif type(expr) == type(FloatType()):
                return FloatType()  # pass
            else:
                raise TypeMismatchInExpression(ast)

    # method:Id
    # param:List[Expr]

    def visitCallExpr(self, ast, c):
        res = self.lookup(ast.method.name,flatten(c),lambda x: x.name)
        if res is None or not (type(res.mtype) is MType):
            raise Undeclared(Function(),ast.method.name)
        at = [self.visit(x, c) for x in ast.param]
        if len(res.mtype.partype) != len(at):
            raise TypeMismatchInExpression(ast)
        else:
            for i in range(len(at)):
                # c type -len -eletype
                if type(at[i] is type(res.mtype.partype[i])):
                    if type(at[i]) is ArrayPointerType:
                        if type(at[i].eleType) == type(res.mtype.partype[i].eleType):
                            pass
                        else:
                            raise TypeMismatchInExpression(ast)
                    else:
                        pass
                elif type(at[i]) is IntType and type(res.mtype.partype[i]) is FloatType:
                    pass
                elif type(at[i]) is ArrayType and type(res.mtype.partype[i]) is ArrayPointerType and type(
                        at[i].eleType) == type(res.mtype.partype[i].eleType):
                    pass
                else:
                    # !=
                    raise TypeMismatchInExpression(ast)

        if res.name != self.c_funcname:
            res.value = True
        return res.mtype.rettype
    '''
    def visitCallExpr(self, ast, c):

        at = [self.visit(x, c) for x in ast.param]
        res = self.lookup(ast.method.name, flatten(c), lambda x: x.name)
        if res is None:
            raise Undeclared(Function(), ast.method.name)
        elif not (type(res.mtype) is MType):
            raise TypeMismatchInExpression(ast)

        if len(res.mtype.partype) != len(at) or True in [type(a) != type(b) or (type(a) is  IntType and type(b) is FloatType) for a, b in zip(at, res.mtype.partype)]:
            raise TypeMismatchInExpression(ast)
        else:
            return res.mtype.rettype'''
    #ok

    def visitBreak(self, ast, c):
        if not self.c_inloop:
            raise BreakNotInLoop()

    def visitContinue(self, ast, c):
        if not self.c_inloop:
            raise ContinueNotInLoop()

    def visitArrayType(self,ast,c):
        eleType= self.visit(ast.eleType,c)
        return ArrayType(ast.dimen,eleType)
    #ok
    def visitArrayPointerType(self, ast, c):
        eleType = self.visit(ast.eleType, c)
        return ArrayPointerType(eleType)

    def visitIntLiteral(self, ast, c):
        return IntType()

    def visitFloatLiteral(self, ast, c):
        return FloatType()

    def visitBooleanLiteral(self, ast, c):
        return BoolType()

    def visitStringLiteral(self, ast, c):
        return StringType()

    def visitVoidType(self, ast, c):
        return VoidType()

    def visitIntType(self, ast, c):
        return IntType()

    def visitFloatType(self, ast, c):
        return FloatType()

    def visitBoolType(self, ast, c):
        return BoolType()

    def visitStringTYpe(self, ast, c):
        return StringType()



'''
 *   @author Nguyen Hua Phung
 *   @version 1.0
 *   23/10/2015
 *   This file provides a simple version of code generator
 *   HV CHU XUAN TINH 1870583
 *
'''
from Utils import *
from StaticCheck import *
from StaticError import *
from Emitter import Emitter
from Frame import Frame
from abc import ABC, abstractmethod

class CodeGenerator(Utils):
    def __init__(self):
        self.libName = "io"

    def init(self):
        return [Symbol("getInt", MType(list(), IntType()), CName(self.libName)),
                    Symbol("putInt", MType([IntType()], VoidType()), CName(self.libName)),
                    Symbol("putIntLn", MType([IntType()], VoidType()), CName(self.libName)),
                    Symbol("putFloatLn", MType([FloatType()], VoidType()), CName(self.libName)),
                    Symbol("putFloat", MType([FloatType()], VoidType()), CName(self.libName)),
                    Symbol("getFloat", MType([], FloatType()), CName(self.libName)),
                    Symbol("putBool", MType([BoolType()], VoidType()),CName(self.libName)),
                    Symbol("putBoolLn", MType([BoolType()], VoidType()), CName(self.libName)),
                    Symbol("putString", MType([StringType()], VoidType()), CName(self.libName)),
                    Symbol("putStringLn", MType([StringType()], VoidType()), CName(self.libName)),
                    Symbol("putLn", MType([], VoidType()), CName(self.libName)),
                    ]

    def gen(self, ast, dir_):
        #ast: AST
        #dir_: String

        gl = self.init()
        gc = CodeGenVisitor(ast, gl, dir_)
        gc.visit(ast, None)

class ClassType(Type):
    def __init__(self, cname):
        #cname: String
        self.cname = cname

    def __str__(self):
        return "ClassType"

    def accept(self, v, param):
        return v.visitClassType(self, param)

class SubBody():
    def __init__(self, frame, sym):
        #frame: Frame
        #sym: List[Symbol]

        self.frame = frame
        self.sym = sym
        #self.g_var = g_var

class Access():
    def __init__(self, frame, sym, isLeft, isFirst):
        #frame: Frame
        #sym: List[Symbol]
        #isLeft: Boolean
        #isFirst: Boolean

        self.frame = frame
        self.sym = sym
        self.isLeft = isLeft
        self.isFirst = isFirst

        # local variable -> moi bien co 1 chi so index, cap phat o chi so bao nhieu , bien Local moi tao ra index, sau nay truy xuat biet no o dau (Address)

class Val(ABC):
    pass

class Index(Val):
    def __init__(self, value):
        #value: Int

        self.value = value

class CName(Val):
    def __init__(self, value):
        #value: String

        self.value = value

class CodeGenVisitor(BaseVisitor, Utils):
    def __init__(self, astTree, env, dir_):
        #astTree: AST
        #env: List[Symbol]
        #dir_: File

        self.astTree = astTree
        self.env = env
        self.className = "MCClass"
        self.path = dir_
        self.emit = Emitter(self.path + "/" + self.className + ".j")

    def visitProgram(self, ast, c):
        #ast: Program
        #c: Any
        # Emiter : cung cap tac vu sinh ma
        # Frame: co nhiem vu lam viec voi: ham, chuong trinh con
        list_decl = self.env
        self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))

        for x in ast.decl:
            if type(x) is FuncDecl:
                list_paraType = [i.varType for i in x.param]
                list_decl = [Symbol(x.name.name, MType(list_paraType, x.returnType), CName(self.className))] + list_decl
            # var_global ->visit o vardecl
            # varArray
            else:
                #list_sym = self.visit(x, SubBody(Frame("<clinit>", x.varType), list(), g_var=True)) # xem lai nhe
                list_sym = self.visit(x, (SubBody(None, list_decl), "Global"))
                list_decl = [list_sym] + list_decl

        e = SubBody(None, list_decl)
        [self.visit(x, e) for x in ast.decl if type(x) is FuncDecl]
        # visit la funcdec
        # e = self.visit(x, e)
        # visit di vao cac khai bao bien toan cuc-> sinh ra ma tuong uong

        # generate default constructor
        self.genMETHOD(FuncDecl(Id("<init>"), list(), None, Block(list())), c, Frame("<init>", VoidType))

        self.emit.emitEPILOG()
        # sinh ra ma tan cung cua class
        return c

    def genMETHOD(self, consdecl, o, frame):
        #consdecl: FuncDecl
        #o: Any
        #frame: Frame

        isInit = consdecl.returnType is None
        isMain = consdecl.name.name == "main" and len(consdecl.param) == 0 and type(consdecl.returnType) is VoidType
        # check ham main
        returnType = VoidType() if isInit else consdecl.returnType
        methodName = "<init>" if isInit else consdecl.name.name
        intype = [ArrayPointerType(StringType())] if isMain else list()
        mtype = MType(intype, returnType)

        self.emit.printout(self.emit.emitMETHOD(methodName, mtype, not isInit, frame))

        frame.enterScope(True)

        glenv = o

        # Generate code for parameter declarations
        if isInit:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", ClassType(self.className), frame.getStartLabel(), frame.getEndLabel(), frame))
        if isMain:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayPointerType(StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))
            # sinh ra nhan dau tien , getstart label -> sinh ra label

        '''local_sub = SubBody(frame, glenv)
        for x in consdecl.param + [i for i in consdecl.body.member if type(i) is VarDecl]:
            local_sub = self.visit(x, local_sub)
        body = consdecl.body
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))'''

        local_sub = SubBody(frame, glenv)
        for x in consdecl.param:
            local_sub = self.visit(x, (local_sub, "Parameter"))

        for x in consdecl.body.member:
            if type(x) is VarDecl:
                local_sub = self.visit(x, (local_sub, "Local"))
            else:
                self.visit(x, local_sub)

        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))

        # Generate code for statements
        if isInit:
            self.emit.printout(self.emit.emitREADVAR("this", ClassType(self.className), 0, frame))
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        #list(map(lambda x: self.visit(x, SubBody(frame, glenv)), body.member))

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if type(returnType) is VoidType:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope();

    def visitFuncDecl(self, ast, o):
        #ast: FuncDecl
        #o: Any
        # khi co 1 method -> su dung dich vu frame, level1: cua chuong trinh con vaf chuong trinh khac nhau (vi du Jump label),
        # frame quan lys label cua chuong trinh con, khong duoc truyen frame cua chuong trinh con nay  cho ct con khac
        # frame , sinh ma thuoc trong 1 ct con , tao moi khi co func moi, tao frame moi
        # o: env
        subctxt = o
        frame = Frame(ast.name, ast.returnType)
        # truyen frame vao genmethod
        self.genMETHOD(ast, subctxt.sym, frame)
        return SubBody(None, [Symbol(ast.name, MType(list(), ast.returnType), CName(self.className))] + subctxt.sym)
    # xem lai
    def visitVarDecl(self, ast, o):
        ctxt = o[0]
        frame = ctxt.frame
        env = ctxt.sym
        if o[1] == "Global":
            self.emit.printout(self.emit.emitATTRIBUTE(ast.variable, ast.varType, False, ""))
            return Symbol(ast.variable, ast.varType)
        # goi getnewindex dua vao , gap 1 khai bao goi getnew index
        # param & local
        elif o[1] == "Local":
            idx = frame.getNewIndex()
            labelStart = frame.getNewLabel()
            self.emit.printout(self.emit.emitVAR(idx, ast.variable, ast.varType, labelStart, frame.getEndLabel(), frame))
            self.emit.printout(self.emit.emitLABEL(labelStart,frame))
            return SubBody(frame, [Symbol(ast.variable, ast.varType, Index(idx))] + env)
        else:
            idx = frame.getNewIndex()
            self.emit.printout(self.emit.emitVAR(idx, ast.variable, ast.varType, frame.getStartLabel(), frame.getEndLabel(), frame))
            # dua vao env (name, type, index)
            return SubBody(frame, [Symbol(ast.variable, ast.varType, Index(idx))] + env)


    def visitBlock(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        newenv = o.sym
        list_var = SubBody(frame, newenv)
        frame.enterScope(False)
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        for x in ast.member:
            if type(x) is not VarDecl:
                self.visit(x, list_var)
            else:
                list_var = self.visit(x, (list_var, False))
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        frame.exitScope()
        return newenv

    def visitBreak(self, ast, o):
        return self.emit.printout(self.emit.emitGOTO(o.frame.getBreakLabel(), o.frame))

    def visitContinuce(self, ast, o):
        return self.emit.printout(self.emit.emitGOTO(o.frame.getContinuceLabel(), o.frame))

    def visitReturn(self, ast, o):
        if ast.expr:
            exp, typexp = self.visit(ast.expr, Access(o.frame, o.sym, False, True))
            if type(typexp) == IntType and type(o.frame.returnType) == FloatType:
                self.emit.printout(exp + self.emit.emitI2F(o.frame) + self.emit.emitRETURN(FloatType(), o.frame))
            else:
                self.emit.printout(exp + self.emit.emitRETURN(typexp, o.frame))
        else:
            self.emit.printout(self.emit.emitRETURN(VoidType(), o.frame))





    def visitIf(self, ast,o):
        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        labelOut = frame.getNewLabel() # true
        labelElse = frame.getNewLabel() if ast.elseStmt else None # false
        exprCode, exprType = self.visit(ast.expr, Access(frame, nenv, False, True))

        self.emit.printout(exprCode)
        # emitIFFALSE(LabelElse)
        if ast.elseStmt:
          # false -> jump to label Else
            self.emit.printout(self.emit.emitIFFALSE(labelElse, frame))
        else:
            self.emit.printout(self.emit.emitIFFALSE(labelOut, frame))

        thenStmt = self.visit(ast.thenStmt, ctxt)

        if thenStmt is not True:
            self.emit.printout(self.emit.emitGOTO(labelOut, frame))

        elseStmt = []
        if ast.elseStmt:
            self.emit.printout(self.emit.emitLABEL(labelElse, frame))
            elseStmt = self.visit(ast.elseStmt, ctxt)

        self.emit.printout(self.emit.emitLABEL(labelOut, frame))

        if thenStmt is True and elseStmt is True:
            return True
            # None?


    def visitDowhile(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        labelLoop = frame.getNewLabel()
        labelExit = frame.getNewLabel()
        frame.enterLoop()
        self.emit.printout(self.emit.emitLABEL(labelLoop, frame))
        list(map(lambda x: self.visit(x, o) if type(x) is not VarDecl else self.visit(x, (o, "Local")), ast.sl))
        self.emit.printout(self.emit.emitLABEL(frame.getContinueLabel(), frame))
        expCode, expType = self.visit(ast.exp, Access(frame, nenv, False, True))
        self.emit.printout(expCode)
        self.emit.printout(self.emit.emitIFTRUE(labelLoop, frame))
        self.emit.printout(self.emit.emitGOTO(labelExit, frame))
        self.emit.printout(self.emit.emitLABEL(labelExit, frame))
        self.emit.printout(self.emit.emitLABEL(frame.getBreakLabel(), frame))
        frame.exitLoop()

    '''def visitFor(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        nevn = ctxt.sym
        labelLoop = frame.getNewLabel()
        labelExit = frame.getNewLabel()
        labelConti = frame.getContinueLabel()
        labelBreak = frame.getBreakLabel()
        #expr1Code, expr1Type = self.visit(ast.expr1, Access(frame, nevn, False, True))
        expr2Code, expr2Type = self.visit(ast.expr2, Access(frame, nevn, False, True))
        #expr3Code, expr3Type = self.visit(ast.expr3, Access(frame, nevn, False, True))
        frame.enterScope()
        self.visit(ast.expr1, o)
        self.emit.printout(self.emit.emitLABEL(labelLoop, frame))
        self.emit.printout(expr2Code)
        self.emit.printout(self.emit.emitIFFALSE(labelExit, frame))
        self.visit(ast.loop, o)
        self.emit.printout(self.emit.emitLABEL(labelConti, frame))
        self.visit(ast.expr3, o)
        self.emit.printout(self.emit.emitGOTO(labelLoop, frame))
        self.emit.printout(self.emit.emitLABEL(labelExit, frame))
        self.emit.printout(self.emit.emitLABEL(labelBreak, frame))
        frame.exitScope()'''

    def visitFor(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        nevn = ctxt.sym
        labelStart = frame.getNewLabel()
        labelEnd = frame.getNewLabel()
        expr1Code, expr1Type = self.visit(ast.expr1, Access(frame, nevn, False, True))
        expr2Code, expr2Type = self.visit(ast.expr2, Access(frame, nevn, False, True))
        expr3Code, expr3Type = self.visit(ast.expr3, Access(frame, nevn, False, True))
        self.emit.printout(expr1Code)
        self.emit.printout(self.emit.emitPOP(frame))
        frame.enterLoop()
        self.emit.printout(self.emit.emitLABEL(labelStart, frame))
        self.emit.printout(expr2Code)
        self.emit.printout(self.emit.emitIFFALSE(labelEnd, frame))
        self.visit(ast.loop, ctxt)
        self.emit.printout(self.emit.emitLABEL(frame.getContinueLabel(), frame))
        self.emit.printout(expr3Code)
        self.emit.printout(self.emit.emitPOP(frame))
        self.emit.printout(self.emit.emitGOTO(labelStart, frame))
        self.emit.printout(self.emit.emitLABEL(frame.getBreakLabel(), frame))
        self.emit.printout(self.emit.emitLABEL(labelEnd, frame))
        frame.exitLoop()

    def visitCallExpr(self, ast, o):
        #ast: CallExpr
        #o: Any
        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.method.name, nenv, lambda x: x.name)
        cname = sym.value.value
        ctype = sym.mtype
        in_ = ("", list())
        for x in ast.param:
            str1, typ1 = self.visit(x, Access(frame, nenv, False, True))
            in_ = (in_[0] + str1, in_[1].append(typ1))
        self.emit.printout(in_[0])
        self.emit.printout(self.emit.emitINVOKESTATIC(cname + "/" + ast.method.name, ctype, frame))

        # Tra ve ma code, type
        # visit statement : khong tra ve ma in ra luon
        # visit declare -> return moi truong



    #ok
    def visitUnaryOp(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        op = ast.op
        exprCode, exprType = self.visit(ast.body, o)
        if op == '!':
            return exprCode + self.emit.emitNOT(BoolType(), frame), BoolType()
        elif op == '-':
            return exprCode + self.emit.emitNEGOP(exprType, frame), exprType

    def visitBinaryOp(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        op = ast.op
        nenv = o.sym
        if op == '=':
            rightCode, rightType = self.visit(ast.right, Access(frame, nenv, False, True))
            leftCode, leftType  = self.visit(ast.left, Access(frame, nenv, True, True))
            if type(leftType) == FloatType and type(rightType) == IntType:
                rightCode = rightCode + self.emit.emitI2F(frame)
            #return rightCode + leftCode
            returncode = rightCode + leftCode
            frame.push()
            if type(o) is SubBody:
                self.emit.printout(returncode)
            else:
                returncode = rightCode + self.emit.emitDUP(frame) + leftCode
                return returncode, leftType
        else:
            leftCode, leftType = self.visit(ast.left, Access(frame, nenv, False, True))
            rightCode, rightType = self.visit(ast.right, Access(frame, nenv, False, True))
            expr_type = FloatType() if type(leftType) is not type(rightType) else leftType
            if type(expr_type) is FloatType:
                if type(leftType) is IntType:
                    leftCode = leftCode + self.emit.emitI2F(frame)
                if type(rightType) is IntType:
                    rightCode = rightCode + self.emit.emitI2F(frame)
            if op in ["+", "-"]:
                return leftCode + rightCode + self.emit.emitADDOP(op, expr_type, frame), expr_type
            elif op in ["*", "/"]:
                return leftCode + rightCode + self.emit.emitMULOP(op, expr_type, frame), expr_type
            elif op == "%":
                return leftCode + rightCode + self.emit.emitMOD(frame), IntType()
            elif op == "||":
                return leftCode + rightCode + self.emit.emitOROP(frame), BoolType()
            elif op == "&&":
                return leftCode + rightCode + self.emit.emitANDOP(frame), BoolType()
            else:
                return leftCode + rightCode + self.emit.emitREOP(op, expr_type, frame), BoolType()

    def visitId(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        symbols = ctxt.sym
        isLeft = ctxt.isLeft
        isFirst = ctxt.isFirst
        sym = self.lookup(ast.name, symbols, lambda x: x.name)
        if not isFirst and isLeft:
            frame.push()
        elif not isFirst and not isLeft:
            frame.pop()
        if sym.value is None:
            if isLeft:
                return self.emit.emitPUTSTATIC(self.className + "/" + sym.name, sym.mtype, frame), sym.mtype
            else:
                return self.emit.emitGETSTATIC(self.className + "/" + sym.name, sym.mtype, frame), sym.mtype
        else:
            if isLeft:
                return self.emit.emitWRITEVAR(sym.name, sym.mtype, sym.value.value, frame), sym.mtype
            else:
                return self.emit.emitREADVAR(sym.name, sym.mtype, sym.value.value, frame), sym.mtype

    def visitIntLiteral(self, ast, o):
        #ast: IntLiteral
        #o: Any
        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHICONST(ast.value, frame), IntType()

    def visitFloatLiteral(self, ast, o):

        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHFCONST(str(ast.value), frame), FloatType()

    def visitBooleanLiteral(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHICONST(str(ast.value), frame), BoolType()

    def visitStringLiteral(self, ast,o):
        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHCONST('"' + str(ast.value) + '"', StringType(), frame), StringType()
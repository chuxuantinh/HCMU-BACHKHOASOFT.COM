# HV CHU XUAN TINH 1870583
from MCVisitor import MCVisitor
from MCParser import MCParser
from AST import *
from functools import reduce

class ASTGeneration(MCVisitor):
    # program: many_declaration+ EOF;  // dau ++
    def visitProgram(self,ctx:MCParser.ProgramContext):

        '''decl = []
        for x in ctx.many_declaration():
            decl += self.visit(x)
        return Program(decl)'''

        list_manydecl = []
        for x in ctx.many_declaration():
            if x.variable_declaration():
                list_manydecl = list_manydecl + self.visit(x)
            else:
                list_manydecl.append(self.visit(x))
        return Program(list_manydecl)

    # https://www.edureka.co/community/41299/what-the-difference-between-append-and-insert-python-lists
    # many_declaration: variable_declaration|function_declaration;
    def visitMany_declaration(self, ctx: MCParser.Many_declarationContext):
        if ctx.variable_declaration():
            return self.visit(ctx.variable_declaration())
        if ctx.function_declaration():
            return self.visit(ctx.function_declaration())

    """
    # variable_declaration: primitive_type variable_list SEMI ; # check lai cai nay nhe
    def visitVariable_declaration(self, ctx: MCParser.Variable_declarationContext):
        self.primitive_type = self.visit(ctx.primitive_type())
        self.visit(ctx.variable_list())

    # variable_list:  variable (COMMA variable)*;
    # variable: ID (LSB INTLIT RSB)?;
    
    # variable_list:  variable (COMMA variable)*;
    def visitVariable_list(self, ctx: MCParser.Variable_listContext):
        list_variable = []
        for x in ctx.variable_list:
            list_variable += self.visit(x)
        return list_variable

    # variable: ID (LSB INTLIT RSB)?; xem lai cai nay nhe
    def visitVariable(self, ctx: MCParser.VariableContext):
        if ctx.INLIT():
            return VarDecl(Id(ctx.ID().getText()), ArrayType(IntLiteral(ctx.INTLIT().getText()), self.visit(ctx.primitive_type())))
        else:
            return VarDecl(Id(ctx.ID().getText()), self.visit(ctx.primitive_type()))
    """

    # variable_declaration: primitive_type variable_list SEMI ;
    # variable_list:  variable (COMMA variable)*;
    # variable: ID (LSB INTLIT RSB)?; getChildCount


    def visitVariable_declaration(self, ctx: MCParser.Variable_declarationContext):
        list_variable = []
        variable = ctx.variable_list().variable()
        for x in variable:
            if x.INTLIT():
                list_variable.append(VarDecl(Id(x.ID().getText()), ArrayType(IntLiteral(x.INTLIT().getText()), self.visit(ctx.primitive_type()))))
            else:
                list_variable.append(VarDecl(Id(x.ID().getText()), self.visit(ctx.primitive_type())))
        return list_variable


    # function_declaration: (VOID| primitive_type| arraypointer_type_out) ID LB parameter_list? RB block_statement  ;
    # name: Id
    # param: List[VarDecl]
    # returnType: Type
    # body: Block

    def visitFunction_declaration(self, ctx:MCParser.Function_declarationContext):
        name = Id(ctx.ID().getText())
        param = ([self.visit(x) for x in ctx.parameter_list().parameter_declaration()] if ctx.parameter_list() else [])
        if ctx.VOID():
            re_type = VoidType()
        elif ctx.primitive_type():
            re_type = self.visit(ctx.primitive_type())
        else:
            if ctx.arraypointer_type_out().LSB():
                re_type = ArrayPointerType(self.visit(ctx.arraypointer_type_out().primitive_type()))
        body = self.visit(ctx.block_statement())
        return FuncDecl(name, param, re_type, body)



    # parameter_list:  parameter_declaration (COMMA parameter_declaration)*;
    '''
    def visitParameter_list(self, ctx: MCParser.Parameter_listContext):
        para_list =[]
        for x in ctx.parameter_declaration():
            para_list += self.visit(x)
        return para_list'''

    # parameter_declaration:   primitive_type ID (LSB RSB)? ;
    def visitParameter_declaration(self, ctx: MCParser.Parameter_declarationContext):
        _id = Id(ctx.ID().getText())
        _type = self.visit(ctx.primitive_type())
        if ctx.LSB():
            return VarDecl(_id, ArrayPointerType(_type))
        else:
            return VarDecl(_id, _type)


    # arraypointer_type_out:  primitive_type LSB RSB;
    def visitArraypointer_type_out(self, ctx: MCParser.Arraypointer_type_outContext):
        if ctx.LSB() and ctx.RSB():
            return ArrayPointerType(self.visit(ctx.primitive_type()))

    # block_statement: LP (variable_declaration | statement)* RP xem lai nhe
    def visitBlock_statement(self, ctx: MCParser.Block_statementContext):
        bl = [];
        if ctx.variable_declaration():
            for x in ctx.variable_declaration():
                bl = bl + self.visit(x)
        if ctx.statement():

            if ctx.statement():
                bl = bl + [self.visit(x) for x in ctx.statement()]
            else:
                bl = bl + []
        return Block(bl)


    # statement: if_statement| while_statement|  for_statement| break_statement| continuce_statement|return_statement| exp_statement | block_statement ;

    def visitStatement(self, ctx: MCParser.StatementContext):

        if ctx.if_statement():
            return self.visit(ctx.if_statement())
        if ctx.while_statement():
            return self.visit(ctx.while_statement())
        if ctx.for_statement():
            return self.visit(ctx.for_statement())
        if ctx.break_statement():
            return Break()
        if ctx.continuce_statement():
            return Continue()
        if ctx.return_statement():
            return self.visit(ctx.return_statement())
        if ctx.exp_statement():
            return self.visit(ctx.exp_statement())
        if ctx.block_statement():
            return self.visit(ctx.block_statement())

    # if_statement: IF LB expression RB statement (ELSE statement)?;
    def visitIf_statement(self, ctx: MCParser.If_statementContext):
        if ctx.ELSE():
            return If(self.visit(ctx.expression()),self.visit(ctx.statement(0)), self.visit(ctx.statement(1)))
        else:
            return If(self.visit(ctx.expression()),self.visit(ctx.statement(0)),None)

    # return If(self.visit(ctx.expression()),self.visit(ctx.statement(0)),[])

    # while_statement: DO statement+ WHILE expression SEMI; do trong AST cua Thay
    def visitWhile_statement(self, ctx:MCParser.While_statementContext):
        sl = [self.visit(x) for x in ctx.statement()]
        exp = self.visit(ctx.expression())
        return Dowhile(sl,exp)

    # for_statement: FOR LB expression SEMI expression SEMI expression RB statement;
    #expr1: Expr
    #expr2: Expr
    #expr3: Expr
    #loop: Stmt
    def visitFor_statement(self, ctx:MCParser.For_statementContext):
        expr1 = self.visit(ctx.expression(0))
        expr2 = self.visit(ctx.expression(1))
        expr3 = self.visit(ctx.expression(2))
        loop = self.visit(ctx.statement())
        return For(expr1,expr2,expr3,loop)

    def visitBreak_statement(self, ctx:MCParser.Break_statementContext):
        return Break()


    # Visit a parse tree produced by MCParser#continuce_statement.
    def visitContinuce_statement(self, ctx:MCParser.Continuce_statementContext):
        return Continue()


    # Visit a parse tree produced by MCParser#return_statement.
    #return_statement: RETURN expression? SEMI;
    def visitReturn_statement(self, ctx:MCParser.Return_statementContext):
        if ctx.expression():
            return Return(self.visit(ctx.expression()))
        else:
            return Return(None)

    #exp_statement: expression SEMI;
    def visitExp_statement(self, ctx:MCParser.Exp_statementContext):
        return self.visit(ctx.expression())

    # funcall: ID LB (expression (COMMA expression)*)? RB ;
    # Funcall(method, param)
    def visitFuncall(self, ctx:MCParser.FuncallContext):
        method = Id(ctx.ID().getText())
        param = list(map(lambda x:self.visit(x),ctx.expression())) if ctx.expression() else []
        return CallExpr(method, param)



    # not used
    '''def visitIndex_exp(self, ctx:MCParser.Index_expContext):
        return self.visitChildren(ctx)'''


    # expression: expression1 ASSIGN_OP expression | expression1;  if ctx.getChildCount() == 3->class BinaryOp(Expr):

    def visitExpression(self, ctx: MCParser.ExpressionContext):
        if ctx.ASSIGN_OP():
            op = ctx.ASSIGN_OP().getText()
            left = self.visit(ctx.expression1())
            right = self.visit(ctx.expression())
            return BinaryOp(op, left, right)
        else:
            return self.visit(ctx.expression1())

    # expression1: expression1 OR expression2| expression2;
    def visitExpression1(self, ctx:MCParser.Expression1Context):
        if ctx.OR():
            op = ctx.OR().getText()
            left = self.visit(ctx.expression1())
            right = self.visit(ctx.expression2())
            return BinaryOp(op,left,right)
        else:
            return self.visit(ctx.expression2())

    # expression2: expression2  AND expression3 | expression3;
    def visitExpression2(self, ctx:MCParser.Expression2Context):
        if ctx.AND():
            op = ctx.AND().getText()
            left = self.visit(ctx.expression2())
            right = self.visit(ctx.expression3())
            return BinaryOp(op,left,right)
        else:
            return self.visit(ctx.expression3())
    # expression3: expression4 (EQUAL| NOT_EQUAL) expression4 | expression4;
    def visitExpression3(self, ctx:MCParser.Expression3Context):
        if ctx.EQUAL():
            op = ctx.EQUAL().getText()
        elif ctx.NOT_EQUAL():
            op = ctx.NOT_EQUAL().getText()
        else:
            return self.visit(ctx.expression4(0))
        left = self.visit(ctx.expression4(0))
        right = self.visit(ctx.expression4(1))
        return BinaryOp(op,left,right)



    #expression4: expression5(LESS_THAN | LESS_THAN_EQUAL | GREATER_THAN | GREATER_THAN_EQUAL) expression5 | expression5;
    def visitExpression4(self, ctx:MCParser.Expression4Context):
        if ctx.LESS_THAN():
            op = ctx.LESS_THAN().getText()
        elif ctx.LESS_THAN_EQUAL():
            op = ctx.LESS_THAN_EQUAL().getText()
        elif ctx.GREATER_THAN():
            op = ctx.GREATER_THAN().getText()
        elif ctx.GREATER_THAN_EQUAL():
            op = ctx.GREATER_THAN_EQUAL().getText()
        else:
            return self.visit(ctx.expression5(0))
        left = self.visit(ctx.expression5(0))
        right = self.visit(ctx.expression5(1))
        return BinaryOp(op,left,right)

    #expression5: expression5 (ADD | SUB) expression6 | expression6;
    def visitExpression5(self, ctx:MCParser.Expression5Context):
        if ctx.ADD():
            op = ctx.ADD().getText()
        elif ctx.SUB():
            op = ctx.SUB().getText()
        else:
            return self.visit(ctx.expression6())
        left = self.visit(ctx.expression5())
        right = self.visit(ctx.expression6())
        return BinaryOp(op,left,right)
    # expression6: expression6 (DIV| MUL | MOD) expression7 | expression7;

    def visitExpression6(self, ctx:MCParser.Expression6Context):
        if ctx.DIV():
            op = ctx.DIV().getText()
        elif ctx.MUL():
            op = ctx.MUL().getText()
        elif ctx.MOD():
            op = ctx.MOD().getText()
        else:
            return self.visit(ctx.expression7())
        left = self.visit(ctx.expression6())
        right = self.visit(ctx.expression7())
        return BinaryOp(op,left,right)

    # expression7: (SUB| NOT) expression7 | expression8;
    def visitExpression7(self, ctx: MCParser.Expression7Context):
        if ctx.SUB():
            op = ctx.SUB().getText()
        elif ctx.NOT():
            op = ctx.NOT().getText()
        else:
            return self.visit(ctx.expression8())
        body = self.visit(ctx.expression7())
        return UnaryOp(op, body)

    # expression8: term LSB expression RSB | term;
    def visitExpression8(self, ctx: MCParser.Expression8Context):
        if ctx.LSB():
            arr = self.visit(ctx.term())
            idx = self.visit(ctx.expression())
            return ArrayCell(arr, idx)
        else:
            return self.visit(ctx.term())

    # term:  BOOLEAN_LIT| FLOAT_LIT |INTLIT| STRING_LIT| ID| funcall | LB expression RB ;
    def visitTerm(self, ctx: MCParser.TermContext):
        if ctx.BOOLEAN_LIT():
            return BooleanLiteral(bool(ctx.BOOLEAN_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())
        elif ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.funcall():
            return self.visit(ctx.funcall())
        else:
            return self.visit(ctx.expression())

    # primitive_type: INT|FLOAT|STRING|BOOLEAN;
    def visitPrimitive_type(self, ctx: MCParser.Primitive_typeContext):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.STRING():
            return StringType()
        else:
            return BoolType()

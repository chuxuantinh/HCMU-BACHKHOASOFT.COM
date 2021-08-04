import unittest
from TestUtils import TestLexer


class LexerSuite(unittest.TestCase):

    def test_identifiers(self):
        """test identifiers"""
        self.assertTrue(TestLexer.checkLexeme("ab", "ab,<EOF>", 101))
    def test_lower_upper_id(self):
        self.assertTrue(TestLexer.checkLexeme("aCBbdc", "aCBbdc,<EOF>", 102))
    def test_lexer_mix_id1(self):
        self.assertTrue(TestLexer.checkLexeme("abc123ABC", "abc123ABC,<EOF>", 103))
    def test_wrong_token(self):
        self.assertTrue(TestLexer.checkLexeme("aA?sVN", "aA,Error Token ?", 104))
    def test_lexer1(self):
        self.assertTrue(TestLexer.checkLexeme("_abcd", "_abcd,<EOF>", 105))
    def test_lexer2(self):
        self.assertTrue(TestLexer.checkLexeme("abc_def", "abc_def,<EOF>", 106))
    def test_id3(self):
        self.assertTrue(TestLexer.checkLexeme("abc_123", "abc_123,<EOF>", 107))
    def test_lexer3(self):
        self.assertTrue(TestLexer.checkLexeme("<abc>", "<,abc,>,<EOF>", 108))

    # test float
    def test_float_1(self):
        self.assertTrue(TestLexer.checkLexeme("123.1234", "123.1234,<EOF>", 110))
    def test_float_2(self):
        self.assertTrue(TestLexer.checkLexeme("123e-1234", "123e-1234,<EOF>", 111))
    def test_float_3(self):
        self.assertTrue(TestLexer.checkLexeme("1.2", "1.2,<EOF>", 112))
    def test_float_4(self):
        self.assertTrue(TestLexer.checkLexeme("123.", "123.,<EOF>", 113))
    def test_float_5(self):
        self.assertTrue(TestLexer.checkLexeme(".123", ".123,<EOF>", 114))
    def test_float6(self):
        self.assertTrue(TestLexer.checkLexeme("123e123", "123e123,<EOF>", 115))
    def test_float6(self):
        self.assertTrue(TestLexer.checkLexeme(".123e123", ".123e123,<EOF>", 116))
    def test_float8(self):
        self.assertTrue(TestLexer.checkLexeme("123e-1234", "123e-1234,<EOF>", 118))
    def test_float9(self):
        self.assertTrue(TestLexer.checkLexeme("1.2E-2", "1.2E-2,<EOF>", 119))
    def test_float10(self):
        self.assertTrue(TestLexer.checkLexeme("1.2e-2", "1.2e-2,<EOF>", 120))
    def test_float11(self):
        self.assertTrue(TestLexer.checkLexeme(".2e-2", ".2e-2,<EOF>", 120))
    def test_float12(self):
        self.assertTrue(TestLexer.checkLexeme("9.0", "9.0,<EOF>", 121))
    def test_float13(self):
        self.assertTrue(TestLexer.checkLexeme("1.", "1.,<EOF>", 122))
    def test_float14(self):
        self.assertTrue(TestLexer.checkLexeme("0.33E-3", "0.33E-3,<EOF>", 123))
    # test operator
    def test_separator5(self):
        self.assertTrue(TestLexer.checkLexeme(",123", ",,123,<EOF>", 124))

    def test_boolean1(self):
        self.assertTrue(TestLexer.checkLexeme("true", "true,<EOF>", 125))
    def test_boolean1(self):
        self.assertTrue(TestLexer.checkLexeme("TruE", "TruE,<EOF>", 126))
    def test_boolean3(self):
        self.assertTrue(TestLexer.checkLexeme("FalSe", "FalSe,<EOF>", 127))
    def test_boolean4(self):
        self.assertTrue(TestLexer.checkLexeme("TruE False", "TruE,False,<EOF>", 128))
    def test_boolean5(self):
        self.assertTrue(TestLexer.checkLexeme("FALSE TRUE", "FALSE,TRUE,<EOF>", 129))

    # test integer
    def test_integer(self):
        self.assertTrue(TestLexer.checkLexeme("123a123", "123,a123,<EOF>", 130))
    def test_integer2(self):
        self.assertTrue(TestLexer.checkLexeme("123abc", "123,abc,<EOF>", 131))
    def test_integer3(self):
        self.assertTrue(TestLexer.checkLexeme("1234_abcd", "1234,_abcd,<EOF>", 132))
    def test_integer4(self):
        self.assertTrue(TestLexer.checkLexeme("123 456 789", "123,456,789,<EOF>", 133))
    def test_integer5(self):
        self.assertTrue(TestLexer.checkLexeme("123_123", "123,_123,<EOF>", 134))
    def test_interger6(self):
        self.assertTrue(TestLexer.checkLexeme("234_abc456", "234,_abc456,<EOF>", 135))
    def test_interger7(self):
        self.assertTrue(TestLexer.checkLexeme("123", "123,<EOF>", 136))

    def test_operator1(self):
        self.assertTrue(TestLexer.checkLexeme("a+b", "a,+,b,<EOF>", 137))
    def test_operator2(self):
        self.assertTrue(TestLexer.checkLexeme("a-b", "a,-,b,<EOF>", 138))
    def test_operator3(self):
        self.assertTrue(TestLexer.checkLexeme("-123-abc", "-,123,-,abc,<EOF>", 139))
    def tes_operator4(self):
        self.assertTrue(TestLexer.checkLexeme("abc*xyz", "abc,*,xyz,<EOF>", 140))
    def tes_operator5(self):
        self.assertTrue(TestLexer.checkLexeme("abc/xyz", "abc,/,xyz,<EOF>", 141))
    def test_operator6(self):
        self.assertTrue(TestLexer.checkLexeme("90/2", "90,/,2,<EOF>", 142))
    def test_operator7(self):
        self.assertTrue(TestLexer.checkLexeme("-123-abc", "-,123,-,abc,<EOF>", 143))
    def test_operator8(self):
        self.assertTrue(TestLexer.checkLexeme("123/*456", "123,/,*,456,<EOF>", 144))
    def test_operator9(self):
        self.assertTrue(TestLexer.checkLexeme("/%%/", "/,%,%,/,<EOF>", 145))
    def test_operator10(self):
        self.assertTrue(TestLexer.checkLexeme("a!&&||b", "a,!,&&,||,b,<EOF>", 146))
    def test_operator11(self):
        self.assertTrue(TestLexer.checkLexeme("><!=!=><", ">,<,!=,!=,>,<,<EOF>", 147))
    def test_operator12(self):
        self.assertTrue(TestLexer.checkLexeme("=>!=", "=,>,!=,<EOF>", 148))
    def test_operator13(self):
        self.assertTrue(TestLexer.checkLexeme("(a+b-c+d*e/f / g % h)", "(,a,+,b,-,c,+,d,*,e,/,f,/,g,%,h,),<EOF>", 149))
    def test_operator14(self):
        self.assertTrue(TestLexer.checkLexeme("(a>=b-c<=d*e/f / g % h)", "(,a,>=,b,-,c,<=,d,*,e,/,f,/,g,%,h,),<EOF>", 150))

    # test keyword
    def test_keyword1(self):
        self.assertTrue(TestLexer.checkLexeme("coNTinue coNTinue coNTINuE cONtiNUe", "coNTinue,coNTinue,coNTINuE,cONtiNUe,<EOF>", 151))
    def test_keyword2(self):
        self.assertTrue(TestLexer.checkLexeme("FOR foR For fOR", "FOR,foR,For,fOR,<EOF>", 152))
    def test_keyword3(self):
        self.assertTrue(TestLexer.checkLexeme("intEgeR float StrIng BoOleaN", "intEgeR,float,StrIng,BoOleaN,<EOF>", 153))
    def test_keyword4(self):
        self.assertTrue(TestLexer.checkLexeme("BreaK bREAK BrEAk bReAK", "BreaK,bREAK,BrEAk,bReAK,<EOF>", 154))
    def test_keyword5(self):
        self.assertTrue(TestLexer.checkLexeme("INT BOolean STRing while", "INT,BOolean,STRing,while,<EOF>",155))
    def test_keyword6(self):
        self.assertTrue(
            TestLexer.checkLexeme("boolean break continue else for float if int return void do while true false string",
                                  "boolean,break,continue,else,for,float,if,int,return,void,do,while,true,false,string,<EOF>",
                                  156))
    def test_keyword7(self):
        self.assertTrue(TestLexer.checkLexeme("string_integer", "string_integer,<EOF>", 157))

    def test_illegalesc1(self):
        self.assertTrue(TestLexer.checkLexeme(" \"\\ ","Illegal Escape In String: \\ ",158))
    def test_illegalesc2(self):
        self.assertTrue(TestLexer.checkLexeme(" \"\\abcd ","Illegal Escape In String: \\a",159))
    # test comment
    def test_comment1(self):
        self.assertTrue(TestLexer.checkLexeme("/*//abc123*/", "<EOF>", 160))
    def test_comment2(self):
        self.assertTrue(TestLexer.checkLexeme("/*{this is block comment}*/", "<EOF>", 161))
    def test_comment3(self):
        self.assertTrue(TestLexer.checkLexeme("""//met qua Thay a a\n bbbb""","bbbb,<EOF>",162))
    def test_comment4(self):
        self.assertTrue(TestLexer.checkLexeme("///abc}", "<EOF>", 163))
    def test_comment6(self):
        self.assertTrue(TestLexer.checkLexeme("//This is a line comment", "<EOF>", 164))
    def test_comment5(self):
        self.assertTrue(TestLexer.checkLexeme("""/*Tong 2 so la*/c = a + b""","c,=,a,+,b,<EOF>",165))
    def test_comment7(self):
        self.assertTrue(TestLexer.checkLexeme("//////////////(*has no special meaning in comments that begin with*){}", "<EOF>", 166))
    def test_comment8(self):
        self.assertTrue(
            TestLexer.checkLexeme("/*//////////////(*has no special meaning in comments that begin with*){}*/", "<EOF>",
                                  167))
    def test_comment9(self):
        self.assertTrue(TestLexer.checkLexeme("/ //abcd", "/,<EOF>", 168))

    def test_Unclosedstring1(self):
        self.assertTrue(TestLexer.checkLexeme("\"ABC", "Unclosed String: ABC", 169))
    def test_Unclosedstring2(self):
        self.assertTrue(TestLexer.checkLexeme(" \"\\t ","Unclosed String: \\t ",170))
    def test_lexer56(self):
        self.assertTrue(TestLexer.checkLexeme(""""abc""", """Unclosed String: abc""", 171))

    # test Error Token
    def test_lexer50(self):
        self.assertTrue(TestLexer.checkLexeme("^", "Error Token ^", 172))
    def test_lexer51(self):
        self.assertTrue(TestLexer.checkLexeme("?", "Error Token ?", 173))
    def test_error_token(self):
        self.assertTrue(TestLexer.checkLexeme("abc?def","abc,Error Token ?",174))
    def test_array1(self):
        self.assertTrue(TestLexer.checkLexeme("a[99] &", "a,[,99,],Error Token &", 175))
    def test_lexer20(self):
        self.assertTrue(TestLexer.checkLexeme("\\", "Error Token \\", 176))
    def test_lexer21(self):
        self.assertTrue(not TestLexer.checkLexeme("abcd_1234", "abcd,1234,<EOF>", 177))
    def test_lexer196(self):
        self.assertTrue(TestLexer.checkLexeme("""error#""", """error,Error Token #""", 196))
    def test_separator1(self):
        self.assertTrue(TestLexer.checkLexeme("[ba[b]a[ba]",                                       "[,ba,[,b,],a,[,ba,],<EOF>",178))
    def test_separator2(self):
        self.assertTrue(TestLexer.checkLexeme("{abc}(efk)", "{,abc,},(,efk,),<EOF>", 179))
    def test_separator3(self):
        self.assertTrue(
            TestLexer.checkLexeme("int a,b;", "int,a,,,b,;,<EOF>", 180))
    def test_separator4(self):
        self.assertTrue(TestLexer.checkLexeme("abc;abc;", "abc,;,abc,;,<EOF>", 181))
    def test_all1(self):
        self.assertTrue(TestLexer.checkLexeme("_", "_,<EOF>", 182))

    def test_all6(self):
        self.assertTrue(TestLexer.checkLexeme("1[2]", "1,[,2,],<EOF>", 183))
    def test_array1(self):
        self.assertTrue(TestLexer.checkLexeme("array [1 + 3]", "array,[,1,+,3,],<EOF>", 184))
    def test_array2(self):
        self.assertTrue(TestLexer.checkLexeme("int a[5],b[5];","int,a,[,5,],,,b,[,5,],;,<EOF>", 185))
    def test_array3(self):
        self.assertTrue(TestLexer.checkLexeme("string a;float[] foo(){}","string,a,;,float,[,],foo,(,),{,},<EOF>", 186))
    def test_array4(self):
        self.assertTrue(TestLexer.checkLexeme("foo()[99]", "foo,(,),[,99,],<EOF>", 187))
    def test_array5(self):
        self.assertTrue(TestLexer.checkLexeme("int[] foo(int a, float b[])", "int,[,],foo,(,int,a,,,float,b,[,],),<EOF>", 188))

    def test_pointer1(self):
        self.assertTrue(TestLexer.checkLexeme("int[] main(int a[])","int,[,],main,(,int,a,[,],),<EOF>",1991))
    def test_lexer189(self):
        self.assertTrue(TestLexer.checkLexeme("foo(1)[2+x]", "foo,(,1,),[,2,+,x,],<EOF>", 189))
    def test_lexer190(self):
        self.assertTrue(TestLexer.checkLexeme("a[b[2]] +3;", "a,[,b,[,2,],],+,3,;,<EOF>", 190))
    def test_lexer191(self):
        self.assertTrue(TestLexer.checkLexeme("void main ();", "void,main,(,),;,<EOF>", 191))
    def test_lexer192(self):
        self.assertTrue(TestLexer.checkLexeme("float foo();", "float,foo,(,),;,<EOF>", 192))

    def test_lexer4(self):
        self.assertTrue(TestLexer.checkLexeme("if (a==b) return c;", "if,(,a,==,b,),return,c,;,<EOF>", 193))
    def test_lexer5(self):
        self.assertTrue(TestLexer.checkLexeme("int a,b,c; a = b = c;","int,a,,,b,,,c,;,a,=,b,=,c,;,<EOF>", 194))
    def test_lexer6(self):
        self.assertTrue(TestLexer.checkLexeme("(a || b)[4]", "(,a,||,b,),[,4,],<EOF>", 195))
    def test_lexer7(self):
        self.assertTrue(TestLexer.checkLexeme("""`#BKHCMUT""","""Error Token `""",197))
    def test_lexer8(self):
        self.assertTrue(TestLexer.checkLexeme("""&BKHCMUT&&&&&&&&""","""Error Token &""",198))
    def test_lexer9(self):
        self.assertTrue(TestLexer.checkLexeme("""$BKHCMUT""","""Error Token $""",199))


    def test_string1(self):
        self.assertTrue(TestLexer.checkLexeme(""" "mmmm" ""","""mmmm,<EOF>""",1001))
    def test_string2(self):
        self.assertTrue(TestLexer.checkLexeme("\"\\nABC ABC\"", "\\nABC ABC,<EOF>", 1002))
    def test_string3(self):
        self.assertTrue(TestLexer.checkLexeme("\"ABC\\\\ABC\"", "ABC\\\\ABC,<EOF>", 1003))
    def test_string4(self):
        self.assertTrue(TestLexer.checkLexeme("\"ABC\\bABC\"", "ABC\\bABC,<EOF>", 1004))
    def test_string5(self):
        self.assertTrue(TestLexer.checkLexeme("\"\\nABC ABC\"", "\\nABC ABC,<EOF>", 1005))
    def test_string6(self):
        self.assertTrue(TestLexer.checkLexeme("\"ABC\\tABC\"", "ABC\\tABC,<EOF>", 1006))
    def test_string7(self):
        self.assertTrue(TestLexer.checkLexeme("\"ABC\\rABC\"", "ABC\\rABC,<EOF>", 1007))
    def test_string8(self):
        self.assertTrue(TestLexer.checkLexeme("\"ABC\\\'ABC\"", "ABC\\\'ABC,<EOF>", 1008))
    def test_string9(self):
        self.assertTrue(TestLexer.checkLexeme("\"ABC\\\"ABC\"", "ABC\\\"ABC,<EOF>", 1009))





import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):

    def test_int(self):
        """Simple program: int main() {} """
        input = """void main() {putInt(100);}"""
        expect = "100"
        self.assertTrue(TestCodeGen.test(input, expect, 500))

    def test_int_ast(self):
        input = Program([
            FuncDecl(Id("main"), [], VoidType(), Block([
                CallExpr(Id("putInt"), [IntLiteral(5)])]))])
        expect = "5"
        self.assertTrue(TestCodeGen.test(input, expect, 501))

    def test_int_ln(self):
        input = """void main() {putIntLn(2020);}"""
        expect = "2020\n"
        self.assertTrue(TestCodeGen.test(input, expect, 502))

    def test_float1(self):
        input = Program([
            FuncDecl(Id("main"), [], VoidType(), Block([
                CallExpr(Id("putFloat"), [FloatLiteral(6.0)])]))])
        expect = "6.0"
        self.assertTrue(TestCodeGen.test(input, expect, 503))

    def test_float2(self):
        input = """
        void main(){
            putFloat(1.123456E7);
        }
        """
        expect = "1.123456E7"
        self.assertTrue(TestCodeGen.test(input,expect,504))


    def test_put_float3(self):
        input = """void main() {putFloat(20.202);}"""
        expect = "20.202"
        self.assertTrue(TestCodeGen.test(input, expect, 505))

    def test_put_float4(self):
        input = """void main() {putFloatLn(20.202);}"""
        expect = "20.202\n"
        self.assertTrue(TestCodeGen.test(input, expect, 506))

    def test_string1(self):
        input = Program([
            FuncDecl(Id("main"), [], VoidType(), Block([
                CallExpr(Id("putString"), [StringLiteral('Year2020')])]))])
        expect = "Year2020"
        self.assertTrue(TestCodeGen.test(input, expect, 507))

    def test_string2(self):
        input = Program([
            FuncDecl(Id("main"), [], VoidType(), Block([
                CallExpr(Id("putStringLn"), [StringLiteral('Happy')]),
                CallExpr(Id("putString"), [StringLiteral('Year2020')])
            ]))])
        expect = "Happy\nYear2020"
        self.assertTrue(TestCodeGen.test(input, expect, 508))

    def test_bool1(self):
        input = """
            void main () {
                putBoolLn(true);
            }"""
        expect = "true\n"
        self.assertTrue(TestCodeGen.test(input, expect, 509))

    def test_bool2(self):
        input = """
        void main()
        { 
            boolean a,b;
            a = true;
            b = false;
            putBool(a);
            putBool(b);
        }
        """
        expect = """truefalse"""
        self.assertTrue(TestCodeGen.test(input,expect,510))

    def test_bool_or_op(self):
        input = """void main(){
            putBoolLn(true||false);
            putBool(true&&false);
        }"""
        expect = "true\nfalse"
        self.assertTrue(TestCodeGen.test(input, expect, 511))

    def test_bool_op_1(self):
        input = """void main(){
            int a, b; a = 4, b = 5;
            putBool(a<=b);
        }"""
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 512))

    def test_bool_in_op_2(self):
        input = """void main(){
            int a, b; a = 4, b = 5;
            putIntLn(a<=b);
            putInt(a>b);
        }"""
        expect = "1\n0"
        self.assertTrue(TestCodeGen.test(input, expect, 513))

    def test_boolean_op(self):
        input = """
        void main() {
            putStringLn("toi");
            putStringLn("di");
            putString("hoc");
        }
        """
        expect = "toi\ndi\nhoc"
        self.assertTrue(TestCodeGen.test(input, expect, 514))

    def test_int_mod(self):
        input = """void main() {
            int i; i = 10;
            putInt(i % 3);
        }"""
        expect = "1"
        self.assertTrue(TestCodeGen.test(input,expect,515))


    def test_add_sub_int2(self):
        input = """void main() {
            int i;
            i = 0;
            putInt(i+2019);
            putInt(i-2020);
        }"""
        expect = "2019-2020"
        self.assertTrue(TestCodeGen.test(input,expect,516))

    def test_add_sub_int3(self):
        input = """void main(){
 
            putInt(1*(2+(3-(4+5))));
        }"""
        expect = "-4"
        self.assertTrue(TestCodeGen.test(input, expect, 517))

    def test_mul_int1(self):
        input = """void main() {
            int i; i = 4;
            putInt(i * 5);
        }"""
        expect = "20"
        self.assertTrue(TestCodeGen.test(input,expect,518))

    def test_mul_div_int3(self):
        input = """void main() {
            int i, j;
            i = 2; j = 6;
            putIntLn(i * 5);
            putInt(j/i);
        }"""
        expect = "10\n3"
        self.assertTrue(TestCodeGen.test(input,expect,519))

    def test_binary_float_1(self):
        input = """void main() {
            float i, j;
            i = 2.0; j = 6.5;
            putFloatLn(i * j);
            putFloat(i+j);
        }"""
        expect = "13.0\n8.5"
        self.assertTrue(TestCodeGen.test(input,expect,520))

    def test_many_add_float(self):
        input = """void main(){
            putFloat(1+1.1+2+2.345);
        }"""
        expect = "6.4449997"
        self.assertTrue(TestCodeGen.test(input, expect, 521))

    def test_div_int(self):
        input = """void main() {
            int a;
            a = 11;
            putIntLn(a / 4);
        }"""
        expect = "2\n"
        self.assertTrue(TestCodeGen.test(input,expect,522))

    def test_mod_int4(self):
        input = """void main() {
            int a;
            a = 11;
            putInt(a % 4);
        }"""
        expect = "3"
        self.assertTrue(TestCodeGen.test(input,expect,523))

    def test_mul_div_float(self):
        input = """void main(){
            putFloat(5.5/2*3);
        }"""
        expect = "8.25"
        self.assertTrue(TestCodeGen.test(input, expect, 524))

    def test_mul_int_float1(self):
        input = """
            void main() {
                putIntLn(2*3);
                putFloatLn(2.3*3.2);
                putFloatLn(4.5* 5);
                }"""
        expect = "6\n7.36\n22.5\n"
        self.assertTrue(TestCodeGen.test(input, expect, 525))

    def test_bool_and(self):
        input = """
            void main() {
                putBoolLn(true && true && true);
                putBoolLn(true && false && true);
                }"""
        expect = """true\nfalse\n"""
        self.assertTrue(TestCodeGen.test(input, expect, 526))

    def test_bool_or(self):
        input = """
            void main() {
                putBoolLn(true || true && false);
                putBoolLn(true || false || true);
                }"""
        expect = """true\ntrue\n"""
        self.assertTrue(TestCodeGen.test(input, expect, 527))

    def test_local_var_multil1(self):
        input = """
                    void main() {
                        int a; float b; string c; boolean d;
                        a = 5; b =5.6;
                        c = "HK22019"; d = true;
                        putIntLn(a);
                        putFloatLn(b);
                        putStringLn(c);
                        putBool(d);
                        }"""
        expect = """5\n5.6\nHK22019\ntrue"""
        self.assertTrue(TestCodeGen.test(input, expect, 528))

    def test_float_scope(self):
        input = """
        int i, j;
        void main(){
            int a, b, t;
            i = 10;
            {
                float i;  i = 111.222;
                putFloat(i);
            }
            i = 333;
            putIntLn(333);
        }
        """
        expect = "111.222333\n"
        self.assertTrue(TestCodeGen.test(input,expect,529))


    def test_if1(self):
        input = """
            int a;
            void main(){
                if (true) putInt(3);
                else putInt(2);
            }
            """
        expect = "3"
        self.assertTrue(TestCodeGen.test(input,expect,530))

    def test_if2(self):
        input = """void main() {
            int i;
            i = 1;
            if(i >= 5.5){
                putString("pass");
            }
        }"""
        expect = ""
        self.assertTrue(TestCodeGen.test(input,expect,531))

    def test_if3(self):
        input = """void main() {
            int i;
            i = 1;
            if(i >= 5){
                putString("pass");
            }
            else
            { putString("fail");}
        }"""
        expect = "fail"
        self.assertTrue(TestCodeGen.test(input,expect,532))

    def test_if4(self):
    	input = """
        void main() {
            int x;
            x = 2;
            if (x >= 3)
                x = 3;
            else
                x = 5;
            putIntLn(x);
        }"""
    	expect = "5\n"
    	self.assertTrue(TestCodeGen.test(input,expect,533))

    def test_if5(self):
    	input = """
        void main() {
            int x;
            x  = 1 ;
            if (x == 9)
                putFloat(9.5);
            else
                putFloat(1.5);
        }"""
    	expect = "1.5"
    	self.assertTrue(TestCodeGen.test(input,expect,534))


    def test_unary_neop1(self):
            input = """
            void main(){
                int a, b, c;
                a = 5 ; b = -9
                c = a + b;
                putInt(c);
                return;
            }"""
            expect = "-4"
            self.assertTrue(TestCodeGen.test(input,expect,535))

    def test_unary_neop2(self):
            input = """
            void main(){
                boolean a;boolean b;
                a = true; b = false;
                if (b != a){
                    putString("aaa");
                }
                return;
            }"""
            expect = "aaa"
            self.assertTrue(TestCodeGen.test(input,expect,536))

    def test_float_var_op(self):
        input = """void main(){
            a=2;
            b=3;
            c=a*b+b%a;
            putFloat(c+b);
        }
        int a, b;
        float c;"""
        expect = "10.0"
        self.assertTrue(TestCodeGen.test(input, expect, 537))

    def test_mull_ass(self):
        input = """
                int a,b,c;
                void main() {
                    a = b = 20; c = 20;
                    putIntLn(a);
                    putIntLn(b);
                    putIntLn(c);
                    }"""
        expect = """20\n20\n20\n"""
        self.assertTrue(TestCodeGen.test(input, expect, 538))

    def test_int_mul1(self):
        input = """void main() {
            int a;
            a = 5;
            putInt(a * 5);
        }"""
        expect = "25"
        self.assertTrue(TestCodeGen.test(input,expect,539))

    # upload nop test -> tiep tuc them de nop

    def test_block_if_simple1(self):
    	input = """
        int i,j;
        void main() {
            i = 3;
            j = 0;
            if (i <= 6){
                i = i + 1;
                j = i - 3;
            }
            putIntLn(i+j);
        }"""
    	expect = "5\n"
    	self.assertTrue(TestCodeGen.test(input,expect,540))


    def test_for(self):
        input = """
        void main(){
            int i, , t;
            t = 0;
            for (i = 0; i< 10 ; i= i+1){
                if (t > 21) break;
                if (i % 3==0) continue;
                t = t + i;
            }
            putInt(t);
        }
        """
        expect = "28"
        self.assertTrue(TestCodeGen.test(input,expect,541))


    def test_for_with_break(self):
        input = """
            void main(){
                int i, s;
                s = 0;
                for(i=1;i<10;i = i + 1){
                    s = s + i;
                    if(s > 30)
                        break;
                }
                putInt(s);
            }

        """
        expect = "36"
        self.assertTrue(TestCodeGen.test(input, expect, 542))

    def test_for1(self):
        input = """
        void main()
        {   int i;
            i = 0;
            for(i=1;i<10;i = i + 1)
            {
                putInt(i);
            }
        }
        """
        expect = "123456789"
        self.assertTrue(TestCodeGen.test(input, expect, 543))

    def test_for_break1(self):
        input ="""
        void main(){
            int i;
            for(i = 0; i <= 10 ; i = i + 1){
                putInt(i);
                break;
            }                   
        }
        """
        expect = "0"
        self.assertTrue(TestCodeGen.test(input,expect,544))

    def test_for_break2(self):
    	input = """
        void main() {
            int i;
            int a;
            a = 0 ;
            for (i = 0 ; i <= 10; i = i + 1 ){
                if (i == 5)
                {
                    break;
                }
                a =  a + 1; 
            }
            putInt(a);
        }"""
    	expect = "5"
    	self.assertTrue(TestCodeGen.test(input,expect,545))


    def test_for_Continue(self):
    	input = """
        void main() {
            int i;
            int a;
            a = 0 ;
            for (i = 0 ; i <= 10; i=i+1 ){
                if (i == 5){
                    continue;
                }
                a = a + 4; 
            }
            putInt(a);
        }"""
    	expect = "44"
    	self.assertTrue(TestCodeGen.test(input,expect,546))


    def test_break_continu1(self):
        input = """
        int i;
        void main()
        {
            for (i = 0 ; i <= 10; i=i+1 )
            {
                if (i > 5)  {break;}
            putInt(i);
            }

            for (i = 0 ; i <= 10; i=i+1 )
            {
                if i >= 5 { continue;}
                else {putInt(i);}
            }
        }
        """
        expect = "01234501234"
        self.assertTrue(TestCodeGen.test(input, expect, 547))

    def test_for_break3(self):
        input = """
            void main() {
                int i;
                for (i = 0; i < 15; i = i +1) {
                    if (i == 10) { break; }
                    putInt(i);
                }
            }
        """
        expect = "0123456789"
        self.assertTrue(TestCodeGen.test(input, expect, 548))

    def test_for_loop(self):
        input = """void main(){
            int i, j, t;
            t = 0;
            for (i = 0; i< 10;i=i+1){
                for (j = 0; j< i - 1; j=j+1){
                    if (i + j > 23) break;
                    if (j % 2==0) continue;
                    t = t + 1;
                }
                if (t > 50) break;
                if (i % 3 != 0) continue;
                t = t + 2;
            }
            putIntLn(t);
        }
        """
        expect = "54\n"
        self.assertTrue(TestCodeGen.test(input,expect,549))

    #dowhile


    def test_dowhile(self):
        input = """void main() {
            int i; i= 0;
            do
                i = i +1;
            while(i < 20);
            putInt(i);
        }"""
        expect = "20"
        self.assertTrue(TestCodeGen.test(input,expect,550))

    def test_dowhile1(self):
        input = """void main() {
            int i; i= 1;
            int a;
            a = 1;
            do {
                a = a+ 1;
                i = i * a;
            }
            while(a <10);
            putInt(i);
        }"""
        expect = "3628800"
        self.assertTrue(TestCodeGen.test(input,expect,551))


    def test_dowhile2(self):
        input = """void main() {
            int i; i = 1;
            int j; j = 1;
            do {
                i = i + 2;
                j = i + ((i - 2)*3)%4;
            }
            while(i <10);
            putInt(j);
        }"""
        expect = "14"
        self.assertTrue(TestCodeGen.test(input,expect,552))

    '''def test_fibonaci(self):
        input = """
        int fn(int n)
        {
            if (n < 0) { return -1;}
            else if (n == 0) {return 0;}
            else if (n == 1) { return 1;}
            else return fn(n - 1) + fn(n - 2);
        }

        void main(){
        int i;
        {
            for (i = 0; i < 7; i = i + 1)
                putIntLn(fn(i));
        }}
        """
        expect = "0\n1\n1\n2\n3\n5\n8\n13\n"
        self.assertTrue(TestCodeGen.test(input, expect, 565))'''

    def test_dowhile3(self):
        input = """void main(){
            do
                putInt(12);
            while(false);
        }"""
        expect = "12"
        self.assertTrue(TestCodeGen.test(input, expect, 553))

    def test_dowhile4(self):
        input = """
        void main(){
            int i,s;
            i=s=0;
            do
            {
                s = s+i;
                i=i+1;
            }while (i<=10);
            s=s*2;
            putInt(s);
            return;
        }
        """
        expect = "110"
        self.assertTrue(TestCodeGen.test(input,expect,554))

    def test_dowhile5(self):
        input = """void main() {
            int i; i= 0;
            do
                i = i +1;
            while(i<10);
            putInt(i);
        }"""
        expect = "10"
        self.assertTrue(TestCodeGen.test(input,expect,555))

    def test_dowhile6(self):
        input = """
        void main() {
            int i; i = 0 ;
            do{
                i = i + 1;
                if (i == 2){
                    continue;
                }
                putIntLn(i);                

            }
            while(i < 4);
        }"""
        expect = "1\n2\n3\n4\n"
        self.assertTrue(TestCodeGen.test(input, expect, 556))

    def test_for_dowhile(self):
        input = """
            void main() {
                     int i;
                      for( i =1; i < 10; i = i+1)
                        do{
                            putIntLn(i);
                            i = i*2;
                       }
                        while( i< 7);
                       putIntLn(i);
              }
        """
        expect = """1\n2\n4\n9\n19\n"""
        self.assertTrue(TestCodeGen.test(input, expect, 557))

    def test_break_in_loop(self):
        input = """
            void main() {
                int i,j;
                i =j =0;
                for (i =0 ;true; i = i + 1) {
                    if (i == 3)
                        break;
                    for (j = 0; true ;j = j + 1) {
                        if (j == 2) break;
                        putInt(j);
                    }
                }
            }
        """
        expect = "010101"
        self.assertTrue(TestCodeGen.test(input, expect, 558))

    def test_simple_put_int(self):
        input = """void main(){
            2;
            putInt(2*(3+(2-(3+2))));
        }"""
        expect = "0"
        self.assertTrue(TestCodeGen.test(input, expect, 559))

    def test_dowhile_break(self):
        input = """
            void main(){
                int a;
                a = 10;
                do{ putInt(a);
                    a = a + 1;
                    if(a > 15)
                        {break;}
                 
                }while(a < 20);
                
            }
        """
        expect = "101112131415"
        self.assertTrue(TestCodeGen.test(input, expect, 560))

    def test_stmt_block1(self):
        input = """
        void main() {
            if (true) 
                if(true){ 
                    putInt(2);

                    if (true) {
                        putInt(3);
                    } 
                    else {
                        putBool(false);
                    }
                }
            else 
                putString("string");
        }
        """
        expect = "23"
        self.assertTrue(TestCodeGen.test(input, expect, 561))


    def test_var_in_block1(self):
        """Simple program: int main() {} """
        input = """
            int a,b,c;
            void main() {
               a = 0;
               {
                    int a; a = 19;
                    putIntLn(a);
                }
                {
                    float a; a = 20;
                    putFloatLn(a);
                }
            }"""
        expect = """19\n20.0\n"""
        self.assertTrue(TestCodeGen.test(input, expect, 562))

    def test_return_in_func(self):
            input = """
            void func(){
                putFloat(1.5);
                return;
            }
            void main(){
                func();
                return;
            }"""
            expect = "1.5"
            self.assertTrue(TestCodeGen.test(input,expect,563))


    def test_block_scope(self):
        input = """
            void main(){
                int a; float b;
                a = 1;
                putInt(a);
                {
                    float a;
                    int b;
                    a = 1.5; b = 3;
                    putFloat(a+b+3.45+7);
                }
                {
                    boolean a ; boolean b;
                    b = true; a = b;
                    putBool(a);
                }
                a = a + 6 - 9 ;
                putInt(89);
            }
        """
        expect = "114.95true89"
        self.assertTrue(TestCodeGen.test(input, expect, 564))

    def test_dowhile_break(self):
        input = """
            void main(){
                int a;
                a = 10;
                do{ putInt(a);
                    a = a + 1;
                    if(a > 15)
                        {break;}

                }while(a < 20);

            }
        """
        expect = "101112131415"
        self.assertTrue(TestCodeGen.test(input, expect, 565))












import unittest
from TestUtils import TestParser

class ParserSuite(unittest.TestCase):
    def test_simple_program(self):
        """Simple program: int main() {} """
        input = """int main() {}"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,201))

    def test_more_complex_program(self):
        """More complex program"""
        input = """int main () {
            putIntLn(4);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,202))
    
    def test_wrong_miss_close(self):
        """Miss ) int main( {}"""
        input = """int main( {}"""
        expect = "Error on line 1 col 10: {"
        self.assertTrue(TestParser.checkParser(input,expect,203))

    def test_var_decl4(self):
        input = """int a;"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 204))

    def test_var_decl5(self):
        input = """int main()
         {  int x,y,z;}
       """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 205))

    def test_var_decl6(self):
        input="""string a[6];"""
        expect ="successful"
        self.assertTrue(TestParser.checkParser(input, expect,206))

    def test_var_decl7(self):
        input="""int a,b,c; float d; string a[6];"""
        expect ="successful"
        self.assertTrue(TestParser.checkParser(input, expect,207))
    def test_simpleprogram1(self):
        input="""int A[10]; string st;
            void main() {}"""
        expect= "successful"
        self.assertTrue(TestParser.checkParser(input,expect,208))
    def test_simpleprogram2(self):
        input="""int a[10]; string st;
            void main( {}"""
        expect= "Error on line 2 col 23: {"
        self.assertTrue(TestParser.checkParser(input,expect,209))

    def test_simplefunc(self):
        input = """void foo() { int a; string b; float c;}"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 210))

    def test_simplefunc1(self):
        input = """int a; string b; float c; int foo()"""
        expect = "Error on line 1 col 35: <EOF>"
        self.assertTrue(TestParser.checkParser(input, expect, 211))

    def test_function_decl1(self):
        input = """int foo(); int a,b {}"""
        expect = "Error on line 1 col 9: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 2111))
    #

    def test_simpleprogram2(self):
        input="""int a[10], int c; string st;
            void main() {} """
        expect= "Error on line 1 col 11: int"
        self.assertTrue(TestParser.checkParser(input,expect,212))

    def test_simpleprogram3(self):
        input="""float a[3];int c; string st;
            void main() {}"""
        expect= "successful"
        self.assertTrue(TestParser.checkParser(input,expect,213))

    def test_simpleprogram4(self):
        input="""float a[];int c; string st;
            void main() {}"""
        expect= "Error on line 1 col 9: ;"
        self.assertTrue(TestParser.checkParser(input,expect,214))

    def test_function_decl3(self):
        input = """int tong(int a, int c, float b) {}"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 215))

    def test_function_decl4(self):
        input = """int tong() {int a, float b = 1.0}"""
        expect = "Error on line 1 col 19: float"
        self.assertTrue(TestParser.checkParser(input, expect, 216))

    def test_var_decl_int(self):
        input = """int i[5];"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 217))
        # int i [ 5 ] ; // CORRECT

    def test_var_decl_int2(self):
        input = """int i[];"""
        expect = "Error on line 1 col 7: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 218))
        # int i [] ; // ERROR

    def test_var_decl_int3(self):
        input="int x, y = 10; string abc;"
        expect="Error on line 1 col 9: ="
        self.assertTrue(TestParser.checkParser(input,expect,219))
        # Not support variable initialization
    
    def test_var_decl4(self):
        input = """int main(){
        float x; int y,z;
            { x = y * z;}
        int i; int a[5];}"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 220))

    def test_simpleprogram5(self):
        input="""int foo(){}
                void main(){}"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,221))

    def test_simpleprogram6(self):
        input="""void foo(int a,float b,string c ,boolean d){int i; i = a + 3;}"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,222))

    def test_simpleprogram7(self):
        input = """boolean a_; string b_; void main() {{{/*nothing*/}}}"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 223))

    def test_statement_assign(self):
        input = """int main()
       { int x,y,z;
        {
                x = y;
                z = x + y * 5;
        }}"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 224))

    def test_statement_assign1(self):
        input = """int main()
       { int x,y,z;
        {
                x = ;
                z = x + y * 5;
        }}"""
        expect = "Error on line 4 col 20: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 224))



    def test_statement_if2(self):
        input="""void main(){
        float x,y,z;
        {if (x>y) {x = x + 10; y = y * 5;}}}"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect, 225))

    def test_statement_if3(self):
        input="""int main()
        {
            int number;
            printf("Enter an integer: ");
            // True if the remainder is 0
            if  (number%2 == 0) 
            {
                printf("%d is an even integer.",number);
            }
            else
            {
                printf("%d is an odd integer.",number);
            }
            return 0;
        }"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect, 226))
    
    def test_statement_ifelse(self):
        input="""int main()
        {
        int x,y,z;
         {  
          if (x>y) 
          { 
            y = x * 5 ; z = y + 10;
          } 
          else 
           { 
             z = x * y;
        }}}"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect, 227))

    def test_simple_program25(self):
        input="""int foo(int a, float b){
                if (b= 10.0)
                   { continue;}
                else
                   { break;}
                return a;
                }
                void main() {}"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,228))

    def test_if_statement1(self):
        input="""int a,b;void main(){
            if(a>b) c[0]=1; 
        }"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,229))

    def test_if_statement_con(self):
        input = """int main()
        {int toan, ly, hoa;
        {
            if (x + y + z >= 24)  continue;
        }}"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 230))

    def test_arraypointer1(self):
        input = """int[] foo(int a, float b[]) {int c[3]; if (a>0) foo(a-1,b); return c; }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 231))

    def test_local_variable1(self):
        input = """int foo ( int a , float b[ ] )
        {
        boolean c ;
        int i ;
        i = a + 3 ;
        if ( i >0) {
        int d ;
        d = i + 3 ;
        putInt(d) ;
        }
        return i ;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 232))



    def test_do_while1(self):
        input = """int main()
        {
            int number, sum;
            // the body of the loop is executed at least once
            do
            {
                sum = number;
            }
            while(number != 0.0);
            printf("Sum = %.2lf",sum);
            return 0;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 233))

    def test_do_while2(self):
        input = """int main() 
        { 
            int i; 
            do { 
                printf("GFG\n"); 
                i = 5 ;
                i = i + 1; 
            } while (i < 10); 
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 234))


    def test_do_while2_nested3(self):
        input = """int main()
        {
            int i,j;
            do
            {
                j=1;
                do
                {
                    printf("*");
                    j = j + 1;
                }while(j <= i);
                i = i + 1;
                printf("\n");
            }while(i <= 5);
            return 0;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 235))

    def test_do_while2_nested4(self):
        input = """int main()
        {
            int i,j,n;
            for(i=2;i <= n; i = i + 1)
            {
                for(j=2; j<= 100 ; j = j + 1)
                {
                    if(i%j==0)
                    {
                        printf("%d gia tri\n",i);
                        break;
                    }    
                }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 236))

    def test_do_while2_nested5(self):
        input = """int main()
           {
               int i,j,n, sum;
               for(i=2;i <= 99; i = i + 1)
               {
                   for(j=2; j<= 100 ; j = j + 1)
                   {
                       for (n = 1; n <= 10; n = n + 1)
                        { 
                            sum = i * j * n;
                        }
                   }
               }
           }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 237))

    def test_continue_statement1(self):
        input="""void foo(){
            for(i=0;i<100;i=i+1){
                if(i % 13==0) break;
                else continue;
            }
        }"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,238))

    def test_continue_statement2(self):
        input="""int main () {
           /* local variable definition */
           int a;
           /* do loop execution */
           do {  
              if( a == 15) {
                 /* skip the iteration */
                 a = a + 1;
                 continue;
              }	
              printf("value of a: %d\n", a);
              a = a + 1; 
           } while( a < 20 );
           return 0;
            }"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,239))

    def test_statement_assign2(self):
        input = """int x,y,z;
        void main()  
        {
          x = y = z = 5;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 240))
    
    def test_if_statement_e(self):
        input = """void main()
    {   int x;
        if (x)  else {} 
    }"""
        expect = "Error on line 3 col 16: else"
        self.assertTrue(TestParser.checkParser(input, expect, 241))

    def test_dowhile1(self):
        input="""void main(){
            int a,b, c[5],d;int x,y; string z;
            do x=y + 0.5;
            while x < 20;
        }"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,242))

    def test_dowhile2(self):
        input="""void main(){
            do  x = x + 1;
                {
                    if(x =100) return 0 ;
                }
            while (x > 50 && x <= 100);
        }"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,243))

    def test_expr_p1(self):
        input="""void main(){
            putString("check\\n");
            putInt(i);
            foo1(a,b[1])[a+i[3]];
        }"""
        expect= "successful"
        self.assertTrue(TestParser.checkParser(input,expect,244))

    def test_statement_break3(self):
        input = """int x,y,z;
        void main()
           { 
               y= 5; z =100;
               for (x = y +1 ; x <= 150; x= x + 1)
               {
                x = y * z;
                }
                break;
           }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 245))

    def test_while23(self):
        input = """void main()
        {
            n =10;
            for (i= 6 ; i <= n; i = i + 2)
                a  = a*b+4*7+2*5-1;
            do
                n=n*n;
            while (i < 20);
            }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 246))


    def test_parser_return1(self):
        input = """float foo()
            {
                if (a) return 2.3; 
                else return 2;
            }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 247))

    def test_parser_return2(self):
        input = """ 
        int test()
        {
            n = foo1(foo2(),a[2],x+y);
            return a + 2018;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 248))

    def test_parser_return3(self):
        input = """int x,y;
        int callfunc()
        {
            n = foo1(foo2(),a[2],x+y);
            return func2(a);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 249))

    def test_parser_return4(self):
        input = """int sum;
        int main() 
        { 
            num = sum(); 
            printf("\nSum of two given values = %d", num); 
            return 0; 
        } 
        int sum() 
        { 
            a = 50; b = 80; sum; 
            sum = sqrt(a) + sqrt(b); 
            return sum; 
        } """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 250))

    def test_expression1(self):
        input = """void main()
        { 
            a = 5 || b;
        }
        int a , b;"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 251))

    def test_expression2(self):
        input = """float a,b,c;
        void main(){ 
                a = b;
                a != b;
                a > b;
                a < b;
                a >= b;
                a <= b;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 252))

    def test_expression3(self):
        input = """ 
        int main()
        {
            n =10;
            for (i = 6 ; i<= 10; i = i + 1)
                a = a*b+4*7+2*5-1;
                do
                    n=n*n;
                while (n <20);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 253))

    def test_expression4(self):
        input = """ 
        void main()
        {
            n= 1 || a = b && c;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 254))

    def test_expression5(self):
        input = """void main()
        {
            n= 1 || a = b && c;
            i = 1;
            foo(1 , 2 );
            i + 2;
            100;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 255))

    def test_expression6(self):
        input = """int a,b,c;
        void main()
        {
        foo (3 , a+1, m(2));
        c = a % b;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 256))

    def test_expression7(self):
        input = """ 
        int a,b,c,i,j,k[5];
            void main(){
                a[foo[i]]=6;
                foo()[j]=k[5];
            }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 257))

    def test_expression8(self):
        input = """void main()
                {
                    foo(1)[2+x] = a[b[4]] +3;
                }
                int a,b,c;
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 258))

    def test_expression9(self):
        input = """int main()
        {
        int a , b , c ; 
        a=b=c=5;
        float f [ 5 ] ;
        if ( a==b) f[0] = 1.0 ;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 259))



    def test_call_function260(self):
        input = """ 
        void main()
        {
            n = foo(a,b,c);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 260))

    def test_call_function261(self):
        input = """int test()
        {
            n = foo1(foo2(),a[2],x+y);
            foo(2)[3+x] = a[b[2]] +3;
            return n;}"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 261))

    def test_call_function262(self):
        input = """ 
       void callfunc(int a[])
        {
            n = foo1(foo2(),a[2],x+y);
            return func2(a);
        }
        int x,y;"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 262))

    def test_idxexpress1(self):
        input = """ 
        int main()
        {
            a =b = c = foo()[3]+foo2() ;
            foo(2)[3+x] = a[b[2]] +3;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 263))

    def test_idxexpress2(self):
        input="""int x,y,z;
          int foo(int a[],int b[])
            {
                z[x[1]+y[2]] = foo1(x[3+x])[6+x] + a[b[2]] +3;
            }"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,264))

    def test_paser1(self):
        input="""int foo(int a, float b){
                for(a = 1; a < 100; a = a + 1 )
                    i = i + 1;
                }
                void main() 
                {  
                }"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,265))

    def test_paser2(self):
        input = """int main()
           {
            do 
            a =b = c = foo()[3]+foo2();
            while (a < 5) ;
           }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 266))

    def test_paser3(self):
        input = """int main()
           {
            do 
            a =b = c = foo()[3]+foo2();
            while (a < 5) ;
            return a = 0;
           }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 267))

    def test_paser4(self):
        input="""int func(int a, int b, int c){
                c = a[b[1]] + 2;
                    return a[0];
                }
                void main() {}"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,268))

    def test_paser5(self):
        input="""void main(int a, float b){}
                void foo1(int x, string y){}
                void foo2(int c){}"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,269))

    def test_paser6(self):
        input="""int i,j;
                void main(int a[],float x){
                    i = 1;
                    return foo(2)[x +3];
                }"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,270))



    # test_for

    def test_for_statement1(self):
        input = """int main() {
          int i;
          for (i = 1; i < 11; i = i + 1)
          {
            printf("%d ", i);
          }
          return 0;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 271))

    def test_for_statement2(self):
        input = """int main()
        {
            int num, count, sum;
            sum = 0;
            for(count = 1; count <= num; count = count + 1)
            {
                sum = sum + count;
            }
            printf("Sum = %d", sum);
            return 0;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 272))

    def test_for_statement3(self):
        input = """int main()
        {  int i,j;
           for (i=0; i<2; i = i + 1)
           {
            for ( j=0; j<4; j = j +1)
            {
               printf("%d, %d\n",i ,j);
            }
           }
           return 0;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 273))

    def test_for_statement4(self):
        input = """void main(){
            for(i=1;i<10;i=i+1){
                swap(x,y);
            }
        }
        void swap(int x,int y){
                x=y;
                y=x;
            }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 274))

    def test_for_statement5(self):
        input = """int a; int main () {
         for( a = 10; a < 20; a = a + 1 ){
          printf("value of a: %d\n", a);
         }
            return 0;
         }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 275))

    def test_for_statement6(self):
        input = """int i, j;int main () {
       for(i = 2; i<100; i = i + 1) {

          for(j = 2; j <= (i/j); j = j + 1) 
          if(!(i%j)) break; // if factor found, not prime
          if(j > (i/j)) printf("%d is prime\n", i);
       }
       return 0;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 276))

    def test_for_statement7(self):
        input = """int i;
        int main() { 
            // loop from 1 to 10  
            for (i = 1; i <= 10; i= i + 1) {  
                // If i is equals to 6,  
                // continue to next iteration  
                // without printing  
                if (i == 6)  
                    continue;  
                else
                    // otherwise print the value of i  
                    printf("%d ", i);  
            }   
            return 0;  
        } """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 277))

    def test_ino_statement7(self):
        input = """void foo ( float a[]){}
        void goo ( float x [ ] ) {
        float y[10] ;
        int z [10] ;
        foo ( x ) ; //CORRECT
        foo ( y ) ; //CORRECT
        foo ( z ) ; //WR
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 278))

    def test_block_statement7(self):
        input = """int foo()
        {
        int a , b , c ;
        a=b=c=5; 
        float f [ 5 ] ;
        if ( a==b) f [ 0 ] = 1.0 ;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 279))

    def test_parser280(self):
        input = """        int main()
        {}
        float foo1()
        {
            a=b+1;
            c=b--1;
        } float a,b;"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 280))

    def test_parser281(self):
        input = """        int main()
        {
         a =b =c = foo()[3]+foo2() ;
        }
        float foo1()
        {
            a=b+1;
            c=b--1;
        } float a,b;"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 281))

    def test_parser282(self):
        input = """void main(){
            {
                float a,b;
                putFloat(a+b);
                {
                    int c;
                    int d;
                    putInt(c+d);
                }
            }

        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 282))

    def test_parser283(self):
        input = """int main()
        {
            if (x>y )
                if (x>5) 
                   x =x+1;
                else
                    if (x<3) 
                        a = a+3;
                    else
                        a = a-3;
            else
                a =a*100;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 283))

    def test_parser284(self):
        input="""int main(){
            do 
                i=getInt();
                {
                    for(i;i<n;i=i+1)
                    {
                      x= a || b || c && d;
                      t = t+1;
                      n = n+1;
                    }
                    break;
                }
                while(i<10);
        }"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,284))

    def test_parser285(self):
        input = """        void main()
        {
        	if ((x<a[4]) && (b< c +7))  
        		x =a[4] +1;
        }
        int foo() {}"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 285))

    def test_parser286(self):
        input = """void main(int x, int z)
        {
            putIntLn(sum(x,y,z));   
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 286))

    def test_parser287(self):
        input="""string b,c; boolean t;int i,j,k[]; 
                void func(string st[],float a){
                  string b,c; boolean t;  return foo(2)[i+3];
                }"""
        expect="Error on line 1 col 32: ]"
        self.assertTrue(TestParser.checkParser(input,expect,287))

    def test_parser288(self):
        input="""void main(){
            for(i=0;i<n;i=i+1){
                if(i%13==0) break;
                else continue;
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,288))

    def test_programm1(self):
        input = """int main()
        {
          int n, c;
          printf("Enter a number\n");
          if (n == 2)
            printf("Prime number.\n");
          else
          {
            for (c = 2; c <= n - 1; c = c +1)
            {
              if (n % c == 0)
                break;
            }
            if (c != n)
              printf("Not prime.\n");
             else
               printf("Prime number.\n");
          }
          return 0;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,289))

    def test_programm2(self):
        input = """void main()
    {
        int array[100], n, c;
        printf("Enter number of elements in array\n");
        printf("Enter %d elements\n", n);
        for (c = 0; c < n; c =c + 1)
            {printf("The array elements are:\n");}
        for (c = 0; c < n; c =c + 1)
            {printf("%d\n", array[c]);}
        return 0;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,290))

    def test_programm3(self):
        input = """int main()
        {
            t1 = 0; t2 = 1;
            printf("Fibonacci Series: ");
            for (i = 1; i <= n; i = i +1)
            {
                printf("%d, ", t1);
                nextTerm = t1 + t2;
                t1 = t2;
                t2 = nextTerm;
            }
            return 0;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,291))

    def test_programm4(self):
        input = """int main()
    {
        int n, i;
        float num[100], sum, average;
        printf("Enter the numbers of elements: ");
       do
        {
            printf("Error! number should in range of (1 to 100).\n");
            printf("Enter the number again: ");
        }
        while (n > 100 || n <= 0);
        for(i = 0; i < n; i = i +1)
        {
            printf("%d. Enter number: ", i+1);
            sum = sum + num[i];
        }
        average = sum / n;
        printf("Average = %.2f", average);
        return 0;
    }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,292))

    def test_programm5(self):
        input = """int main()
        {
            int i, n;
            float arr[100], temp;
            for(i = 0; i < n; i = i +1)
            {
               printf("Enter Number %d: ", i+1);
            }
            for(i = 1; i < n; i =  i = 1)
            {
               if(arr[0] < arr[i]) 
               {
                   temp = arr[0];
                   arr[0] = arr[i];
                   arr[i] = temp;
               }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,293))
    
    def test_programm6_wrong(self):
        input="""int a;int i[1]; i[1]=10;
                void foo(string b,float c){
                }"""
        expect="Error on line 1 col 16: i"
        self.assertTrue(TestParser.checkParser(input,expect,294))

    def test_programm7(self):
        input="""int sum(int a, int b)
        {
             c = a+b;
             return c;
        }
        int main()
        {
            var1 =10;
            var2 = 20;
            var3 = sum(var1, var2);
            printf("%d", var3);
            return 0;
        }"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,295))

    def test_programm8(self):
        input="""int main()               
        {
            float m, n ;
            n = square ( m ) ;                      
        }
        float square (float x)
        {
            float p ;
            p = x * x ;
            return ( p ) ;
        }"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,296))


    def test_programm9(self):
        input=""" int test()
        {
            n = foo1(foo2(),a[2],x+y);
            return a + 2018;
        }
        int main () 
        { 
            printf("%d", sum(10, 5)); 
            return 0; 
        } 
        int sum (int b, int c, int a) 
        { 
            return (a+b+c); 
        } 
               """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,297))


    def test_programmc(self):
        input = """void foo ( ) {
        if (a&&b) return ; //CORRECT
        else return 2 ; //WRONG
        }
        int [ ] foo ( int b [] ) {
        int a [1] ;
        if (a>=b) return a ; //CORRECT
        else return b ; //CORRECT
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 298))

    def test_programmc2(self):
        input = """int i ;
        int f () {
        return 200;
        }
        void main () {
        int main ;
        main = f () ;
        putIntLn (main) ;
        {
        int i ;
        int main ;
        int f ;
        main = f = i = 100;
        putIntLn (main) ;
        putIntLn (f) ;
        }
        putIntLn (main) ;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 299))

    def test_programm10(self):
        input="""int main()
        {
            display();
            display();
        }
        void display()
        {
            int c;
            c = c + 5;
            printf("%d  ",c);
        }"""
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,300))

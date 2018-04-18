import java.io.IOException;

public class main {
	int i;
	int a; 
	int b; 
	int c;
	int d;
	int t;
	int n;

	

    public static void main(String[] args)  {
        int res = (new main()).fibonacci();
    }
    public int fibonacci(){
   i = n - 1;
   a = 1;
   b = 0;
   c = 0;
   d = 1;
   if (n <= 0)
     return 0;
   while (i > 0){
     while (i % 2 == 0){
       t = d*(2*c + d);
       c = c*c + d*d;
       d = t;
       i = i / 2;
     }
     t = d*(b + a) + c*b;
     a = d*b + c*a;
     b = t;
     i--;
   }
   return a + b;
    }
}

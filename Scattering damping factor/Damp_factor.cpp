#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<conio.h>
#define standard_precision double
using namespace std;
#define pi 3.1415926

double Distance(double x1,double x2,double x3,double y1,double y2,double y3)
{double s;
s=sqrt(pow((x1-y1),2)+pow((x2-y2),2)+pow((x3-y3),2));
return s;
}

int main()
{
         FILE *output=NULL;
         output=fopen("data Output.txt","w");
         
         double xstep,rstep,x,y,z,x0,y0,z0;
         double Radius;
         int N,NT;
         
         
         printf("Input particle diameter\n");
         scanf("%lf",&Radius);
         Radius=Radius/2;
         printf("Input output steplength\n");
         scanf("%lf",&rstep);
         printf("Input calculation steplength\n");
         scanf("%lf",&xstep);
         
         NT=Radius*2/rstep;
         
         double num[NT];
         for(N=1;N<=NT;N++)
         {
                           num[N]=0;
         }
         double shell_num;
         double x_0;
         for(x0=0;x0<Radius;x0=x0+xstep)
         {
            shell_num=4*pi/3*(pow((x0+rstep),3)-pow((x0-rstep),3))/pow(rstep,3);                      
         
            for(x=-Radius;x<=Radius;x=x+xstep)
            {
              for(y=0;y<=Radius;y=y+xstep)
              {
                for(z=0;z<=Radius;z=z+xstep)
                {
                  if(Distance(x0,0,0,0,0,0)<=Radius)
                  {
                    if(Distance(x,y,z,0,0,0)<=Radius)
                    {
                      printf("%lf",Distance(x,y,z,x0,0,0));
                      if(Distance(x,y,z,x0,0,0)!=0)
                      {
                        N=Distance(x,y,z,x0,0,0)/rstep;
                        num[N]=num[N]+pow(xstep/Radius,3)*shell_num*4;
                        printf("\nRuning");                
                      }
                    }
                  }
            
                }
              }
            }
          }
         fprintf(output,"r\tdamping\n");
         for(N=1;N<=NT;N++)
         {
                           fprintf(output,"%lf\t%lf\n",N*rstep,num[N]);
         }
         printf("Process end");
         fclose(output);
         getch();
         return 0;
}
  

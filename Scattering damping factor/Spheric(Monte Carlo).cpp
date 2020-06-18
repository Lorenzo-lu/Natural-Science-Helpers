#include<stdio.h>
#include<stdlib.h>
#include<math.h>
//#include<conio.h>
#define standard_precision double
using namespace std;
#define pi 3.1415926



double Prob(int s)
{
       double X;
       X=rand()%s/(s-1.0);
       return X;
}

double directx,directy,directz;//Directions;
double direct()
{
       double i0,i1,ss;
       ss=2;
       while(ss>=1)
       {
       i0=Prob(7000)*2-1.0;
       i1=Prob(7000)*2-1.0;
       ss=i0*i0+i1*i1;
       if(ss<1)
        {
               directx=2*sqrt(1.0-ss)*i0;
               directy=2*sqrt(1.0-ss)*i1;
               directz=1-2*ss;
        }
       }
       return 0;
}

double Distance(double x1,double x2,double x3,double y1,double y2,double y3)
{double s;
s=sqrt(pow((x1-y1),2)+pow((x2-y2),2)+pow((x3-y3),2));
return s;
}


int main()
{
    double x1,y1,z1,x2,y2,z2;
    
    
         FILE *output=NULL;
         output=fopen("data Output.txt","w");
         
         
         double Radius,rstep;
         printf("Input particle diameter\n");
         scanf("%lf",&Radius);
         Radius=Radius/2;
         printf("Input output steplength\n");
         scanf("%lf",&rstep);
         
         int NT,N;
         NT=Radius*2/rstep+1;//N=1时，r=0 
         
         double DPF[NT];
         //double sumwt;//距离为r的点占有的权重不一样，与求面面积正相关，需要加和 
         
         for (N=1;N<=NT;N++)
         {
             DPF[N]=0;
         }
         
         int cycles,i,ii;
         double D;//第一个点距离球心的距离 
         printf("cycles for each radius output?\n");
         scanf("%d",&cycles);
         
         for(N=1;N<=NT;N++)
         {
                        
            //for(i=1;i<=cycles;i++)
            i=1;
            while(i<=cycles)
            {
                
                /* direct();
                D=Prob(1000)*Radius; //printf("%lf\t",Prob(1000));
                x1=D*directx;
                y1=D*directy;
                z1=D*directz;
                */
                
                x1=(2*Prob(1000)-1.0)*Radius;
                y1=(2*Prob(1000)-1.0)*Radius;
                z1=(2*Prob(1000)-1.0)*Radius;
                
                //y1=0;z1=0;
                //x1=D;
                //printf("%lf\t",x1);
                if(Distance(x1,y1,z1,0,0,0)<=Radius)
                {
                    i+=1;
                    for(ii=1;ii<=cycles;ii++)
                    {
                        direct();
                        x2=x1+(N-1)*rstep*directx;
                        y2=y1+(N-1)*rstep*directy;
                        z2=z1+(N-1)*rstep*directz;
                        //printf("%lf\t%lf\t%lf\n",x2,y2,z2);
                        if(Distance(x2,y2,z2,0,0,0)<=Radius)
                        {
                                                            //PF[N]+=1.0/cycles/cycles*D*D;
                                                            DPF[N]+=1.0/cycles/cycles;
                                                            //sumwt+=D*D/cycles/100;
                        }
                    
                    }
                }
                                  
            }
            //DPF[N]=DPF[N]/sumwt;
            //printf("%lf\n",sumwt);
         }
         
         
         
          fprintf(output,"r\tdamping\n");
         for(N=1;N<=NT;N++)
         {
                           fprintf(output,"%lf\t%e\n",(N-1)*rstep,DPF[N]/DPF[1]);
         }
         fclose(output);
         printf("Process end");
         //getch();
         return 0;
}

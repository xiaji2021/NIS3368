#include <iostream>

using namespace std;

int main()
{
    int a[10][10]= {0},f[10][10]= {0}, R,i,j,sum;

    cin >> R;

    for(i=0; i<R; ++i)
    {
        for(j=0; j<=i; ++j)
        {
            cin >> a[i][j];
        }
    }

    f[0][0]=a[0][0];
    //f[1][0]=a[1][0]+f[0][0];
    //f[1][1]=a[1][1]+f[0][0];
    for(i=1; i<R; ++i)
    {
        for(j=0; j<=i; ++j)
        {
            if(j>=1)
            {
                if(f[i-1][j]>f[i-1][j-1])
                {
                    f[i][j]=a[i][j]+ f[i-1][j];
                }
                else f[i][j]=a[i][j]+f[i-1][j-1];
            }
            else f[i][j]=f[i-1][j]+a[i][j];
        }
    }

    sum=f[R-1][0];
    for(i=1; i<R; ++i)
    {
        if(f[R-1][i]>sum)
            sum=f[R-1][i];
    }

    cout << sum;


    return 0;
}

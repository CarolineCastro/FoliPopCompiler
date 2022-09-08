#include <stdio.h>
int main (void){
float a;
float b;
float s;
float c;
printf("Calcula média aritimética\n");
printf(" \n");
a = 0;
while(a<1){
printf("Entre com a quantidade de valores a serem calculados: \n");
if(0 == scanf("%f", &a)) {
a = 0;
scanf("%*s");
}
}
b = 0;
s = 0;
while(b<a){
printf("Entre com um valor: \n");
if(0 == scanf("%f", &c)) {
c = 0;
scanf("%*s");
}
s = s+c;
b = b+1;
}
printf("A média é: \n");
printf ("%.2f\n", (float)(s/a));
return 0;
}

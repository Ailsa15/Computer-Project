#Calculating percentage difference delta E

Theoretical = [3.086-3.004, 3.708-3.645, 4.147-4.124, 4.534-4.579]
Experimental = [0.1329181133959173, 0.09644712130509946, 0.08566453598601087]
Difference = [exp - theor for exp, theor in zip(Experimental, Theoretical)]
PercentageDifference = [diff / theor * 100 if theor != 0 else 0 for diff, theor in zip(Difference, Theoretical)]
#print(PercentageDifference)

x=3.414-2*1.28
print(x)    

b = 0.229953092713145
b1 = 0.2300191926452611
b2 = 0.20687788000618407
#b3 = 0.25328010802040457
#Delta b = 0.02326714887226866
bE = b1-b
bM = b2-b
DeltaE = (bM**2+bE**2)**0.5
print(b, DeltaE)
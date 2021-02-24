import math
import random
from sympy import isprime

def pointAdd(x1, y1, x2, y2, p):
	s = ((y2-y1)*pow((x2-x1),-1, p)) % p
	x3 = (s**2 - x1 - x2) % p
	y3 = (s*(x1 - x3) - y1) % p
	return (x3, y3)

def pointDouble(x1, y1, a, p):
	s = ((3*x1**2+a)*pow((2*y1), -1, p)) % p
	x3 = (s**2 - x1 - x1) % p
	y3 = (s*(x1 - x3) - y1) % p
	return (x3, y3)

def pointMult(x1, y1, n, a, p):
	x = x1
	y = y1
	d = list(f'{n:b}')
	for i in range(1, len(d)):
		(x, y) = pointDouble(x,y,a,p)
		if d[i] == '1':
			(x, y) = pointAdd(x,y,x1,y1,p)
	return (x, y)

def main():
	a = -3
	b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
	p = pow(2,521)-1
	q = 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449

	P_x = 0xc6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66
	P_y = 0x1839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650
	n = 457351 #ephemeral
	private = 1537540

	(B_x, B_y) = pointMult(P_x,P_y,private,a,p)
	print('B_x =', B_x)
	print('B_y =', B_y)

	(R_x, R_y) = pointMult(P_x,P_y,n,a,p)
	print('R_x =,', R_x)
	print('R_y =,', R_y)

	x = 0x777196555de9a55a506c5c8be936e9438e979ed58814a62eb361b89c316ef61714affcc03cad7912bc7696324e5f958aae2b7b517ec5b1db1441915f9b5be446
	r = R_x
	print('xr mod q is equivalent to', (x*r)%q)

	inv_n = pow(n, -1, q) #ephemeral inverse
	print('inv_n =', inv_n)

	s = ((x+private*r)*inv_n)%q
	print('r =', r)
	print('s =', s)

	w = pow(s, -1, q)
	u1 = (w*x)%q
	u2 = (w*r)%q
	(u1P_x, u1P_y) = pointMult(P_x,P_y,u1,a,p)
	(u2B_x, u2B_y) = pointMult(B_x,B_y,u2,a,p)
	(V_x, V_y) = pointAdd(u1P_x, u1P_y, u2B_x, u2B_y, p)
	v = V_x
	print('w =', w)
	print('u1 =', u1)
	print('u2 =', u2)
	print('V_x =', V_x)
	print('V_y =', V_y)
	print('v == r is', v%q == r%q)

	return

if __name__ == '__main__':
	main()
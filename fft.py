#!/usr/local/bin/python2.3
import math
import sys

pi=math.pi
e=math.e
j=complex(0,1)

def fft(f,inv):
    n=len(f)
    if n==1:
        return f

    for p in 2,3,5:
        if n%p==0:
            break
    else:
        raise Exception('%s not factorable ' % n)

    #print 'n=%d,p=%d' % (n,p)
    #print f,' << fin'
    m = n/p
    Fout=[]
    for q in range(p): # 0,1
        fp = f[q::p]
        #print fp,'<< fp'
        Fp = fft( fp ,inv)
        Fout.extend( Fp )

    for u in range(m):
        scratch = Fout[u::m] # u to end in strides of m
        #print scratch
        for q1 in range(p):
            k = q1*m + u  # indices to Fout above that became scratch
            Fout[ k ] = scratch[0] # cuz e**0==1 in loop below
            for q in range(1,p):
                if inv:
                    t = e ** ( j*2*pi*k*q/n )
                else:                    
                    t = e ** ( -j*2*pi*k*q/n )
                Fout[ k ] += scratch[q] * t

    return Fout

def real_fft( f,inv ):
    if inv:
        sys.stderr.write('not impl\n')
        sys.exit(1)

    N = len(f) / 2

    res = f[::2]
    ims = f[1::2]

    fp = [ complex(r,i) for r,i in zip(res,ims) ]
    Fp = fft( fp ,0 )

    F = []
    for k in range(N):
        F1k = Fp[k] + Fp[-k].conjugate()
        F2k = -j*(Fp[k] - Fp[-k].conjugate())

        F.append( ( F1k + e ** ( -j*pi*k/N ) * F2k ) * .5 )

    F.append( complex( Fp[0].real - Fp[0].imag , 0 ) )
    return F

def test(f=range(1024),ntimes=10):
    import time
    t0 = time.time()
    for i in range(ntimes):
        fft(f,0)
    t1 = time.time()
    print '%ss'% (t1-t0)

def main():
    #fft_func = fft
    fft_func = real_fft

    tvec = [0.309655,0.815653,0.768570,0.591841,0.404767,0.637617,0.007803,0.012665]
    Ftvec = [ complex(r,i) for r,i in zip(
                [3.548571,-0.378761,-0.061950,0.188537,-0.566981,0.188537,-0.061950,-0.378761],
                [0.000000,-1.296198,-0.848764,0.225337,0.000000,-0.225337,0.848764,1.296198] ) ]

    F = fft_func( tvec,0 )

    nerrs= 0
    for i in range(len(Ftvec)/2 + 1):
        if abs( F[i] - Ftvec[i] )> 1e-5:
            print 'F[%d]: %s != %s' % (i,F[i],Ftvec[i])
            nerrs += 1

    print '%d errors in forward fft' % nerrs
    if nerrs:
        return

    trec = fft_func( F , 1 )

    for i in range(len(trec) ):
        trec[i] /= len(trec)

    for i in range(len(tvec) ):
        if abs( trec[i] - tvec[i] )> 1e-5:
            print 't[%d]: %s != %s' % (i,tvec[i],trec[i])
            nerrs += 1

    print '%d errors in reverse fft' % nerrs

    
if __name__ == "__main__":
    main()

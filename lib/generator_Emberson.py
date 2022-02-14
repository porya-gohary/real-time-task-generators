  
#!/usr/bin/python

"""A taskset generator for experiments with real-time task sets
Copyright 2010 Paul Emberson, Roger Stafford, Robert Davis. 
All rights reserved.
Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:
   1. Redistributions of source code must retain the above copyright notice, 
      this list of conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation 
      and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY EXPRESS 
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
EVENT SHALL THE AUTHORS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
The views and conclusions contained in the software and documentation are 
those of the authors and should not be interpreted as representing official 
policies, either expressed or implied, of Paul Emberson, Roger Stafford or 
Robert Davis.
Includes Python implementation of Roger Stafford's randfixedsum implementation
http://www.mathworks.com/matlabcentral/fileexchange/9700
Adapted specifically for the purpose of taskset generation with fixed
total utilisation value
Please contact paule@rapitasystems.com or robdavis@cs.york.ac.uk if you have 
any questions regarding this software.
"""

from lib.task import task
import numpy

def StaffordRandFixedSum(n, u, nsets):

    #deal with n=1 case
    if n == 1:
        return numpy.tile(numpy.array([u]),[nsets,1])
    
    k = numpy.floor(u)
    s = u
    step = 1 if k < (k-n+1) else -1
    s1 = s - numpy.arange( k, (k-n+1)+step, step )
    step = 1 if (k+n) < (k-n+1) else -1
    s2 = numpy.arange( (k+n), (k+1)+step, step ) - s

    tiny = numpy.finfo(float).tiny
    huge = numpy.finfo(float).max

    w = numpy.zeros((n, n+1))
    w[0,1] = huge
    t = numpy.zeros((n-1,n))

    for i in numpy.arange(2, (n+1)):
        tmp1 = w[i-2, numpy.arange(1,(i+1))] * s1[numpy.arange(0,i)]/float(i)
        tmp2 = w[i-2, numpy.arange(0,i)] * s2[numpy.arange((n-i),n)]/float(i)
        w[i-1, numpy.arange(1,(i+1))] = tmp1 + tmp2;
        tmp3 = w[i-1, numpy.arange(1,(i+1))] + tiny;
        tmp4 = numpy.array( (s2[numpy.arange((n-i),n)] > s1[numpy.arange(0,i)]) )
        t[i-2, numpy.arange(0,i)] = (tmp2 / tmp3) * tmp4 + (1 - tmp1/tmp3) * (numpy.logical_not(tmp4))

    m = nsets
    x = numpy.zeros((n,m))
    rt = numpy.random.uniform(size=(n-1,m)) #rand simplex type
    rs = numpy.random.uniform(size=(n-1,m)) #rand position in simplex
    s = numpy.repeat(s, m);
    j = numpy.repeat(int(k+1), m);
    sm = numpy.repeat(0, m);
    pr = numpy.repeat(1, m);

    for i in numpy.arange(n-1,0,-1): #iterate through dimensions
        e = ( rt[(n-i)-1,...] <= t[i-1,j-1] ) #decide which direction to move in this dimension (1 or 0)
        sx = rs[(n-i)-1,...] ** (1/float(i)) #next simplex coord
        sm = sm + (1-sx) * pr * s/float(i+1)
        pr = sx * pr
        x[(n-i)-1,...] = sm + pr * e
        s = s - e
        j = j - e #change transition table column if required

    x[n-1,...] = sm + pr * s
    
    #iterated in fixed dimension order but needs to be randomised
    #permute x row order within each column
    for i in range(0,m):
        x[...,i] = x[numpy.random.permutation(n),i]

    return numpy.transpose(x);

def gen_periods(n, nsets, min, max, gran, dist):

    if dist == "logunif":
        periods = numpy.exp(numpy.random.uniform(low=numpy.log(min), high=numpy.log(max+gran), size=(nsets,n)))
    elif dist == "unif":
        periods = numpy.random.uniform(low=min, high=(max+gran), size=(nsets,n))
    else:
        return None
    periods = numpy.floor(periods / gran) * gran

    return periods

def gen_tasksets(n, u, nsets, permin, permax, gran, dist,round_C):
    """
    n: size of taskset (number of tasks in each taskset)
    u: total taskset utilisation
    nsets: number of tasksets
    permin: minimum period value
    permax: maximum period value
    gran: period granularity
    dist: choose period distribution to be 'unif' or 'logunif'
    round_C: round execution times to nearest integer
    """
    x = StaffordRandFixedSum(n, u, nsets)
    periods = gen_periods(n, nsets, permin, permax, gran, dist)
    #iterate through each row (which represents utils for a taskset)
    tasksets=[]
    for i in range(numpy.size(x, axis=0)):
        C = x[i] * periods[i]
        if round_C:
            C = numpy.round(C, decimals=0)
        
        temp = numpy.c_[x[i], C / periods[i], periods[i], C]
        taskset=[]
        for t in range(numpy.size(temp,0)):
            temp_task=task(wcet=int(temp[t][3]),period=int(temp[t][2]),deadline=int(temp[t][2]))
            taskset.append(temp_task)
        tasksets.append (taskset)
    return tasksets
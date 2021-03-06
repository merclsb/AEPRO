function[Lo,Up]=confinh(x,statfun,alpha,B1,varargin)
%           
%      [Lo,Up]=confinh(x,statfun,alpha,B1,PAR1,...)
%
%      Confidence interval of the estimator of a parameter
%      based on the bootstrap hybrid method  
%
%     Inputs:
%           x - input vector data 
%     statfun - the estimator of the parameter given as a Matlab function   
%      alpha  - level of significance (default alpha=0.05)  
%          B1 - number of bootstrap resamplings (default B1=199) 
%    PAR1,... - other parameters than x to be passed to statfun
%
%     Outputs:
%         Lo - The lower bound 
%         Up - The upper bound
%
%     Example:
%
%     [Lo,Up] = confinth(randn(100,1),'mean');


%  Created by A. M. Zoubir and D. R. Iskander
%  May 1998
%
%  References:
% 
%  Efron, B.and Tibshirani, R.  An Introduction to the Bootstrap.
%               Chapman and Hall, 1993.
%
%  Hall, P. Theoretical Comparison of Bootstrap Confidence
%               Intervals. The Annals of Statistics, Vol  16, 
%               No. 3, pp. 927-953, 1988.
%
%  Zoubir, A.M. Bootstrap: Theory and Applications. Proceedings 
%               of the SPIE 1993 Conference on Advanced  Signal 
%               Processing Algorithms, Architectures and Imple-
%               mentations. pp. 216-235, San Diego, July  1993.
%
%  Zoubir, A.M. and Boashash, B. The Bootstrap and Its Application
%               in Signal Processing. IEEE Signal Processing Magazine, 
%               Vol. 15, No. 1, pp. 55-76, 1998.

pstring=varargin;

if (exist('B1')~=1), B1=199; end;
if (exist('alpha')~=1), alpha=0.05; end;

x=x(:);
vhat=feval(statfun,x,pstring{:});
[vhatstar,ind]=bootstrp(B1,statfun,x,pstring{:});

q1=floor(B1*alpha*0.5);
q2=B1-q1+1;
tvec=vhatstar-vhat;       
st=sort(tvec);
Lo=vhat-st(q2);
Up=vhat-st(q1);


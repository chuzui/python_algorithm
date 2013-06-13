function xx = degexpand(x,deg)
  % Expands input vectors to contain also powers of input features,
  % and also scales down each feature.
  [n,m] = size(x) ;
  xx = reshape(  repmat(x,[1,1,deg]) .^ ...
	             repmat(reshape(1:deg,[1,1,deg]),[n,m]) ...
              ,[n,m*deg]) ;
  % Scale down to numbers in [-1,1]
  xx = xx / diag(max(abs(xx))) ;
  

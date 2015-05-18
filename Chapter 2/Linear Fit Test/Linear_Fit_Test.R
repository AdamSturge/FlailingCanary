#Define linear regression function
Y_hat = function(B,X){
  return (t(X)%*%B)
}

# Load data and solve for model parameters (stored in Beta)
load("ESL.mixture.rda")
X = cbind(rep(1,200),ESL.mixture$x)
y = ESL.mixture$y
det = det(t(X)%*%X)
if(det != 0){
  Beta = solve(t(X)%*%X)%*%t(X)%*%y
}else{
  print("X is signular, could not solve for Beta")
  Beta = c(0,0,0)
}

# Define orange-blue classifier
ob_classify = function(y_hat){
  if(y_hat >= 0.5){
    return ('ORANGE')
  }else{
    return ('BLUE')
  }
}

# Define color coded training dataset
TColors = unlist(lapply(y,ob_classify))
TData   = cbind(ESL.mixture$x,TColors)
colnames(TData , do.NULL = FALSE)
colnames(TData) <- c("x1","x2","color")

# Define color coded latice
Density = 0.25
GridMin = -2
GridMax = 4
GridLine = seq(GridMin,GridMax,Density)
RowCount = length(GridLine)^2 + 1
ColCount = 3
Grid = matrix(nrow=RowCount,ncol=ColCount)
colnames(Grid , do.NULL = FALSE)
colnames(Grid) <- c("x1","x2","color")
rowIndex = 1
for(i in 1:length(GridLine))
{
  x1 = GridLine[i]
  for(j in 1:length(GridLine))
  {
    x2 = GridLine[j]
    input = c(1,x1,x2)
    y_hat = input%*%Beta
    color = ob_classify(y_hat)
    Grid[rowIndex,] = c(x1,x2,color)
    rowIndex = rowIndex + 1
  }
}

#Solve for decision boundry
#j = expression(Beta[1]*1 + Beta[2]*x1 + Beta[3]*x2)
DBoundry = data.frame(t=GridLine)
param_1 = function(t) { return (t) }
param_2 = function(t) { return ((0.5 - Beta[1] - Beta[2]*t)/Beta[3])}
DBoundry$x1=param_1(dat$t)
DBoundry$x2=param_2(dat$t)

# Create plot
plot(Grid[,1],Grid[,2],col=Grid[,3],xlab='X1',ylab='X2',xaxt='n',yaxt='n',ylim=c(GridMin, GridMax),pch = 20,cex=0.75,lwd=1)
par(new=TRUE)
plot(TData[,1],TData[,2],col=TData[,3],xlab='',ylab='',xaxt='n',yaxt='n',ylim=c(GridMin, GridMax),pch = 1,cex=1.5,lwd=2)
par(new=TRUE)
plot(DBoundry$x1,DBoundry$x2,type="l",xlab='',ylab='',xaxt='n',yaxt='n',ylim=c(GridMin, GridMax))
par(new=FALSE)




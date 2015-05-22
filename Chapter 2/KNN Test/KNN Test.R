# Define KNN values
k <- 15
metric <- function(x,y){
  diff <- as.matrix(x - y)
  return (norm(diff))
}
KNNAvg <- function(x,k){
  s = sum(x)
  return (s/k);
}

# Load data 
load("ESL.mixture.rda")
x <- ESL.mixture$x
colnames(x , do.NULL <- FALSE)
colnames(x) <- c("x1","x2")
y <- ESL.mixture$y


# Define orange-blue classifier
obClassify <- function(yHat){
  if(yHat >= 0.5){
    return ('ORANGE')
  }else{
    return ('BLUE')
  }
}

# Define color coded training dataset
tColors = unlist(lapply(y,obClassify))
tData   = cbind(ESL.mixture$x,tColors)
colnames(TData , do.NULL = FALSE)
colnames(TData) <- c("x1","x2","color")

# Define Grid
density <- 0.20
gridMin <- -3
gridMax <- 7
gridLine <- seq(gridMin,gridMax,density)
rowCount <- length(gridLine)^2
colCount <- 3
grid <- matrix(nrow=rowCount,ncol=colCount)
colnames(grid , do.NULL=FALSE)
colnames(grid) <- c("x1","x2","color")
rowIndex <- 1
for(i in 1:length(gridLine))
{
  x1 <- gridLine[i]
  for(j in 1:length(gridLine))
  {
    x2 <- gridLine[j]   
    grid[rowIndex,] <- c(x1,x2,"Black")
    rowIndex <- rowIndex + 1
  }
}
    
# Compute KNN value for each point in grid
for(i in 1:nrow(grid)){
  # compute distances
  classificationPoint <- as.numeric(cbind(grid[[i,1]],grid[[i,2]]))
  distances <- cbind(rep(0,nrow(x)),rep(0,nrow(x)))
  colnames(distances , do.NULL=FALSE)
  colnames(distances) <- c("distance","y_val")
  for(j in 1:nrow(x)){
    trainingPoint <- x[j,]
    distances[j,1] <- metric(classificationPoint,trainingPoint)
    distances[j,2] <- y[j]
  }
  
  #order by distance
  distances <- distances[order(distances[,1]),]
  
  # select top k contributors
  distances <- head(distances,k)
  
  #compute average and classify
  yHat <- KNNAvg(distances[,2],k)
  grid[i,3] <- obClassify(yHat)
  
}

# Create plot
plot(grid[,1],grid[,2],col=grid[,3],xlab='X1',ylab='X2',xaxt='n',yaxt='n',xlim=c(gridMin, gridMax),ylim=c(gridMin, gridMax),pch = 20,cex=0.75,lwd=1)
par(new=TRUE)
plot(tData[,1],tData[,2],col=tData[,3],xlab='',ylab='',xaxt='n',yaxt='n',xlim=c(gridMin, gridMax),ylim=c(gridMin, gridMax),pch = 1,cex=1.5,lwd=2)
par(new=FALSE)
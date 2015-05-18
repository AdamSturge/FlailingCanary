#  The purpose here is to build something in R from scratch, without relying 
#  too much on pre-built ML functions.

Dist <- function(x,y){  # Function to compute Euclidean distance of numeric vectors.
  return(sqrt(sum((x-y)^2)))
}

#We need a function to find the N nearest neighbours to a point.
#We can probably do better than calculating the distance of all points and then sorting the whole list.
#I will look into how R's implementation works.
NearNeighbourSearch <- function(point, training.data, n){  # Function to find n nearest neighbours
  temptd <- cbind(training.data, temp.distances <- apply(training.data[, 1:2],
                                                         1, Dist, point))  # Calculate distance of all 
                                                                       # data to the point in question.
  
  
  
  return(head(temptd[order(temp.distances), ],n))
}


#The linear model is just a quick matrix computation.
LinModel <- function(training.data, observed){
  params <- solve(t(training.data)%*%training.data)%*%t(training.data)%*%observed
  return(params)
}


#Next we load our libraries and data.
library("ggplot2")
load("ESL.mixture.rda")

# Load the training data, observed values, and test data.
training.data.set <- ESL.mixture$x

training.data.observed <- ESL.mixture$y #And the observed values

test.data <- ESL.mixture$xnew

#Augment the data for the linear model. 
training.data.set.aug <- cbind(training.data.set,rep(1,times=200))



#I should probably write a function to compute this, so that I can change the number of neighbours more easily.
nn.predictions <- apply(test.data, 1, function (x) sum(NearNeighbourSearch(x,cbind(training.data.set,training.data.observed),7)[,3])/7)


linmod.predictions <- cbind(test.data,1)%*%LinModel(training.data.set.aug,training.data.observed)


nn.predictions.bin <- cbind(test.data,ifelse(nn.predictions >0.5,1,0))
linmod.predictions.bin <- cbind(test.data,ifelse(linmod.predictions >0.5,1,0))
test.data.plot <- qplot(test.data[,1],test.data[,2])

nn.plot <- (test.data.plot + geom_point(aes(colour = factor(nn.predictions.bin[, 3]))))

linmod.plot <- (test.data.plot + geom_point(aes(colour = factor(linmod.predictions.bin[, 3]))))

# some inputation functions to replace missing values cases.
random.impute <- function(a) {
	missing <- is.na(a)
	n.missing <- sum(missing)
	obs <- a[!missing]
	imputed <- a
	imputed[missing] <- sample(obs, n.missing, replace = TRUE)
	return(imputed)
}

randomTime.imputed <- function(a) {
	missing <- is.na(a) | (a== "0000-00-00 00:00:00") | (a==0)
	n.missing <- sum(missing)
	obs <- a[!missing]
	imputed <- a
	imputed[missing] <-  "2013-01-01 00:00:00"
	return(imputed)
}

mean.imputed <- function(a) {
	missing <- (a==0) | (a > 100)
	n.missing <- sum(missing)
	obs <- a[!missing]
	imputed <- a
	imputed[missing] <- rnorm(n.missing, mean = mean(a[a<100 & a>0], na.rm = TRUE), sd=sd(a, na.rm = TRUE)/10)
	return(imputed)

}

timediff <- function(x) {
 jan1 <- strptime( "2013-01-01", "%Y-%m-%d ")
 difftime(jan1, x, unit="week")
 }


# function to split the data set into training and test sets
 splitdf <- function(df, percent =70, seed = 1) {
	set.seed(seed)
	index <- 1:nrow(df)
	trainindex <- sample(index, round(nrow(df)*percent/100))
	train <- df[trainindex,]
	test <- df[-trainindex,]
	totalset <- list(train,  test)
	return(totalset)
} 


# compute the cosine similarity: A.B/|A|*|B|
cosineSimilarity <- function(vecA, vecB) {
	if (length(vecA) != length(vecB)){
		return(0)
	}
	sim <- ( vecA %*% vecB)/(sqrt(vecA %*%vecA) * sqrt(vecB %*% vecB))
	return(sim)
}


# compute the jaccard similarity: intersect(A,B)/union(A,B)

jaccardSimilarity <- function(vecA, vecB) {
	if (length(vecA) != length(vecB)){
		return(0)
	}
	intersect <- vecA %*% vecB
	union = length(vecA)
	sim <- intersect/union
	return(sim)
}


rmse <- function(y, x) {
	if (length(y) != length(x)) {
		stop('Output and input are not of the same length')
	}

	err = 0
	for (i in 1:length(y)) {
		err = err + (y[i] - x[i]) * (y[i] - x[i])
	}
	return (sqrt(err))
}


library(gdata)


#########################################################################################################
#########################################################################################################


course_details <- read.csv('data/course_details.csv', sep='\t', header= TRUE)
salary_details <- read.xls('data/Salary-19thFeb.xlsx', header= TRUE)
course_details <- course_details[,c("course_id", "fees_value", "fees_unit")]

course_location <- read.csv('data/course_location.csv', sep ='\t', header = TRUE)

course_details.fin <- merge(course_details, course_location, by.x = "course_id", by.y = "course_id")

insticoursemap <- read.xls('data/InstituteToCourse.xlsx', header= TRUE)
courselist <- unique(insticoursemap$course_id)

course_details.final <- merge(course_details.fin, insticoursemap, by.x = "course_id", by.y = "course_id")

examcourse <- read.csv("data/listingExamMap.csv", sep='\t', colClasses='character')
examcourse <- examcourse[!duplicated(examcourse),]

salary_details <- salary_details[which(salary_details$exp_bucket == '0-2'),]
salary_details <-  salary_details[, c("shikshainst", "ctc50")]

course_details.final$CAT <- 0

for (course in unique(examcourse$typeId)) {
	if (nrow(examcourse[which(examcourse$typeId == course & examcourse$marks > 0 & examcourse$examId == 305),]) > 0 & (nrow(course_details.final[which(course_details.final$course_id == course), ]) > 0 )) {
		course_details.final[which(course_details.final$course_id == course), ]$CAT <- examcourse[which(examcourse$typeId == course & examcourse$examId == 305 & examcourse$marks > 0),]$marks
	}
}

course_details.final$CAT  <- as.numeric(course_details.final$CAT)
course_details.final$MAT <- 0

for (course in unique(examcourse$typeId)) {
	if (nrow(examcourse[which(examcourse$typeId == course & examcourse$marks > 0 & examcourse$examId == 306),]) > 0 & (nrow(course_details.final[which(course_details.final$course_id == course), ]) > 0 )) {
		course_details.final[which(course_details.final$course_id == course), ]$MAT <- examcourse[which(examcourse$typeId == course & examcourse$examId == 306 & examcourse$marks > 0),]$marks
	}
}

course_details.final$MAT  <- as.numeric(course_details.final$MAT)
course_details.final$CMAT <- 0

for (course in unique(examcourse$typeId)) {
	if (nrow(examcourse[which(examcourse$typeId == course & examcourse$marks > 0 & examcourse$examId == 309),]) > 0 & (nrow(course_details.final[which(course_details.final$course_id == course), ]) > 0 )) {
		course_details.final[which(course_details.final$course_id == course), ]$CMAT <- examcourse[which(examcourse$typeId == course & examcourse$examId == 309 & examcourse$marks > 0),]$marks
	}
}

course_details.final$CMAT  <- as.numeric(course_details.final$CMAT) 
course_details.final <- merge(course_details.final, salary_details, by.x='institute_id', by.y = 'shikshainst', all = FALSE, all.x = TRUE)

course_details.final <- course_details.final[!duplicated(course_details.final),]


simScoreList.all <- data.frame()

for (course1 in unique(course_details.final$course_id)) {
	course1.feat <- course_details.final[which(course_details.final$course_id == course1),]
	simScoreList <- data.frame('institute' = character() ,'course' = character(), 'feescore' =  numeric(), 'cutoffscore' = numeric(), 'locscore' = numeric(), 'salscore' = numeric(), 'medScore' = numeric())
	for (course2 in unique(course_details.final$course_id)){
		course2.feat <- course_details.final[which(course_details.final$course_id == course2),]
		if(course1.feat$fees_unit != course2.feat$fees_unit) {
			simScore.fees <- 0
		} 
		else {
			diff <- abs(course1.feat$fees_value - course2.feat$fees_value)
			simScore.fees <- median(course_details.final$fees_value, na.rm = TRUE) / (median(course_details.final$fees_value, na.rm = TRUE) + diff)
		}

		if(course1.feat$CAT == 0 | course2.feat$CAT == 0){
			simScore.cutoff <- 0
		}
		else {
			simScore.cutoff <- 1 /(1 + abs(course1.feat$CAT - course2.feat$CAT)/course1.feat$CAT)
		}

		simScore.loc = 0
		if(course1.feat$state_id == course2.feat$state_id) {
			simScore.loc  = 0.5
		}

		if(course1.feat$city_id == course2.feat$city_id) {
			simScore.loc  = 1
		}

		if(is.na(course1.feat$ctc50) | is.na(course2.feat$ctc50)){
			simScore.ctc50 <- 0
		} else {
			diff <- abs(course1.feat$ctc50 - course2.feat$ctc50)
			simScore.ctc50 <- median(course_details.final$ctc50, na.rm = TRUE) / (median(course_details.final$ctc50, na.rm = TRUE) + diff)
		}

		medianScore <- median(c(simScore.loc, simScore.ctc50, simScore.cutoff, simScore.fees), na.rm = TRUE)
		simScoreList <- rbind(simScoreList , data.frame('course1' = course1, 'institute' = course2.feat$institute_id ,'course2' = course2, 'feescore' =  simScore.fees, 'cutoffscore' = simScore.cutoff, 'locscore' = simScore.loc, 'salscore' = simScore.ctc50, 'medScore' = medianScore))

		# simScore <- rbind(simScore, data.frame('course1' <- course1, 'course2' <- course2, 'score' <- simScore.fees))
	} 
		simScoreList.order <- simScoreList[order(simScoreList$institute, -simScoreList$medScore), c("course1","course2", "institute", "medScore")]
		simScoreList.trim <- simScoreList.order[!duplicated(simScoreList[c("institute")]), ] 
		simScoreList.trim <- simScoreList.trim[order(-simScoreList.trim$medScore), ]
		simScoreList.trim <- simScoreList.trim[1:7,]
		simScoreList.all <- rbind(simScoreList.all, simScoreList.trim)
}
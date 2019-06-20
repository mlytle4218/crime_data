print('starting')
library(RANN)
setwd('/home/marc/Desktop/crime_data/')
# Read in the Crime data.
df_crime <- read.csv("Crime_Data_from_2010_to_Present.csv")

# Get rid of huge spaces in address and cross street
df_crime$Address <- gsub("[ \t]{1,}", ' ', as.character(df_crime$Address))
df_crime$Cross.Street <- gsub("[ \t]{1,}", ' ', as.character(df_crime$Cross.Street))



# From the inside out - get the Location column as character - strip
# the parenthesis from the GPS data - split the data on the comma - 
# turn the result into a matrix with rbind 
loc_temp <- do.call(
  rbind, strsplit(
    gsub("\\(|\\)", '', as.character(df_crime$Location)), 
    ',')
  )

# Create Lat and Lon columns as floats instead of characters
df_crime$Lat <- as.numeric(loc_temp[,1])
df_crime$Lon <- as.numeric(loc_temp[,2])
rm(loc_temp)

# Drop Location column as it's data is now Lat and Lon
df_crime$Location <- NULL

#Drop any rows that have Lat and Lon equal to 0
df_crime <- subset(df_crime, Lat!=0)
df_crime <- subset(df_crime, Lon!=0)


# Turning string date into Date
df_crime$Date.Occurred <- as.Date(df_crime$Date.Occurred, format = "%m/%d/%Y")
df_crime$Date.Reported <- as.Date(df_crime$Date.Reported, format = "%m/%d/%Y")




# Load in air data
print('loading pm10')
df_pm10_1 <- read.csv("pm10_1.csv")
df_pm10_2 <- read.csv("pm10_2.csv")
df_pm10_3 <- read.csv("pm10_3.csv")

# combine them together
df_pm10 <- rbind(df_pm10_1,df_pm10_2,df_pm10_3)

# change date from factor to Date - changing it to Date.Occurred to make merging easier
df_pm10$Date.Local <- as.Date(df_pm10$Date.Local, format = "%Y-%m-%d")

# drop the Date.Local now
#df_pm10$Date.Local <-  NULL

# get rid of the old data frames
rm(df_pm10_1,df_pm10_2,df_pm10_3)

# Get rid of rows with missing important data
df_pm10 <- subset(df_pm10, !is.na(df_pm10$Sample.Measurement))
df_pm10 <- subset(df_pm10, !is.na(df_pm10$Latitude))
df_pm10 <- subset(df_pm10, !is.na(df_pm10$Longitude))


# Latitude is a Factor instead of a numeric - making them similar
df_pm10$Latitude <- as.numeric( levels( df_pm10$Latitude  ) )[df_pm10$Latitude]


# Create data frames for nearest neighbor search
df_crime_coords <- data.frame(df_crime$Lat,df_crime$Lon)
df_pm10_coords <- data.frame(df_pm10$Latitude,df_pm10$Longitude)

# run nearest neighbor search 
# was counter intuitive to me - first the data you are trying 
# match to and then the data you are trying to match with then
# the number of matches you want
nn <- nn2(df_pm10_coords, df_crime_coords, k=1)

# the result as the index to the get the site.num and then pass
# it into the crime dataframe
df_crime$site.num <- df_pm10$Site.Num[nn[[1]] ]
rm(df_crime_coords)
rm(df_pm10_coords)
rm(nn)

# breaking up the crime data into regions based on samle locations
df_crime_correlated_site_numbers <- unique((df_crime$site.num))
for (val in df_crime_correlated_site_numbers){
  assign(paste('df_crime',val,sep="_"),  subset(df_crime, site.num==val))
}

# quick graph
library(plyr)

df_6012 <- count(`df_crime_6012`, vars='Date.Occurred')
head(df_6012, 20)
plot(df_6012, xaxt = "n", type = "l")
axis(1, df_6012$Date.Occurred, format(df_6012$Date.Occurred, "%b %d"), cex.axis = .7)

# breaking up the air quality data into regions as well
df_pm10_site_numbers <- unique(df_pm10$Site.Num)
for (val in df_pm10_site_numbers){
  assign(paste('df_pm10',val,sep="_"), subset(df_pm10, Site.Num == val))
}

# get a day by day count of crimes for are 4002
df_crime_4002_count <- count(df_crime_4002, vars='Date.Occurred')


# group and find the mean and max of samples on each day
df_pm10_4002_mean <- setNames(aggregate(df_pm10_4002$Sample.Measurement, by=list(df_pm10_4002$Date.Local), mean), c('Date.Local','Mean'))
df_pm10_4002_max <- setNames(aggregate(df_pm10_4002$Sample.Measurement, by=list(df_pm10_4002$Date.Local), max), c('Date.Local','Max'))


#merge the crime data counts and the mean of sample measurements on the dame days
df_4002_mean <- merge(x=df_crime_4002_count, y=df_pm10_4002_mean, by.x=c("Date.Occurred"), by.y=c("Date.Local"))

#merge the crime data counts and the max of sample measurements on the dame days
df_4002_max <- merge(x=df_crime_4002_count, y=df_pm10_4002_max, by.x=c("Date.Occurred"), by.y=c("Date.Local"))

# test the correlations of the frequncy of crime and mean and max sample rates
correlation_mean <- cor.test(df_4002_mean$freq, df_4002_mean$Mean, method='kendall')

correlation_max <-  cor.test(df_4002_max$freq, df_4002_max$Max, method='kendall')


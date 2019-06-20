library(RANN)
setwd('/home/marc/Desktop/crime_data/')
# Read in the Crime data.
df <- read.csv("Crime_Data_from_2010_to_Present.csv")

# Get rid of huge spaces in address and cross street
df$Address <- gsub("[ \t]{1,}", ' ', as.character(df$Address))
df$Cross.Street <- gsub("[ \t]{1,}", ' ', as.character(df$Cross.Street))



# From the inside out - get the Location column as character - strip
# the parenthesis from the GPS data - split the data on the comma - 
# turn the result into a matrix with rbind 
loc_temp <- do.call(
  rbind, strsplit(
    gsub("\\(|\\)", '', as.character(df$Location)), 
    ',')
  )

# Create Lat and Lon columns as floats instead of characters
df$Lat <- as.numeric(loc_temp[,1])
df$Lon <- as.numeric(loc_temp[,2])
rm(loc_temp)

# Drop Location column as it's data is now Lat and Lon
df$Location <- NULL

#Drop any rows that have Lat and Lon equal to 0
df <- subset(df, Lat!=0)
df <- subset(df, Lon!=0)


# really was a waste of time ----------------------------------------------
# # Add leading zeros to military time and regexing for insertion
# # of colon plus adding the ":00" for seconds
# temp <- paste(
#   trimws(
#     gsub('(?=(?:.{2})$)', ":", sprintf("%04.0f", df$Time.Occurred), perl=TRUE),
#     "r"),
#   ":00",sep='')
# 
# # Concat Date,Occurred and formatted time
# temp <- paste(df$Date.Occurred, temp)
# 
# # Add back into dataframe as datetime
# df$datetime <- strptime(temp, "%m/%d/%Y %H:%M:%S", tz="America/Los_Angeles")
# rm(temp)
# 
# # Drop Time.Occurred and Date.Occurred as the info is in datetime
# df$Time.Occurred <- NULL
# df$Date.Occurred <- NULL



# instead doing this ------------------------------------------------------
df$Date.Occurred <- as.Date(df$Date.Occurred, format = "%m/%d/%Y")
df$Date.Reported <- as.Date(df$Date.Reported, format = "%m/%d/%Y")


# Read in zip code info
df_zips <- read.csv("free-zipcode-database-Primary.csv")

# Limit to only in CA
df_zips <- subset(df_zips, State=='CA')

# Create data frames for nearest neighbor search
df_coords <- data.frame(df$Lat,df$Lon)
df_zips_coords <- data.frame(df_zips$Lat,df_zips$Long)

# run nearest neighbor search 
# was counter intuitive to me - first the data you are trying 
# match to and then the data you are trying to match with then
# the number of matches you want
nn <- nn2(df_zips_coords, df_coords, k=1)

# the result as the index to the get the zip codes and then pass
# them into the crime dataframe
df$zipcode <- df_zips$Zipcode[nn[[1]] ]
rm(df_coords)
rm(nn)


# url <- 'https://aqs.epa.gov/api/api/rawData?user=mlytle4218%40gmail.com&pw=greycrane41&format=DMCSV&pc=AQI+POLLUTANTS&param=81102&bdate=20180101&edate=20190417&state=06&county=037&=Submit'
# download.file(url, 'check.csv', 'auto')


# Load in air data
df_pm10_1 <- read.csv("pm10_1.csv")
df_pm10_2 <- read.csv("pm10_2.csv")
df_pm10_3 <- read.csv("pm10_3.csv")

# combine them together
df_pm10 <- rbind(df_pm10_1,df_pm10_2,df_pm10_3)

# get rid of the old data frames
rm(df_pm10_1,df_pm10_2,df_pm10_3)

# Get rid of rows with missing important data
df_pm10 <- subset(df_pm10, !is.na(df_pm10$Sample.Measurement))
df_pm10 <- subset(df_pm10, !is.na(df_pm10$Latitude))
df_pm10 <- subset(df_pm10, !is.na(df_pm10$Longitude))


# Create data frames for nearest neighbor search
# df_pm10_coords <- data.frame(df_pm10$Latitude,df_pm10$Longitude)

# run nearest neighbor search 
# was counter intuitive to me - first the data you are trying 
# match to and then the data you are trying to match with then
# the number of matches you want
# nn <- nn2(df_zips_coords, df_pm10_coords, k=1)

# the result as the index to the get the zip codes and then pass
# them into the crime dataframe
# df_pm10$zipcode <- df_zips$Zipcode[nn[[1]] ]
# head(df_pm10)
# unique(df_pm10$zipcode)
# nn[[1]]



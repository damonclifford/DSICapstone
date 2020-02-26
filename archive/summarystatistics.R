library(tidyverse)
library(zipcode)
library(rworldmap)

#-- bring in data library
setwd("/Repositories/DSICapstone")
data <- read_csv("data.csv")

#-- Data diving
summary(data)


#-- Revenue
rev0 <- data %>% filter(is.na(TotalRev))
rev <- data %>% filter (!is.na(TotalRev))

ggplot(rev, aes(TotalRev)) +
  geom_histogram()

#-- Zip Code
zip <- data %>% filter(!is.na(ZipCode))

data(zipcode)
zipData <- merge(zip, zipcode, by.x="ZipCode", by.y="zip")
newmap <- getMap(resolution = "low")
plot(newmap, xlim = c(-123, -73), ylim = c(26, 47), asp = 1)
points(zipData$longitude, zipData$latitude, col = "red", cex = .6)  

#-- Number of Employees
emp <- data %>% filter (!is.na(NumEmployees))

ggplot(emp, aes(NumEmployees)) +
  geom_histogram(binwidth = 100)

#-- Call Cycle
call <- data %>% group_by(CallCycle) %>% summarise(total = n())

ggplot(call, aes(CallCycle, total)) +
  geom_bar(stat = "identity")

#-- Contract Type
contract <- data %>% group_by(ContractType) %>% summarise(total = n())

ggplot(contract, aes(ContractType, total)) +
  geom_bar(stat = "identity") + 
  theme(text = element_text(size = 10), 
        axis.text.x = element_text(angle = 90, hjust = 1))

#-- Original Source Type
Orig <- data %>% group_by(OriginalSourceType) %>% summarise(total = n())

ggplot(Orig, aes(OriginalSourceType, total)) +
  geom_bar(stat = "identity") + 
  theme(text = element_text(size = 10), 
        axis.text.x = element_text(angle = 90, hjust = 1))

#-- First Conversion
firstconv <- data %>% group_by(FirstConversion) %>% summarise(total = n()) %>% filter(total > 5)

#-- Industry
ggplot(data %>% group_by(Industry) %>% summarise(total = n()) %>% filter(total > 1), 
       aes(Industry, total)) +
  geom_bar(stat = "identity") + 
  theme(text = element_text(size = 10), 
        axis.text.x = element_text(angle = 90, hjust = 1))

#--MRR
ggplot(data, aes(MRR)) +
  geom_histogram()

#-- Gauge
ggplot(data %>% group_by(Gauge) %>% summarise(total = n()), 
       aes(Gauge, total)) +
  geom_bar(stat = "identity") + 
  theme(text = element_text(size = 10), 
        axis.text.x = element_text(angle = 90, hjust = 1))

#-- Strategic
ggplot(data %>% group_by(Strategic) %>% summarise(total = n()), 
       aes(Strategic, total)) +
  geom_bar(stat = "identity") + 
  theme(text = element_text(size = 10), 
        axis.text.x = element_text(angle = 90, hjust = 1))

#-- Strategic vs. Revenue
test <- data %>% filter(!is.na(TotalRev), !is.na(MRR))

ggplot(test, aes(x = TotalRev, y = MRR, color = Strategic)) +
  geom_point() +
  scale_x_log10() + 
  scale_y_log10()

ggplot(test, aes(x = TotalRev, y = MRR, color = Gauge)) +
  geom_point() +
  scale_x_log10() + 
  scale_y_log10() + 
  scale_color_manual(breaks = c("Green", "Green - Flat", "Green - Increase", "Red","Yellow"),
                     values = c("green", "green","green","red","yellow"))
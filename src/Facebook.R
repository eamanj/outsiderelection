# Clear all
rm(list = ls())
graphics.off()

setwd('~/Documents/Conferences/2016/NorthWestern_June_2016/Datathon/Code/')

# install.packages("Rfacebook")
# install.packages("latticeExtra")

library(Rfacebook)
library(latticeExtra)
library(ggplot2)

# Access token
# https://developers.facebook.com/tools/explorer

fb_oauth = 'EAACEdEose0cBAI0LMLICG7KklZCCZAohOuaHn5hBERA5NtMUlhMjdShnazlRHwveqOuqdohyJP5P6tEG5AkqYAsLeKYbvSuUIfIuKQS1nQAbeGP30MMx7ItJFvnjhFtBIIZBGE3JWfm8E8sZBKULLAvPzifZAJ7bcXV0nLXmUngZDZD'

getUsers("me", token=fb_oauth, private_info=TRUE)

# Download page

dates = c('2016/02/09', '2016/02/27', '2016/03/05', '2016/03/13', '2016/04/05', '2016/04/19', '2016/05/03',
          '2016/05/24', '2016/06/05', '2016/06/14')

total_Hillary =  getPage("hillaryclinton", token=fb_oauth, n = 10, feed= FALSE) 
total_Bernie =  getPage("berniesanders", token=fb_oauth, n = 10, feed= FALSE)
total_Trump =  getPage("DonaldTrump", token=fb_oauth, n = 10, feed= FALSE)


# Extract posts 3 days before the primary 
for (n in c(1 : length(dates)))
{
  page <- getPage("hillaryclinton", token=fb_oauth, n=10,
                  since = as.Date(dates[[n]])-3, until=dates[[n]])
  total_Hillary <- rbind(total_Hillary, page)
  page <- getPage("berniesanders", token=fb_oauth, n=10,
                  since = as.Date(dates[[n]])-3, until=dates[[n]])
  total_Bernie <- rbind(total_Bernie, page)
  page <- getPage("DonaldTrump", token=fb_oauth, n=10,
                  since = as.Date(dates[[n]])-3, until=dates[[n]])
  total_Trump <- rbind(total_Trump, page)
}

total_Hillary[which.max(page$likes_count),]
total_Bernie[which.max(page$likes_count),]
total_Trump[which.max(page$likes_count),]

# total_Hillary$message

write.table("Hillary", "Facebook_message.txt", sep="\t", row.names = FALSE, col.name = FALSE, append=TRUE)
write.table(total_Hillary$message, "Facebook_message.txt", sep="\t", row.names = FALSE, col.name = FALSE, append=TRUE)
write.table("Bernie", "Facebook_message.txt", sep="\t", row.names = FALSE, col.name = FALSE, append=TRUE)
write.table(total_Bernie$message, "Facebook_message.txt", sep="\t", row.names = FALSE, col.name = FALSE, append=TRUE)
write.table("Trump", "Facebook_message.txt", sep="\t", row.names = FALSE, col.name = FALSE, append=TRUE)
write.table(total_Trump$message, "Facebook_message.txt", sep="\t", row.names = FALSE, col.name = FALSE, append=TRUE)

# page[which.max(page$comments_count),]
# page[which.max(page$shares_count),]


T_like <- sum(total_Trump$likes_count)
H_like <- sum(total_Hillary$likes_count)
B_like <- sum(total_Bernie$likes_count)

T_share <- sum(total_Trump$shares_count)
H_share <- sum(total_Hillary$shares_count)
B_share <- sum(total_Bernie$shares_count)

T_comments <- sum(total_Trump$comments_count)
H_comments <- sum(total_Hillary$comments_count)
B_comments <- sum(total_Bernie$comments_count)

# counts total posts

T_counts = dim(total_Trump)[[1]]
H_counts = dim(total_Hillary)[[1]]
B_counts = dim(total_Bernie)[[1]]

# Plot 3D bar chart

col1 = c('Hillary', 'Hillary', 'Hillary', 'Bernie', 'Bernie', 'Bernie',
'Trump', 'Trump', 'Trump')
col2 = c('Likes', 'Shares', 'Comments', 'Likes', 'Shares', 'Comments', 'Likes', 
         'Shares', 'Comments')

# Normalized likes, shares, comments by number of posts
col3 = c(sum(total_Hillary$likes_count)/H_counts,  sum(total_Hillary$shares_count)/H_counts, 
         sum(total_Hillary$comments_count)/H_counts, sum(total_Bernie$likes_count)/B_counts, 
         sum(total_Bernie$shares_count)/B_counts, sum(total_Bernie$comments_count)/B_counts,
         sum(total_Trump$likes_count)/T_counts, sum(total_Trump$shares_count)/T_counts,
         sum(total_Trump$comments_count)/T_counts)

d = data.frame(col1, col2,col3)
names(d) = c("Candidate", "Types", "Counts")

ggplot(d, aes(factor(Candidate), Counts, fill = Types)) + 
  geom_bar(stat="identity", position = "dodge") + 
  scale_fill_brewer(palette = "Set1") + xlab("Candidates") +
  ylab("Normalized Counts") + ggtitle("Facebook posts")

# Save to png file
png('facebook.png')
ggplot(d, aes(factor(Candidate), Counts, fill = Types)) + 
  geom_bar(stat="identity", position = "dodge") + 
  scale_fill_brewer(palette = "Set1") + xlab("Candidates") +
  ylab("Normalized Counts") + ggtitle("Facebook posts")
dev.off()



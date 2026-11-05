
args <- commandArgs(trailingOnly = TRUE)
data_dir <- ifelse(length(args) > 0, args[1], ".")

drivers <- read.csv(file.path(data_dir, "drivers.csv"))
d_standings <- read.csv(file.path(data_dir, "driver_standings.csv"))

# Aggregate career wins & points per driver
agg_wins <- aggregate(wins ~ driverId, data = d_standings, FUN = max)
agg_pts  <- aggregate(points ~ driverId, data = d_standings, FUN = sum)

merged <- merge(drivers, agg_wins, by = "driverId")
merged <- merge(merged, agg_pts, by = "driverId")

# Compute Statistical Z-Score of Dominance in R
merged$dominance_z <- round((merged$wins - mean(merged$wins)) / sd(merged$wins), 2)
merged <- merged[order(-merged$dominance_z), ]

write.csv(head(merged[, c("driverRef", "forename", "surname", "nationality", "wins", "dominance_z")], 15),
          file.path(data_dir, "r_f1_dominance_out.csv"), row.names = FALSE)

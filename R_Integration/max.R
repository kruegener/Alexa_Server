myargs <- commandArgs(trailingOnly = T)

nums = as.numeric(myargs)

cat(max(nums))

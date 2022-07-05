install.packages("imager")

require("imager")
botsalt <- load.image("/usr/src/app/output/botsalt.png")
bottemp <- load.image("/usr/src/app/output/bottemp.png")
chl <- load.image("/usr/src/app/output/chl.png")
fchl <- load.image("/usr/src/app/output/fchl.png")
foxy <- load.image("/usr/src/app/output/foxy.png")
fres <- load.image("/usr/src/app/output/fres.png")
fsal <- load.image("/usr/src/app/output/fsal.png")

par(mfrow=c(2,2))
plot(botsalt, axes=FALSE, frame.plot=TRUE)
plot(bottemp, axes=FALSE, frame.plot=TRUE)
plot(chl, axes=FALSE, frame.plot=TRUE)
plot(fchl, axes=FALSE, frame.plot=TRUE)


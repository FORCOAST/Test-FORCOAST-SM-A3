# "(C) Copyright FORCOAST H2020 project under Grant No. 870465. All rights reserved."

#Aarhus University January 2022, Ecoscience, Janus Larsen & Marie Maar. janus@ecos.au.dk
#extract data from gridded FlexSem model output (NetCdf 4.0) and calculate statistcs
#calculate site selection indicies
#make color coded area plots

########## Script settings ##########

require(ncdf4)
require(cmocean)
require(maptools)
require(fields)
require(raster)

#Janus
#setwd("C:\\AU\\projects\\FORCOAST\\siteSelectionTool")
#datFldr = "C:\\data\\FORCOAST\\"
#Marie 
setwd(".")
datFldr = "/usr/src/app/"
args <- commandArgs(trailingOnly = TRUE)

paramLst = list(botsalt=c("botS","3D",F),bottemp=c("botT","3D",F),chl=c("botchl","3D",F),oxy=c("botoxy","3D",F),resup=c("resup_dd","2D",F),fsal=c("botS","3D",T),ftem=c("botT","3D",T),fchl=c("botchl","3D",T),foxy=c("botoxy","3D",T),fres=c("resup_dd","2D",T),ssi=c("ssi","4D",T))
lm <- c(8.18, 9.5, 56.45, 57.05) # area size
pal=cmocean("haline")
#Define figure titles
names <- list(botsalt=c("Bottom salinity (psu)", "psu\n"), bottemp=c("Bottom water temperature (\U000000B0C)", "\U000000B0C\n"), chl=c("Chrolophyll concentration (mg/m\U00B3)", "    mg/m\U00B3\n"), oxy=c("Oxygen concentration (mmol/m\U00B3)","   mmol/m\u00b3\n"), resup=c("resuspension",""), fsal=c("f salinity",""), ftem=c("f temperature",""), fchl=c("f chlorophyll",""), foxy=c("f oxy",""), fres= c("f resuspension",""), ssi=c("Site suitability index","  Index\n\t1 = Most suitable\n\t0 = Least suitable\n"))


########## User settings ##########

defSet = list(
	param = Sys.getenv("param", "ssi"),
	yrs = as.numeric(args[1]:as.numeric(args[2])),
	mths = as.numeric(args[3]:as.numeric(args[4])),
	# salinity threshold (range: 8 to 36)
	SLT = as.numeric(args[5]), # salinity lower threshold
	SUT = as.numeric(args[6]), # salinity upper threshold
	# temperature threshold (range: 0 to 35)
	TLT = as.numeric(args[7]), # temperature lower threshold 5
	TUT = as.numeric(args[8]), # temperature upper threshold 26
	# half saturation constant for food
	Kf = as.numeric(args[9]),  #mg chl/m3
	# O2 lower threshold
	O2LT = as.numeric(args[10]),
	# threshold resuspension
	Kr = as.numeric(args[11]), #  g-POM/m2/d
	decay_dd = as.numeric(args[12]) # exp decay
)


########## Functions  ##########

#identify NetCdf files, read data and calculate mean and SD (usefunc=SD)
getData <- function(uset,usefunc=mean) {
	if (is.null(paramLst[[uset$param]])) stop("No such parameter")
	lon=c();lat=c()
	cc=1
	for (y in uset$yrs) {
		if (y<2009 | y>2017) stop("Invalid year")
		nc = nc_open(paste0(datFldr,"nc_files_",y,"/limfjord",paramLst[[uset$param]][2],"_",paramLst[[uset$param]][1],"_",y,".nc"))
		if (cc==1) { 
			lon=ncvar_get(nc,"Lon")
			lat=ncvar_get(nc,"Lat")
			dat=array(dim=c(length(lat),length(lon),length(uset$yrs)*length(uset$mths)))
		}
		for (m in uset$mths) {
			dat[,,cc] = ncvar_get(nc,start=c(1,1,m),count=c(-1,-1,1)) #NB: assumes only one variable in nc file 
			cc=cc+1
		}
		nc_close(nc)
	}
	return(list(lon=lon,lat=lat,dat=apply(dat,1:2,usefunc)))
}

#create color coded area plot
plotData <- function(uset,dat,pngfile=NA,figname) {
	if (!exists("spcoast")) load("spdk.RData")
	if (!is.na(pngfile)) png(pngfile,width=1000,height=600)
	par(mar=c(2,2,2,2),oma=c(0,0,0,2),cex=2,mgp=c(3, .5, 0))
	plot(NA,xlim=lm[1:2],ylim=lm[3:4],asp=1,xlab="",ylab="")
	mtext(figname[1],line=0.5,cex=2)
	image(dat$lon,dat$lat,t(dat$dat),col=pal(100),add=T)
	flippedMatrix <- dat$dat[nrow(dat$dat):1,]
	rasterFormat <- raster(flippedMatrix, xmn=8.186484, xmx=10.2941, ymn=56.46693, ymx=57.09677, crs="EPSG:4326")
	writeRaster(rasterFormat, paste0(datFldr,"Bulletin/", uset$param), format = "GTiff", overwrite=TRUE)
	plot(spcoast,col="#B4D79E",axes=T,add=T,lwd=1,border="grey")
	image.plot(dat$dat, col = pal(100), legend.shrink = 0.98, ann = F,legend.only=T,legend.width = 2,legend.mar=0,legend.args=list(text=figname[2], side=3, font=3, line=0, cex=1.1))
	if (!is.na(pngfile)) dev.off()
}

calcSSI <- function(uset,meandat) {
	ssi=NA
	if (uset$param=="fsal") {
		slope = 1/(uset$SUT-uset$SLT)
		ssi = slope*(meandat-uset$SLT)
		ssi[ssi <0] <- 0
		ssi[ssi >1] <- 1
	} else if (uset$param=="ftem") {
	  slope = 1/(uset$TUT-uset$TLT)
	  ssi = slope*(meandat-uset$TLT)
	  ifelse(ssi < 0, 0, ssi)
	  ifelse(ssi > 1, 1, ssi)
	} else if (uset$param=="fchl") {
		cchl = 6.625*12/2 #conversion from mgChl/m3 to to mg-C/m3
		food = meandat*cchl
		ssi <- food/(food+uset$Kf*cchl)
	} else if (uset$param=="foxy") {
		oxyconv = 32/1000 # from mmol-O2/m3 to mg-O2/l
		hypox = meandat*oxyconv
		ssi <- hypox/max(hypox,na.rm=TRUE)
		ssi[hypox<uset$O2LT] <- 0
	} else if (uset$param=="fres") {
		CN = 6.625*12 #conversion from mmol-N/m3 to to mg-C/m3
		SPM_conv = 0.2*1000 # from ugC/l to mgPOM/l
		tstep = 150 #sec in model
		seddep = 0.1 # depth of sediment layer (m)
		resup = meandat*CN/SPM_conv/tstep*86400*seddep
		resth = (resup - uset$Kr)
		resth[resth <0] <- 0
		ssi = exp(resth*uset$decay_dd)
	} else stop("Unsupported Site Selection Index parameter")
	ssi <- ssi/max(ssi,na.rm=TRUE) #normalize
	return(ssi)
}

doAll <- function(figname,uset,pngfile="plot.png",usefunc=mean) {
	if (is.null(paramLst[[uset$param]])) stop("No such parameter")
	if (uset$param=="ssi") {
		#special case for site selection index
		tset=uset; tset$param="fsal"; dat=getData(tset); fsal=calcSSI(tset,dat$dat)
		tset=uset; tset$param="ftem"; dat=getData(tset); ftem=calcSSI(tset,dat$dat)
		tset=uset; tset$param="fchl"; dat=getData(tset); fchl=calcSSI(tset,dat$dat)
		tset=uset; tset$param="foxy"; dat=getData(tset); foxy=calcSSI(tset,dat$dat)
		tset=uset; tset$param="fres"; dat=getData(tset); fres=calcSSI(tset,dat$dat)
		ssi = fchl*foxy*fsal*ftem*fres
		ssi <- ssi/max(ssi,na.rm=TRUE) #normalize
		dat$dat=ssi
	} else {
		dat=getData(uset,usefunc)
		if (paramLst[[uset$param]][3]) dat$dat=calcSSI(uset,dat$dat)
	}
	plotData(uset,dat,pngfile,figname)
}


#Examples of use
#test=getData("botsalt")
uset=defSet; uset$param="botsalt"; doAll(names$botsalt,uset,pngfile="output/botsalt.png")
uset=defSet; uset$param="bottemp"; doAll(names$bottemp,uset,pngfile="output/bottemp.png")
uset=defSet; uset$param="chl"; doAll(names$chl,uset,pngfile="output/chl.png")
uset=defSet; uset$param="oxy"; doAll(names$oxy,uset,pngfile="output/oxy.png")
uset=defSet; uset$param="resup"; doAll(names$resup,uset,pngfile="output/resup.png")
uset=defSet; uset$param="fsal"; doAll(names$fsal,uset,pngfile="output/fsal.png")
uset=defSet; uset$param="ftem"; doAll(names$ftem,uset,pngfile="output/ftem.png")
uset=defSet; uset$param="fchl"; doAll(names$fchl,uset,pngfile="output/fchl.png")
uset=defSet; uset$param="foxy"; doAll(names$foxy,uset,pngfile="output/foxy.png")
uset=defSet; uset$param="fres"; doAll(names$fres,uset,pngfile="output/fres.png")
uset=defSet; doAll(names$ssi,uset,pngfile="output/ssi.png") #everything

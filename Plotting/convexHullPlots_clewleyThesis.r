# Plots to show sensitivity analysis of inversion with varying levels of noise
# using a convex hull as presented in:
#
# Clewley, D. 2012. Retreival of Forest Structure and Biomass From Radar Data using 
# Backscatter Modelling and Inversion. PhD Thesis. Aberystwyth University.
#
# The plots are skewed towards outliers but provide a simple way of identifying a bias in inversion results.

library(spatstat)

# Read in results for different levels of noise
# Each file contains input (true) and inverted values.
inFile0_2dCG = as.data.frame(read.csv("bgl_2dCGtest_InvResults0.csv"))
inFile1_2dCG = as.data.frame(read.csv("bgl_2dCGtest_InvResults1.csv"))
inFile5_2dCG = as.data.frame(read.csv("bgl_2dCGtest_InvResults5.csv"))
inFile10_2dCG = as.data.frame(read.csv("bgl_2dCGtest_InvResults10.csv"))
inFile15_2dCG = as.data.frame(read.csv("bgl_2dCGtest_InvResults15.csv"))
inFile20_2dCG = as.data.frame(read.csv("bgl_2dCGtest_InvResults20.csv"))

pdf(file="bgl_2DataCG.pdf", width=13, height=7)
layout(matrix(1:2, nrow=1))
par(mar=c(6, 6, 0.5, 0.5))
par(font.lab=2)
par(cex.axis=1.5) 
par(cex.lab=1.5)
legendText = c("0% (data points)", "1%", "5%", "10%", "15%", "20%" )
legendSymb = c(21,"","","","","")
legendCol = c(rgb(0,1,0,0),rgb(0,1,0,1), rgb(0,0.5,0,1),rgb(1,1,0,1),rgb(1,0.7,0,1),rgb(1,0,0,1))
legendColBg = c(rgb(0,1,0,0),rgb(0,1,0,0.5), rgb(0,0.5,0,0.5),rgb(1,1,0,0.5),rgb(1,0.7,0,0.5),rgb(1,0,0,0.5))
pchCol = c("black",rgb(0,0,0,0),rgb(0,0,0,0),rgb(0,0,0,0),rgb(0,0,0,0),rgb(0,0,0,0))

# Canopy depth
plot(inFile20_2dCG$realCDepth, inFile20_2dCG$eCDepth, type="n", xlab="Canopy Depth (m)", ylab="Estimated Canopy Depth (m)", xlim=c(0,3), ylim=c(0,3))

plot(convexhull.xy(cbind(inFile20_2dCG$realCDepth, inFile20_2dCG$eCDepth)), col=rgb(1,0,0,0.1), border=rgb(1,0,0,1),  add=TRUE)
plot(convexhull.xy(cbind(inFile15_2dCG$realCDepth, inFile15_2dCG$eCDepth)), col=rgb(1,0.7,0,0.1), border=rgb(1,0.7,0,1), add=TRUE)
plot(convexhull.xy(cbind(inFile10_2dCG$realCDepth, inFile10_2dCG$eCDepth)), col=rgb(1,1,0,0.1), border=rgb(1,1,0,1),  add=TRUE)
plot(convexhull.xy(cbind(inFile5_2dCG$realCDepth, inFile5_2dCG$eCDepth)), col=rgb(0,0.5,0,0.1), border=rgb(0,0.5,0,1), add=TRUE)
plot(convexhull.xy(cbind(inFile1_2dCG$realCDepth, inFile1_2dCG$eCDepth)), col=rgb(0,1,0,0.1), border=rgb(0,1,0,1), add=TRUE)
points(inFile0_2dCG$realCDepth, inFile0_2dCG$eCDepth, pch=21)
lines(seq(0,10),seq(0,10), lty=2)
legend("topleft", legendText, pch=21, col=pchCol, border=legendCol, fill=legendColBg, bty="n", cex=1.5)

# Canopy Density
plot(inFile20_2dCG$realCDens, inFile20_2dCG$eCDens, type="n", xlab=expression(bold(paste("Canopy Density (crowns ",m^-2,")"))), ylab=expression(bold(paste("Estimated Stem Density (stems ",m^-2,")"))), xlim=c(0,2), ylim=c(0,2))

plot(convexhull.xy(cbind(inFile20_2dCG$realCDens, inFile20_2dCG$eCDens)), col=rgb(1,0,0,0.1), border=rgb(1,0,0,1),  add=TRUE)
plot(convexhull.xy(cbind(inFile15_2dCG$realCDens, inFile15_2dCG$eCDens)), col=rgb(1,0.7,0,0.1), border=rgb(1,0.7,0,1), add=TRUE)
plot(convexhull.xy(cbind(inFile10_2dCG$realCDens, inFile10_2dCG$eCDens)), col=rgb(1,1,0,0.1), border=rgb(1,1,0,1),  add=TRUE)
plot(convexhull.xy(cbind(inFile5_2dCG$realCDens, inFile5_2dCG$eCDens)), col=rgb(0,0.5,0,0.1), border=rgb(0,0.5,0,1), add=TRUE)
plot(convexhull.xy(cbind(inFile1_2dCG$realCDens, inFile1_2dCG$eCDens)), col=rgb(0,1,0,0.1), border=rgb(0,1,0,1), add=TRUE)
points(inFile0_2dCG$realCDens, inFile0_2dCG$eCDens, pch=21)
lines(seq(0,2,by=0.1),seq(0,2,by=0.1), lty=2)

dev.off()

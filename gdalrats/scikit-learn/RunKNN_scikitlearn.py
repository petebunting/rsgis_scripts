from sklearn.neighbors import KNeighborsClassifier

from rios import rat
import numpy
import osgeo.gdal as gdal

clumpsImg='./N00E103_10_grid_knn_skl.kea'

# Open dataset
ratDataset = gdal.Open(clumpsImg, gdal.GA_Update)

# Import Columns
print("Importing Columns")
HH = rat.readColumn(ratDataset, "HH")
HV = rat.readColumn(ratDataset, "HV")
NDVI = rat.readColumn(ratDataset, "NDVI")
NDWI = rat.readColumn(ratDataset, "NDWI")
Training = rat.readColumn(ratDataset, "Training")
LCClass = rat.readColumn(ratDataset, "Class")
ApplyTo = rat.readColumn(ratDataset, "ApplyTo")

# Form array of all columns
XTrain = numpy.array([HH,HV,NDVI,NDWI])
XTrain = XTrain.transpose()

# Keep only finite values
XTrain = XTrain[numpy.isfinite(XTrain).all(axis=1)]
CTrain = LCClass[numpy.isfinite(XTrain).all(axis=1)]

# Keep only Coastal strip values
XTrain = XTrain[Training == 1]
CTrain = CTrain[Training == 1]

print(XTrain.shape)
print(CTrain.shape)
nsamples = XTrain.shape[0]

print('Calculate Covariance Matrix')
#  BUG MAYBE??? REALLY SLOW AND TAKES LOTS OF MEMORY!!
#xTrainCov = numpy.cov(XTrain)

mean = numpy.mean(XTrain,axis=0)
# make a mean matrix the same shape as data for subtraction
mean_mat = numpy.outer(numpy.ones((nsamples,1)),mean)
xTrainCov = XTrain - mean_mat
xTrainCov = numpy.dot(xTrainCov.T,xTrainCov)/(nsamples -1)
print(xTrainCov)

print('Create Classifier')
neigh = KNeighborsClassifier(n_neighbors=12, metric='mahalanobis', V=xTrainCov)

print('Training Classifier')
neigh.fit(XTrain, CTrain)

print('Calc Accuracy',)
accVal = neigh.score(XTrain, CTrain)
print(' = ', accVal)

# Create array of IDs (to keep track of the original row number)
ID = numpy.arange(Training.shape[0])

# Form array of all columns
XClass = numpy.array([HH,HV,NDVI,NDWI])
XClass = XClass.transpose()

XClass = XClass[numpy.isfinite(XClass).all(axis=1)]
ID = ID[numpy.isfinite(XClass).all(axis=1)]
XClass = XClass[ApplyTo == 1]
ID = ID[ApplyTo == 1]

print('Predicting Classifier')
predClass = neigh.predict(XClass)
#predClassProb = neigh.predict_proba(XClass)
#print(predClass)

print('Create Output Array')
outLabels = numpy.zeros_like(ApplyTo,dtype=numpy.int16)
outLabels[...] = -1
outLabels[ID] = predClass

print("Writing Columns")
rat.writeColumn(ratDataset, "ClassOut", outLabels)

ratDataset = None



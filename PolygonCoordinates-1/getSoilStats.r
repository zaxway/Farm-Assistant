library(soilDB)
library(sp)
library(rgdal)
library(plyr)
library(raster)
library(rgeos)

# copy contents of getCoordinates.txt file to c()
b <- c(-111.96279,-111.86975,33.48472,33.53625)

# convert bounding box to WKT
p <- writeWKT(as(extent(b), 'SpatialPolygons'))
# compose query, using WKT BBOX as filtering criteria
q <- paste0("SELECT mukey, cokey, compname, comppct_r, taxclname
           FROM component
           WHERE mukey IN (SELECT DISTINCT mukey FROM SDA_Get_Mukey_from_intersection_with_WktWgs84('", p, "') )
           ORDER BY mukey, cokey, comppct_r DESC")

res <- SDA_query(q)
write.csv(res, "soil_composition.csv")

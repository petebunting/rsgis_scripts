
var image = ee.Image('LC8_L1T/LC82040242013139LGN01');

var wbi = image.expression(
    'blue/nir',
    {
        blue: image.select('B2'),    // BLUE
        nir: image.select('B5'),    // NIR
    });


Map.centerObject(wbi);
Map.addLayer(wbi);


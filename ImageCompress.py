#This is a very basic attempt at compressing a simple bitmap file.  Feel free to make fun.
#For simplicity sake, it's limited to 256 colors.  I have no idea how I'm going to make it smaller but...
#what the heck.  It's for fun.

from PIL import Image

class Compression:
    colorList = []
    pixels = []
    width = 0
    height = 0
    image = Image.Image()

    def __init__(self):
        pass

    def __init__(self, image: Image.Image):
        self.width = image.width
        self.height = image.height
        self.image = image

    def populateColorsAndPixels(self):
        pixelNum = 0

        self.colorList = []
        self.pixels = [0] * (self.width * self.height)

        for x in range(self.height):
            for y in range(self.width):
                pixel = self.image.getpixel([y,x])
                if not pixel in self.colorList:
                    self.colorList.append(pixel)
                
                self.pixels[pixelNum] = self.colorList.index(pixel)
                pixelNum += 1

    def buildHeader(self):
        header = [self.width.to_bytes(2, 'big').hex(),
            self.height.to_bytes(2, 'big').hex(),
            len(self.colorList).to_bytes(1, 'big').hex(),
            "".join("".join(channel.to_bytes(1, 'big').hex() for channel in color) for color in self.colorList)]
        
        return "".join(header)

    def buildPixelString(self):
        skip = 1 if len(self.colorList) < 9 else 0

        return "".join(pixel.to_bytes(1, 'big').hex()[skip:] for pixel in self.pixels)

    def compressionString(self):
        retVal = ""

        if (self.width > 0 and self.height > 0):
            self.populateColorsAndPixels()
            retVal = "".join([self.buildHeader(),  self.buildPixelString()])

        return retVal
    
    
file = Image.open("C:\git\PythonLearning\inputImage.bmp")

converted = file.convert('RGB')

compress = Compression(converted)

compressedPixels = compress.compressionString()[40:]

chunks = [compressedPixels[i:i+(converted.width)] for i in range(0, len(compressedPixels), (converted.width))]

print('\n'.join(chunks))


file.close()




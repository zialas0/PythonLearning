#This is a very basic attempt at compressing a simple bitmap file.  Feel free to make fun.
#For simplicity sake, it's limited to 256 colors.  I have no idea how I'm going to make it smaller but...
#what the heck.  It's for fun.

from PIL import Image

class _Helpers:
    def hexDigits(num: int):
        return len(hex(num))-2

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
        skip = 1 if _Helpers.hexDigits(len(self.colorList)) > 1 else 0

        return "".join(pixel.to_bytes(1, 'big').hex()[skip:] for pixel in self.pixels)

    def compressionString(self):
        retVal = ""

        if (self.width > 0 and self.height > 0):
            self.populateColorsAndPixels()
            retVal = "".join([self.buildHeader(),  self.buildPixelString()])

        return retVal
    
    #decompression side
    def decompressToImage(self, hex: str):
        if len(hex) > 10:
            
            self.width = int(hex[:4], 16)
            self.height = int(hex[4:8], 16)
            
            #fill color list
            self.colorList = []

            colorListLength = int(hex[8:10], 16)
            colorListString = hex[10:(10 + (colorListLength * 6))]
            pixelString = hex[(10 + (colorListLength * 6)):]

            for color in range(0, colorListLength):
                #need to add checking for lengths greater than 16
                index = color * 6
                
                #separate RGB values
                red = int(colorListString[index:index+2],16)
                green = int(colorListString[index+2:index+4], 16)
                blue = int(colorListString[index+4:index+6], 16)

                self.colorList.append([red,green, blue])

            #fill image pixels
            outImage = Image.new("RGB", (self.width, self.height))
            
            pixelIndex = 0
            pixelSize = 2 if _Helpers.hexDigits(colorListLength) > 1 else 1

            for y in range(0, self.height):
                for x in range(0, self.width):
                    outImage.putpixel((x, y), tuple(self.colorList[int(pixelString[pixelIndex: pixelIndex + pixelSize])]))
                    pixelIndex = pixelIndex + pixelSize

            #save image
            outImage.save("outImage.bmp", format="BMP")



    
    
# with Image.open("C:\git\PythonLearning\inputImage.bmp") as file:

#     converted = file.convert('RGB')

#     compress = Compression(converted)

#     with open("outCompress.txt", "w") as compressedFile:
#         compressedFile.write(compress.compressionString())

with open("outCompress.txt") as file:
    outImage = Image.Image()
    compress = Compression(outImage)
    compress.decompressToImage(file.read())

    print(compress.width)
    print(compress.height)
    print(compress.colorList)






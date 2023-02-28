import random

from PIL import Image


def two_of_two(filename):
    original = Image.open(filename)
    
    original = original.convert("1")
    #convert the image to grayscale image
    o_pixels = original.load() 
    print("Size of input image is ",original.size)
    first = Image.new("1", (original.size[0], original.size[1]))
    f_pixels = first.load()
    #f_pixels is used to store the pixels of first secret image
    second = Image.new("1", (original.size[0], original.size[1]))
    s_pixels = second.load()
    #s_pixels is used to store the pixels of second secret image
    for i in range(original.size[0]):
        for j in range(original.size[1]):
            if o_pixels[i,j] == 0:
                if random.randint(0, 1):
                    f_pixels[i,j] = 1
                    s_pixels[i,j] = 0
                else:
                    f_pixels[i,j] = 0
                    s_pixels[i,j]    = 1
            else:
                if random.randint(0, 1):
                    f_pixels[i,j] = 0
                    s_pixels[i,j] = 0
                else:
                    f_pixels[i,j] = 1
                    s_pixels[i,j] = 1
    print("Generated 2 shares")
    
    first.save(filename + "_share1.png")
    second.save(filename + "_share2.png")
    print("Size of share 1 image is ",first.size)
    print("Size of share 2 image is ",second.size)
    background = first.convert("RGB")
    overlay = second.convert("RGB")

    new_img = Image.blend(background, overlay, 0.5)
    new_img.save(filename+"_generated.png","PNG")
    

if __name__ == '__main__':
    ImageName=input("Enter the secret image : ")
    two_of_two(ImageName)


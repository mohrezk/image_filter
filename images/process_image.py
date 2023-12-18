import multiprocessing
from PIL import Image, ImageFilter
import time
import os 
import numpy as np
import pilgram

# from skimage import filters

class Process:
    def __init__(self, filter, user):
        filters = {
            "Crop": self.crop_image,
            "Resize": self.resize_image,
            "Gray": self.gray_filter,
            "Brightness": self.image_brightness,
            "Lofi": self.pilgram_lofi,
            "1977": self.pilgram_1977,
            "Aden": self.pilgram_aden,
        }
        self.f = filter
        self.filter = filters[filter]
        self.user = user

    # def apply_gaussian_blur(image):
    #     blurred_img = filters.gaussian(image, sigma=2)

    #     return blurred_img * 255

    def pilgram_lofi(self, image):
        img = Image.fromarray(image)
        img = pilgram.lofi(img)

        return np.array(img)

    def pilgram_1977(self, image):
        img = Image.fromarray(image)
        img = pilgram._1977(img)

        return np.array(img)
    

    def pilgram_aden(self, image):
        img = Image.fromarray(image)
        img = pilgram.aden(img)

        return np.array(img)
    

    def gray_filter(self, region):
        return np.sum(region, axis=2) // 3


    def crop_image(self, image):
        # Implement your crop logic here
        height, width, _  = image.shape
        crop_height = height // 2
        crop_width = width // 2
        cropped_region = image[:crop_height, :crop_width, :]
        return cropped_region

    def resize_image(self, image):
        img = Image.fromarray(image)

        resized_img = img.resize((300, 300))
        resized_img = np.array(resized_img)

        return resized_img


    def image_brightness(self, image):
        brightened_array = np.clip(image * 1.5, 0, 255).astype(np.uint8)
        return brightened_array

    

    def apply_filter_on_multiple(self, image):
        
        img = Image.open(image)
        data = np.array(img)

        result = self.filter(data)
        
        image = os.path.basename(image)

        mode = ""
        if self.f == "Gray" or img.mode == "L": 
            mode = "L"
        else:
            mode = "RGB"
        processed_img = Image.fromarray(result.astype(np.uint8), mode=mode)

        processed_img.save(f"media/uploaded_images/{self.f}_{image}")

        return f"media/uploaded_images/{self.f}_{image}"


    def apply_filter_on_one(self, image):
        
        img = Image.open(image)
        data = np.array(img)

        if self.f != "Crop":
            regions = np.array_split(data, 4) 

        else:
            regions = np.array_split(data, 1) 
        
        pool = multiprocessing.Pool(4)
        result = pool.map(self.filter, regions)
        pool.close()
        pool.join()

        values = np.concatenate(result)

        image = os.path.basename(image)

        mode = ""
        if self.f == "Gray" or img.mode == "L":
            mode = "L"
        else:
            mode = "RGB"

        processed_img = Image.fromarray(values.astype(np.uint8), mode=mode)

        processed_img.save(f"media/uploaded_images/{self.f}_{image}")

        return f"media/uploaded_images/{self.f}_{image}"


    def process_image(self, images):

        start = time.time()

        result = 0
        if type(images) == type([]):  

            pool = multiprocessing.Pool(4)
            result = pool.map(self.apply_filter_on_multiple, images)
            pool.close()
            pool.join()


        else:
            result = self.apply_filter_on_one(images)


        end = time.time()


        print("======================================================")
        print(end - start)
        print("======================================================")

    
        return result
    


        # with multiprocessing.Pool(6) as executor:
        #     executor.map(apply_filter, images)

        # for i in images:
        #     apply_filter(i)





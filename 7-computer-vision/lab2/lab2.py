# %%
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread, imshow
from skimage.color import rgb2hsv, rgb2gray, rgb2yuv
from skimage import color, exposure, transform
from skimage.exposure import equalize_hist

# %%

img1 = imread('Pic1.jpg')
imshow(img1)



# %%
plt.figure(figsize=(8, 6), constrained_layout=False)

img_fft = np.fft.fft2(img1)
img_fftshift = np.fft.fftshift(img_fft)
img_ifftshit = np.fft.ifftshift(img_fftshift)
img_ifft = np.fft.ifft2(img_ifftshit)

plt.subplot(231), plt.imshow(img1, "gray"), plt.title("Original Image")
plt.subplot(232), plt.imshow(np.log(1+np.abs(img_fft)), "gray"), plt.title("log abs img_fft")
plt.subplot(233), plt.imshow(np.log(1+np.abs(img_fftshift)), "gray"), plt.title("log abs img_fftshift")
plt.subplot(235), plt.imshow(np.abs(img_ifft), "gray"), plt.title("img_ifft")

# %%

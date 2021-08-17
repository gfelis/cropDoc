# CropDoc
## Google Summer of Code 2021
### Introduction to the project

CropDoc is a Computer Vision based project that aims to help companies, competent authorities and agricultural professionals overall to detect some diseases on crops by inferring through a Deep Learning model, fed with vegetal images. The application allows the capture of such images, the display of the model results after inferring on them and displaying of this results on the Liquid Galaxy visualization system. 


<div style="text-align:center">
<img src="flaskApp/static/logos/CropDoc-logo.png" alt="drawing" width="350"/>

CropDoc has been developed as part of the Google Summer of Code 2021 program for the Liquig Galaxy organization.
</div>

## Repository structure
- **Main branch:** this is the development branch, designed to be launched on a personal computer, tested on a 64-bit Ubuntu 20.04 LTS OS.
- **Jetson branch:** this is the testing branch, designed to be launched on jetson board, tested on a NVIDIA Jetson Nano 2GB Developer Kit board with a Raspberry Pi v2.1 camera.

The main differences on the code of this two branches reside on the way that the camera video feed is provided.

## Built with

- **Deep Learning model:** Tensorflow, TensorflowLite, OpenCV, Scikit-learn, Pandas, NumPy.
- **Liquig Galaxy interaction:** Pillow, pyKML, 
- **BackEnd:** Flask, Python 3.
- **FrontEnd:** HTML, CSS, JavaScript
- **Hardware:** NVIDIA Jetson Nano 2GB Developer Kit, Raspberry Pi v2.1 camera.


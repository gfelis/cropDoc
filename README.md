# CropDoc
## Google Summer of Code 2021
### Introduction to the project

CropDoc is a Computer Vision based project that aims to help companies, competent authorities and agricultural professionals overall to detect some diseases on crops by inferring through a Deep Learning model, fed with vegetal images. The application allows the capture of such images, the display of the model results after inferring on them and displaying of this results on the Liquid Galaxy visualization system.


<p align="center">
<img src="flaskApp/static/logos/CropDoc-logo.png" alt="drawing" width="350"/>

CropDoc has been developed as part of the Google Summer of Code 2021 program for the Liquig Galaxy organization.
</p>

## External links
- <a href="https://www.kaggle.com/guillemfelis/plant-pathology-2021">Google Summer of Code archive</a>, where you can check my submission for the 2021 GSOC Program as an intern at GDG Lleida.
- <a href="https://www.kaggle.com/guillemfelis/plant-pathology-2021">Crop Doc kaggle notebook</a>, where training of the model was conducted.

## Repository structure
- **Main branch:** this is the development branch, designed to be launched on a personal computer, tested on a 64-bit Ubuntu 20.04 LTS OS.
- **Jetson branch:** this is the testing branch, designed to be launched on jetson board, tested on a NVIDIA Jetson Nano 2GB Developer Kit board with a Raspberry Pi v2.1 camera.

The main differences on the code of this two branches reside on the way that the camera video feed is provided. The final Liquid Galaxy demo is only on the jetson branch.

## Installation guide
To install the project a virtual environment will be created, if you have never used virtual environments you should first learn more here: <a href="https://realpython.com/python-virtual-environments-a-primer/">What are virtual environments?</a>
### Before Installation

Before installing, ensure you have any of the following virtual environments management system available:

- Conda or miniconda <a href="https://conda.io/projects/conda/en/latest/user-guide/install/linux.html">installation guide</a>.
- Python3 virtualenv

To install virtualenv on Linux systems, you'll need pip, a python package manager:
```
python3 -m pip install --upgrade pip
```
Then you can install virtualenv with:
```
pip install virtualenv
```

You will also need to clone the project, install git if you don't have it:
```
git clone https://github.com/gfelis/cropDoc.git
```
### Creating the virtual environment and installing
To simplify installation, a list of required packages is provided both for conda and venv, and a virtual environment can be installed using that list.

#### On conda:
You can replace \<env> by the name that you want to give to your environment.

```
conda create --name <env> --file requirements_conda.txt
```

Once created, you can activate by running:

```
conda activate <env>
```

At this point, if you are still missing any package when running the Flask server, you can install it with pip. To exit the environment:

```
conda deactivate
```

#### With virtualenv:
With the following commands first we create the environment, then we activate it and finally we install the required packages on the environment by using pip. This environment will be named "env".
```
python3 -m venv env
source env/bin/activate
pip install -r requirements_pip.txt
```
To exit the environment run:
```
deactivate
```

### Running the Flask server
With the virtual environment activated, navigate to the cropDoc/flaskApp directory and simply run:
```
python3 app.py
```
This will start the flask server, once it's launched you can navigate to `localhost:5000` on the web browser and you should be able to see CropDoc's main page.
## User's guide

For a detailed guide on the application interface, check out to the <a href="https://docs.google.com/document/d/1RHgmzBhTpD430F9Gk1A2d4GYNM8XBVVeYidUIxgw6Fw/edit?usp=sharing">user's guide</a>.

## Built with

- **Deep Learning model:** Tensorflow, TensorflowLite, OpenCV, Scikit-learn, Pandas, NumPy, training done at Kaggle.
- **Liquig Galaxy interaction:** Pillow, pyKML. 
- **BackEnd:** Flask, Python 3.
- **FrontEnd:** HTML, CSS, JavaScript
- **Hardware:** NVIDIA Jetson Nano 2GB Developer Kit, Raspberry Pi v2.1 camera.

## Project Structure
```
────cropDoc
    │   .gitignore
    |   requirements_conda.txt
    |   requirements_pip.txt
    |   README.md
    └───flaskApp
        |   app.py
        ├───model
        |   predictions.py
        |   utils.py
        |   model.tflite
        ├───parser
        |   app.conf
        |   ConfigurationFile.py
        |   GenerateKml.py
        |   global_vars.py
        |   kml_utils.py
        |   parser.py
        |   setMasterFiles.py
        |   utils.py
        ├───static
        |   ├───css
        |   |   style.css
        |   ├───images
        |   |   stats.png
        |   |   ...
        |   ├───js
        |   |   main.js
        |   |   prediction.js
        |   ├───kml
        |   |   field.kml
        |   |   orbit.kml
        |   |   slave_3.kml
        |   ├───logos
        |   |   Logos.png
        |   |   ...
        |   └───xls
        |       demo_data.xlsx
        └───templates
            index.html
            prediction.html
```
## Files description

- **requirements_conda:** required packages for a conda virtual environment.
- **requirements_pip.txt:** alternatively, required packages for a pip virtual environment.
- **flaskApp/app.py** flask server implementation.
- **flaskApp/model/predictions.py** functions to perform inferrence with the model, as well as to process the resulting probabilities.
- **flaskApp/model/utils.py** utilities to prepare the model usage.
- **flaskApp/model/model.tflite** tensorflowLite compressed model, to fit inside the jetson board limited memmory. You can check how this model was developed at my <a href="https://www.kaggle.com/guillemfelis/plant-pathology-2021">kaggle notebook.</a>
- **flaskApp/parser/app.conf** defined values for the global variables.
- **flaskApp/parser/ConfigurationFile.py** parser to load the values of the global variables.
- **flaskApp/parser/GenerateKML.py** functions to generate the KML files that will be sent to the Liquid Galaxy.
- **flaskApp/parser/global_vars.py** container for the loaded values of the global variables.
- **flaskApp/parser/kml_utils.py** functions to interact with the Liquid Galaxy.
- **flaskApp/parser/parser.py** functions to parse the data from the .xlsx files.
- **flaskApp/parser/setMasterFiles.py** used on a fresh run, to setup the Liquid Galaxy folder for the project.
- **flaskApp/parser/utils.py** data object class, used by the <span>parser</span>.py to represent the information about each field.
- **flaskApp/static/css/style.cs** style definition for the frontEnd.
- **flaskApp/static/images/** images used on the frontEnd interface.
- **flaskApp/static/images/stats.png** image sent to the Liquid Galaxy to show statistics of each field, auto-generated and overwritten for each field.
- **flaskApp/static/js/main.js** button scripts for the base page at /.
- **flaskApp/static/js/predictions.js** button scripts for the /predict page.
- **flaskApp/static/kml/field.kml** auto-generated and overwritten for each field, contains pins and polygons details.
- **flaskApp/static/kml/orbit.kml** auto-generated and overwritten for each field, simulates an orbit movement.
- **flaskApp/static/kml/slave_3.kml** displays the logos on the right most screen for a 5 screens LG system.
- **flaskApp/static/logos/Logos.png** imaged used to display logos on the LG system.
- **flaskApp/static/shots/** generated only locally, directory where the taken photos are stored.
- **flaskApp/static/xls/demo_data.xlsx** contains the coordinates of the polygons and locations to be displayed on the LG.
- **flaskApp/templates/index.html** structure for the frontEnd's base page.
- **flaskApp/templates/prediction.html** structure for the /prediction page.

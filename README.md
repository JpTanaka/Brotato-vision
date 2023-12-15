# Brotato Vision

Object detection in game Brotato using You Only Look Once (YOLO) model version 8.

Originally a project for the course INF573 - Image Analysis and Computer Vision at École Polytechnique.

Authors: Artur César(czartur) and João Tanaka(jptanaka)

![image](https://github.com/JpTanaka/Brotato-vision/assets/82896115/d5c3c25a-0429-4f68-82c6-da0cca18d221)


https://github.com/JpTanaka/Brotato-vision/assets/82896115/e1a11a9d-b791-4c0a-be0e-92c244d93adf

## Installation

1. **Clone the Repository:**
   Clone this repository to your local machine:

   ```
   git clone https://github.com/JpTanaka/Brotato-vision.git
   cd Brotato-vision
   ```

2. **Install Requirements:**
   Install the required packages from `requirements.txt` using `pip`:

   ```
   pip install -r requirements.txt
   ```

## Running the Trained Model

To use the trained model on an image or video, execute `brotato_vision.py` and provide the file type and its name as parameters.

**Example for Video:**

```
python3 brotato_vision.py --video samples/sample_video.mp4
```

**Example for Image:**

```
python3 brotato_vision.py --image samples/sample_image.jpg
```

## Feature and Template Matching

To run the feature matching and template matching algorithms, use the following commands:

**Feature Matching:**

```
python3 feature_matching.py
```

**Template Matching:**

```
python3 template_matching.py
```

<!-- TODO: add data to the repository? -->

## Data annotation

The data for this project was gathered using the source code of the game to generate the annotated data while the game was played. Due to copyright, we can only share the part of the code we used to do this, it is available in [main.gd](https://github.com/JpTanaka/Brotato-vision/blob/main/utils/main.gd) and the [add_id_field.sh](https://github.com/JpTanaka/Brotato-vision/blob/main/utils/add_id_field.sh) script to assign IDs and labels to each entity in the game..

To obtain the source code of the game, you can find it [here](https://steamcommunity.com/sharedfiles/filedetails/?id=2931079751).


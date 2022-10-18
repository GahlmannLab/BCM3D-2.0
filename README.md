<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT LOGO -->
<br />

<div align="center">
  <a href="https://github.com/GahlmannLab/BCM3D-2.0">
    <img src="logo/lab logo.png" alt="Logo" width="300" height="80">
  </a>

<h3 align="center">BCM3D 2.0</h3>



</div>





<!-- ABOUT THE PROJECT -->

## About The Project

Accurate segmentation of single bacterialcells in dense biofilms using computationallygenerated intermediate image representations



<div align="center">
  <a href="https://github.com/GahlmannLab/BCM3D-2.0">
    <img src="logo/figure3_v2.png" >
  </a>



<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Getting Started

This package was tested on a 

### Prerequisites

Tensorflow 2.x with its dependencies (CUDA, cuDNN). Please refer to CSBdeep for further instructions (http://csbdeep.bioimagecomputing.com/doc/install.html).





### Installation



2. pip install
   ```sh
   pip install BCM3D2.0
   ```
   
   

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

#### Model training

1 Use **src/IntermediateImageGenerate.py** to generate image representations from ground truth cell arrangement.

2 Use **dategen.ipynb** to generate training pairs (raw data and the corresponding image representations).

3 Use **train.ipynb** to train CNNs that will train a model.

#### Prediction

1 Use **src/preprocess.py** to apply background substraction to raw data. (optional)

2 Use **predict.ipynb** to generate segmentations







<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - yw9et@virginia.com; jz3nc@virginia.edu; ag5vu@virginia.edu

Project Link: https://github.com/GahlmannLab/BCM3D-2.0

<p align="right">(<a href="#readme-top">back to top</a>)</p>





In this repository you can find a list of scripts to generate masks with different techniques. In addition, there is the **Dockerfile** to create a docker image with all the libraries needed to run the various scripts.
## Post Process Images
The **post_process_img.py** script allows you to apply some filters to the input images to generate clean masks with smoother edges. This script is recommended when you want to create masks from depth maps.

Run the script:
```sh
python post_process_img.py -h
```
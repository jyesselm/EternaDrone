Shape_Predictor
===============
A small module for predicting the SHAPE score for a RNA secondary structure and sequence.

Please checkout our documentation website at: http://jyesselm.github.io/Eterna_Data_Fit/ 

Authors
------
Dr. Joseph Yesselman : Postdoc Associate with Rhiju Das

Dr. Rhiju Das : Assistant Professor at Stanford Univeristy

Install
------
Required python packages: numpy,matplotlib,sklearn, if you have pip or easy_install you can install each at command line.

(Special thanks to Eterna player:ElNando888 for outlining a easy way to get the dependencies)
pip install scipy

pip install ipython

pip install --upgrade distribute  # otherwise, install of matplotlib was complaining

pip install matplotlib

pip install scikit-learn

git clone git@github.com:hitrace/rdatkit.git

cd rdatkit

sudo python setup.py install

Also requires Vienna RNA package which can be downloaded from http://www.tbi.univie.ac.at/RNA/
I am currently using ViennaRNA-1.8.5.tar.gz

Lastly setup your PYTHONPATH and ShapePredictor variable in your .bashrc or .bash_profile script and source it
export PYTHONPATH=$PYTHONPATH:/InstallPath/Eterna_Data_Fit
export ShapePredictor=/InstallPath/Eterna_Data_Fit




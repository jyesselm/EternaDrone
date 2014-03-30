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
Required python packages: numpy,matlibplot,sklearn,scipy if you have pip or easy_install you can install each at command line.

Also requires, rdatkit for processing RDAT files for eterna data which can get gotten at https://github.com/hitrace/rdatkit
>>>git clone git@github.com:hitrace/rdatkit.git
>>>cd rdatkit
>>>sudo python setup.py install

Also requires Vienna RNA package which can be downloaded from http://www.tbi.univie.ac.at/RNA/
I am currently useing ViennaRNA-1.8.5.tar.gz

Lastly setup your PYTHONPATH and ShapePredictor variable in your .bashrc or .bash_profile script and source it
export PYTHONPATH=$PYTHONPATH:/InstallPath/Eterna_Data_Fit
export ShapePredictor=/InstallPath/Eterna_Data_Fit




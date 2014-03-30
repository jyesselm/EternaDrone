Model Testing
========

model testing is a key part of this project either by machine learning or by custom user rules. 

Both types of models can be tested with the test_model.py  

Machine Learned Model
--------

	.. code-block:: python

		#when called without arguments runs model on all saved constructs
		#using machine learned model
		test_model.py 
		>>>Correlation with eterna score (0.85291285713383591, 0.0)

		#can test specific sequence/secondary structure with machine 
		#learned model
		test_model.py -seq "AAAAAAAA" -ss "((....))"
		>>> AAAAAAAA ((....)) 33.1084278079

Custom Specified Model
--------
test_model.py can also be used on any possible model. models can be specified with -model model_filename

.. code-block:: python

		#when called without arguments runs model on all saved constructs
		test_model.py -model model_filename
		>>>Correlation with eterna score (0.12447114870578581, 2.2421628634213801e-27)

		#can test specific sequence/secondary structure with machine 
		test_model.py -seq "AAAAAAAA" -ss "((....))" -model model_filename
		>>> AAAAAAAA ((....)) 160.2

Model file format is as follows

	.. code-block:: python

		cat model_filename
		>>>#Score Function 1
		>>>100 - (percent_au - 0.45) * 0.75 + melting_temp

		cat model_filename2
		>>>#Score Function 1
		>>>100 - (percent_g - 0.45) / free_energy
		>>>#Score Function 2
		>>>n_pairs + melting_temp

You can specify unlimited number of functions using any of the features currently implemented. Here are all the features currently implemented they are also found in the example model file

	.. code-block:: python

		###Sequence Features###
		percent_a : number of As / total length of sequence
		percent_u : number of Us / total length of sequence
		percent_g : number of Gs / total length of sequence
		percent_c : number of Cs / total length of sequence
		max_a_repeat : max stretch of As, ex. AAAUAC => 3
		max_u_repeat : max stretch of Us
		max_g_repeat : max stretch of Gs
		max_c_repeat : max stretch of Cs
		###Structure Features###
		percent_au : number of AU basepairs / number of basepairs (given by target secondary structure)
		percent_gc : number of GC basepairs / number of basepairs
		percent_wc : number of Waston-Crick (AU and GC) basepairs / number of basepairs
		percent_nc : number of Nonconical (Not AU and GC)  basepairs / number of basepairs
		n_basepairs : number of basepairs (given by target secondary structure)
		not_capped_loops : inspired by Eli Fisker (Eterna Proplayer), number of bulges/hairpins/junctions that do NOT have a GC pair at their edge
		not_stem_capped : number of stems (basepair stretches) that do not start with a GC pair at the edge
		###Vienna Features###
		avg_structure_diff : number of structures that differ between target structure and vienna predicted structure
		free_energy: the vienna calculated free energy
		#melting_temp: the temperature at which vienna predicts 0 free energy
		mfe_prob: frequency of mfe structure in ensemble
		ensemble_diversity: vienna's ensemble diversity parameter











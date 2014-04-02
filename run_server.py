import cherrypy
import os

import matplotlib.pyplot as plt
from scipy.stats import *

from eterna_drone.util import *
from eterna_drone.feature_generator_factory import *
 
MEDIA_DIR = os.path.join(os.path.abspath("."))
data_path = os.environ["EternaDrone"]+"/EternaDrone/data/"
feature_generators = FeatureGeneratorFactory.all_generators() 

predictor = pickle.load( open( data_path+"predictor.p", "rb" ) )
all_constructs = pickle.load(open(data_path+"constructs.p","rb"))

features = all_constructs[0].features.keys()
features.sort(key = lambda x : len(x), reverse=True)

class rest:
	@cherrypy.expose
	def index(self):
		return open(os.path.join(MEDIA_DIR, u'media/index.html'))

	@cherrypy.expose
	def posted(self, sequence, structure):

		construct = Construct(sequence,structure,0)
		constructs = [construct]
		populate_features_for_constructs(constructs,feature_generators)
	
		#features = constructs[0].features.keys()
		#features.sort(reverse=True)

		real_scores = []
		all_data = []
		for c in constructs:
			data = []
			for f in features:
				data.append(c.features[f])
			real_scores.append(float(c.eterna_score))
			all_data.append(data)

		predicted_scores = predictor.predict(all_data)
		f = open(os.path.join(MEDIA_DIR, u'media/Score_Seq_SS_Result.html')) 
		lines = f.readlines()
		f.close()

		string = "".join(lines)
		string += """
		<br/>
		<hr>
		<p class=\"lead\">
		Sequence:  %s<br/>
		Structure: %s<br/>
		Score:     %s</p>
		</div>
		</div>
		</body>
		</html>""" % (sequence,structure,predicted_scores[0])
		return string

	@cherrypy.expose
	def posted_2(self, model):
		compiled_model = compile_model_from_str(model,features)

		real_scores = []
		predicted_scores = []

		for c in all_constructs:
			#set the correct local variable name for the compiled code object
			construct = c
			exec compiled_model
			real_scores.append(float(c.eterna_score))
			#local variable score gets set by exec model, see parse_model_file
			predicted_scores.append(score)

		R = pearsonr(real_scores,predicted_scores)
		#R = [0,0]

		f = open(os.path.join(MEDIA_DIR, u'media/Test_Your_Model_Result.html')) 
		lines = f.readlines()
		f.close()

		string = "".join(lines)
		string += """
		<br/>
		<hr>
		<p class=\"lead\">
		Model:          %s<br />
		R Correlation:  %s
		</p>
		</div>
		</div>
		</body>
		</html>""" % (model,R[0])
		return string

if __name__ == "__main__":

	cherrypy.config.update( {
		'server.socket_host':"0.0.0.0", 
		'server.socket_port':8181,
		'tools.staticdir.root': os.path.abspath(os.path.join(os.path.dirname(__file__), ''))
		#'tools.statiddir.root': "/Users/skullnite/Downloads"
	} )
	#print os.path.abspath(os.path.join(__file__, 'static'))
	#cherrypy.quickstart( rest(), '/', 'development.conf' )
	
	cherrypy.quickstart(rest(), '', config={
		'/css': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'css'
			},
		'/images': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'images'
			},
		'/media': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'media'
			},
		}
	)






from flask import Flask
from flask import send_from_directory, send_file
from flask_restful import Resource, Api, reqparse
from semi import SuperFactory, SuperMeta
import random
import json
import os
import asyncio

app = Flask(__name__)
api = Api(app)

class SemiMetaData(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('tokenId', type=int)
		args = parser.parse_args()
		token_id = args['tokenId'] if args['tokenId'] is not None else random.randint(0, 5554)
		semi_meta = SuperMeta.load()[token_id]
		return {args['tokenId']: json.loads(json.dumps(semi_meta, default=lambda s: vars(s)))}, 200  # return data with 200 OK

class SemiPFP(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('tokenId', type=int)
		args = parser.parse_args()
		token_id = args['tokenId'] if args['tokenId'] is not None else random.randint(0, 5554)
		semi = SuperFactory.get(token_id)
		return send_from_directory(os.path.join(app.root_path, semi.path), os.path.basename(os.path.normpath(semi.pfp)))

class SemiPFPTransparent(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('tokenId', type=int)
		args = parser.parse_args()
		token_id = args['tokenId'] if args['tokenId'] is not None else random.randint(0, 5554)
		semi = SuperFactory.get(token_id)
		return send_from_directory(os.path.join(app.root_path, semi.path), os.path.basename(os.path.normpath(semi.pfp_nobg)))

class SemiPFPCustom(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('tokenId', type=int)
		parser.add_argument('traits', type=str)
		args = parser.parse_args()
		token_id = args['tokenId'] if args['tokenId'] is not None else random.randint(0, 5554)
		traits = args['traits'].split(',') if args['traits'] is not None else SuperMeta.trait_types
		img = asyncio.run(SuperFactory.pfp_custom(token_id, args['traits'].split(',')))[1]
		return send_file(img, mimetype='image/png')


class SemiGM(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('tokenId', type=int)
		args = parser.parse_args()
		token_id = args['tokenId'] if args['tokenId'] is not None else random.randint(0, 5554)
		semi = SuperFactory.get(token_id)
		return send_from_directory(os.path.join(app.root_path, semi.path), os.path.basename(os.path.normpath(semi.gm)))

class SemiGN(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('tokenId', type=int)
		args = parser.parse_args()
		token_id = args['tokenId'] if args['tokenId'] is not None else random.randint(0, 5554)
		semi = SuperFactory.get(token_id)
		return send_from_directory(os.path.join(app.root_path, semi.path), os.path.basename(os.path.normpath(semi.gn)))

class SemiHead(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('tokenId', type=int)
		args = parser.parse_args()
		token_id = args['tokenId'] if args['tokenId'] is not None else random.randint(0, 5554)
		semi = SuperFactory.get(token_id)
		return send_from_directory(os.path.join(app.root_path, semi.path), os.path.basename(os.path.normpath(semi.head)))

class SemiHeadTransparent(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('tokenId', type=int)
		args = parser.parse_args()
		token_id = args['tokenId'] if args['tokenId'] is not None else random.randint(0, 5554)
		semi = SuperFactory.get(token_id)
		return send_from_directory(os.path.join(app.root_path, semi.path), os.path.basename(os.path.normpath(semi.head_nobg)))

class SemiQuote(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('tokenId', type=int)
		parser.add_argument('quote', required=True)
		args = parser.parse_args()
		token_id = args['tokenId'] if args['tokenId'] is not None else random.randint(0, 5554)
		file = asyncio.run(SuperFactory.catchphrase(token_id, args['quote']))[1]
		return send_file(file, mimetype='image/png')

class SemiVS(Resource):
	def get(self):
		parser = reqparse.RequestParser()        
		parser.add_argument('tokenId', type=int)
		parser.add_argument('tokenId2', type=int)
		args = parser.parse_args()  # parse arguments to dictionary		
		token_id = args['tokenId'] if args['tokenId'] is not None else random.randint(0, 5554)
		token_id2 = args['tokenId2'] if args['tokenId2'] is not None else random.randint(0, 5554)
		file = asyncio.run(SuperFactory.vs(token_id, token_id2))[2]
		return send_file(file, mimetype='image/png')

class SemiVSGIF(Resource):
	def get(self):
		parser = reqparse.RequestParser()        
		parser.add_argument('tokenId', type=int)
		args = parser.parse_args()  # parse arguments to dictionary		
		file = asyncio.run(SuperFactory.vs_gif(args['tokenId']))
		return send_file(file, mimetype='image/gif')


api.add_resource(SemiMetaData, '/semi')
api.add_resource(SemiPFP, '/pfp')
api.add_resource(SemiPFPTransparent, '/tpfp')
api.add_resource(SemiPFPCustom, '/pfpc')
api.add_resource(SemiGM, '/gm')
api.add_resource(SemiGN, '/gn')
api.add_resource(SemiHead, '/head')
api.add_resource(SemiHeadTransparent, '/thead')
api.add_resource(SemiQuote, '/say')
api.add_resource(SemiVS, '/vs')
api.add_resource(SemiVSGIF, '/vsg')


if __name__ == '__main__':
	app.run()  # run our Flask app
import json
import cherrypy
import torch
import pickle
from pathlib import Path
from models import BERTModel
from model_args import args
import pandas as pd
import os
import numpy as np
import cherrypy_cors
cherrypy_cors.install()


class Root(object):
    def __init__(self):
        dataset = pickle.load(Path('/workspaces/MovieRec/Data/preprocessed/ml-20m_min_rating4-min_uc5-min_sc0-splitleave_one_out/dataset.pkl').open('rb'))
        self.real_u_2_u = dataset['umap']
        self.real_movie_2_movie = dataset['smap']
        with open('id_2_real_id.pickle', 'rb') as handle:
            mapping = pickle.load(handle)
            self.u_2_real_u, self.movie_2_real_movie = mapping['u_2_real_u'], mapping['movie_2_real_movie']
        self.movie_info = pd.read_csv('/workspaces/MovieRec/Data/ml-20m/movies.csv')  
        self.movie_info.columns = ['movieId', 'title', 'genres']
        item_size = len(self.movie_2_real_movie)
        print(f'item_size: {item_size}')
        args.num_items = item_size
        self.seq_len = args.bert_max_len
        self.masked_token = item_size + 1
        best_model_path = '/workspaces/MovieRec/experiments/test_2022-03-14_0/models/best_acc_model.pth'
        model = BERTModel(args).to(device=args.device)        
        best_model = torch.load(best_model_path).get('model_state_dict')
        model.load_state_dict(best_model)
        model.eval()
        self.model = model
        self.device = args.device

        posters_file = []
        for im in os.listdir('/workspaces/MovieRec/MLP-20M'):
            real_id = int(im.split('.')[0])
            if real_id in self.real_movie_2_movie:
                posters_file.append(real_id)
        self.movie_with_posters = posters_file
        


    def model_inference(self, real_movie_seq):
        assert len(real_movie_seq) == (self.seq_len -1)
        history = torch.tensor([self.real_movie_2_movie[s] for s in real_movie_seq], dtype=torch.long).reshape(1, self.seq_len-1)
        seq = torch.cat((history, torch.tensor(self.masked_token).reshape(1, 1)), dim=1).to(device=self.device)
        scores = self.model(seq)
        movie_id = scores[:, -1, :].argmax(dim=-1).to('cpu').item()
        real_movie_id = self.movie_2_real_movie[movie_id]
        movie = self.movie_info[self.movie_info['movieId'] == real_movie_id].iloc[0]
        title, genres = movie['title'], movie['genres']
        print(f'Next recommended movie: {real_movie_id}, {title}, {genres}')
        return {'title': title, 'id': real_movie_id, 'genres': genres}
    
    def randomSelectMovies(self, count=2000):
        random_idx = np.random.choice(len(self.movie_with_posters), count, replace=False).tolist()
        movies = []
        ids = []
        for i in random_idx:
            id = self.movie_with_posters[i]
            movie = self.movie_info[self.movie_info['movieId'] == id]
            if(movie.shape[0] > 0 ):
                title, genres = movie.iloc[0]['title'], movie.iloc[0]['genres']
                movies.append({'id': id, 'title': title, 'genres': genres})
                ids.append(id)
        # print(ids)
        return {'movies': movies}

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def inference(self):
        cherrypy_cors.preflight(allowed_methods=['GET', 'POST'])
        print(cherrypy.request.json)
        input_json = cherrypy.request.json
        return self.model_inference(input_json['movie_seq']) #self.model_inference(input_json['movie_seq'])

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def randomSelect(self):
        return self.randomSelectMovies()

if __name__ == '__main__':
    cherrypy.quickstart(Root(), '/', config="server.conf")
else:
    application = cherrypy.Application(Root(), '/', config="server.conf")
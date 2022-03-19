import './App.css';
import 'antd/dist/antd.css';
import { Card, notification, Slider, Typography, Divider } from 'antd';
import React, { useState, useEffect } from 'react';

const { Title } = Typography;

const seq_buf_len = 99 // 100 - 1

function App() {
  const [movies, setMovies] = useState([]);
  const [recMovies, setRecMovies] = useState([]);
  const [updateFreq, setUpdateFreq] = useState(5);
  const [clickTime, setClickTime] = useState(0);

  let seq_buf = []
  for (let i =0; i < seq_buf_len; i++){
    seq_buf.push(1) // 1 corresponds to 0 for movie id in training
  }
  const [seq, setSeq] = useState(seq_buf);
  

  useEffect(async() => {
    const req = new Request("http://localhost:3500/randomSelect");
    const res = await fetch(req, {
      method: 'GET'
    });
    const content = await res.json();
    setMovies(content.movies)
  }, []);


  const requestInference = async() =>{
    const req = new Request("http://localhost:3500/inference");
    const res = await fetch(req, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      mode: 'cors',  // Required for customizing HTTP request headers,
      credentials: 'same-origin',

      body: JSON.stringify({movie_seq: seq})
    });
    const newMovie = await res.json();


    setRecMovies([...recMovies, newMovie])
  }

  const onClickCard = (id, titile, genres)=>{
    const args = {
      message: `User Clicks ${titile}`,
      description:
        `Genres: ${genres}`,
      duration: 10,
      placement: "topLeft"
    };
    notification.open(args);
    const current_click_time = clickTime + 1
    
    let current_seq = seq;
    current_seq.shift();
    current_seq.push(id);

    if (current_click_time >= updateFreq)
    {
      setClickTime(0);
      requestInference();
    }
    else
    {
      setClickTime(current_click_time);
    }
    setSeq(current_seq);
  }

  return (
    <div className='app'>
      <div className='navBar'>Movie Recommendation Demo using BERT</div>
      <div className='cardRoot'>
          {
            movies.map((movie)=>{
              return <MovieCard key={movie.id} title={movie.title} id={movie.id} genres={movie.genres} onClickCard={onClickCard}/>})
          }

      </div>
      <div className='predictionWindow'>
        <Title level={3} style={{textAlign: "center"}}>Update Frequency (clicks)</Title>
        <Slider onChange={(val)=>{setUpdateFreq(val);}}  style={{width: "80%", marginLeft: "50%", transform: 'translate(-50%, 0)'}} min={1} max={20} defaultValue={updateFreq}  />
        <Title level={3} style={{textAlign: "center", marginTop: "32px"}}>Recommendation</Title>
        <div className='recMovieRoot'>
        {
            recMovies.map((movie)=>{
              return <RecMovie key={movie.id} title={movie.title} id={movie.id} genres={movie.genres} />})
          }
          </div>
      </div>
    </div>
  );
}

const { Meta } = Card;

const MovieCard = ({title, genres, id, onClickCard})=>{

  return   <Card
  style={{width: 240 , marginLeft: "16px", marginRight: "16px", marginTop: "16px"}}
  onClick={()=>{onClickCard(id, title, genres)}}
  hoverable
  cover={<img alt={title} src={`http://localhost:3500/imgs/${id}.jpg`} />}
>
  <Meta title={title} description={genres} />
</Card>
}

const RecMovie = ({title, genres, id})=>{
  return   <Card
  style={{width: 320 , marginLeft: "50%", transform: "translate(-50%, 0)", marginTop: "16px", border: "2px solid black"}}
  cover={<img alt={title} src={`http://localhost:3500/imgs/${id}.jpg`} />}
>
  <Meta title={title} description={genres} />
</Card>
}



export default App;

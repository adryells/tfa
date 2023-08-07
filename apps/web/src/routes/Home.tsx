import { ChangeEvent, useState } from "react";
import Search from "../components/Search";
import { AnimeProps } from "../types/anime";
import Anime from "../components/Anime";
import classes from "./Home.module.css";
import Input from "../components/Input";
import { TFAResultProps } from "../types/tfa";

function Home (){
    const [animes, setAnimes] = useState<AnimeProps[]>([]);
    const [new_anime, setNewAnime] = useState<TFAResultProps | null>(null);
    const [dedicated_hours, setDedicatedHours] = useState(1);
    const [just_arrived, setJustArrived] = useState(true);
    const [title, setTitle] = useState("Random anime");
    const [num_episodes, setNumEpisodes] = useState(1);
    const [average_ep_duration, setAverageEpDuration] = useState(1);

    const loadAnime = async (search: string) => {
      try {
        const res = await fetch("http://127.0.0.1:8000/graphql", {
          method: "POST",
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            "variables": { "search": search },
            "query": `query ($search: String) {
              Animes {
                animes(search: $search) {
                  totalCount
                  items {
                    id
                    synopsis
                    numEpisodes
                    name
                    averageEpDuration
                    totalHours
                    totalDays
                    relatedMedia {
                      url
                      sizeTypeId
                    }
                  }
                }
              }
            }`
          })
        });
    
        if (!res.ok) {
          throw new Error("Erro na chamada da API");
        }
    
        const response_json = await res.json();
        const animes_items = response_json["data"]["Animes"]["animes"]["items"];
        
        setNewAnime(null)
        setAnimes(animes_items);
        setJustArrived(false);
    
      } catch (error: Error | any) {
        console.error("Ocorreu um erro:", error.message);
      }
    }

    const registerAnime = async (numEpisodes: number, title: string, averageMinutesPerEp: number) => {
      try {
        const res = await fetch("http://127.0.0.1:8000/graphql", {
          method: "POST",
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            "variables": {
              "availableHours": dedicated_hours,
              "numEpisodes": numEpisodes,
              "title": title,
              "averageMinutesPerEp": averageMinutesPerEp
            },
            "query": `mutation registerAnime (
              $numEpisodes: Int!,
              $averageMinutesPerEp: Float!,
              $title: String!,
              $availableHours: Float!
            ){
              CalculateTFA(inputData:{
                numEpisodes: $numEpisodes,
                averageMinutesPerEp: $averageMinutesPerEp,
                title: $title,
                availableHours: $availableHours
              }){
                result{
                  daysPredicted
                  totalDays
                  totalHours
                }
              }
            }`
          })
        });
    
        if (!res.ok) {
          throw new Error("Erro na chamada da API");
        }
    
        const response_json = await res.json();
        const result = response_json["data"]["CalculateTFA"]["result"];

        result.name = title
        result.numEpisodes = num_episodes
        result.averageEpDuration = average_ep_duration

        setJustArrived(false);
        setAnimes([]);
        setNewAnime(result);

      } catch (error: Error | any) {
        console.error("Ocorreu um erro:", error.message);
      }
    }

    const updateDedicatedHours = (e: ChangeEvent<HTMLInputElement>) => {
      const valueAsNumber = parseInt(e.target.value, 10); 
      setDedicatedHours(valueAsNumber);
    }


    const updateNumEpisodes = (e: ChangeEvent<HTMLInputElement>) => {
      const valueAsNumber = parseInt(e.target.value, 10); 
      setNumEpisodes(valueAsNumber);
    }
    

    const updateAverageEpDuration = (e: ChangeEvent<HTMLInputElement>) => {
      const valueAsNumber = parseInt(e.target.value, 10); 
      setAverageEpDuration(valueAsNumber);
    }
    

    const updateTitle = (e: ChangeEvent<HTMLInputElement>) => {
      setTitle(e.target.value);
    }

    return (
      <div>
        <section className={classes.result_container}>
          {
          just_arrived && 
          <div className={classes.intro}>
            <img src="https://www.pngplay.com/wp-content/uploads/12/Kawaii-Anime-Girl-PNG-Pic-Background.png" />
            <h2>Como usar?</h2>
            <p>Bem vindo ao TFA!!! você tem 2 opçoes: </p>
            <p>A&#41; Nos campos na area á esquerda você pode buscar por um anime já registrado em nossa base de dados <br /> e logo abaixo informar suas horas disponiveis. <br /></p>
            <p>B&#41; Caso não encontre o anime que deseja você tem a opção de registra-lo na área superior direita. </p>
          </div>
          }
        </section>

        <div className={classes.inputs_container}>
          <div className={classes.search_animes}>
            <Search loadAnime={loadAnime} />
            <Input updateDedicatedHours={updateDedicatedHours} />
          </div>

          <div className={classes.register_anime}>
            <h2>Nome do anime: </h2>
            <input type="text" placeholder="Nome do anime" onChange={updateTitle} required/>

            <h2>Duração média do episódio: </h2>
            <input type="number" placeholder="Duração média do episódio" min={1} step={0.1} onChange={updateAverageEpDuration} required/>

            <h2>Quantidade de episódios: </h2>
            <input type="number" placeholder="Quantidade de episódios" min={1} onChange={updateNumEpisodes} required/>

            <button type="submit" onClick={() => {registerAnime(num_episodes, title, average_ep_duration)}}>Confirmar</button>
          </div>
        </div>

        <div className={classes.animes_container}>
          {animes && animes.length > 0 && animes.map((anime) => (
            <Anime
              id={anime.id}
              key={anime.id}
              name={anime.name}
              synopsis={anime.synopsis}
              numEpisodes={anime.numEpisodes} 
              averageEpDuration={anime.averageEpDuration} 
              totalDays={anime.totalDays} 
              totalHours={anime.totalHours}
              dedicated_hours={dedicated_hours}
            />
          ))}
        </div>

        {new_anime && 
        <div className={classes.new_anime}>
          <h1>{new_anime.name}</h1>
          <h2>{new_anime.numEpisodes}</h2>
          <h3>{new_anime.averageEpDuration.toFixed(2)}</h3>
          <h4>{new_anime.totalDays}</h4>
          <h5>{new_anime.totalHours.toFixed(2)}</h5>
        </div>
        }
      </div>
    );
    
}

export default Home;

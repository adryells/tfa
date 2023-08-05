import { useState } from "react";
import Search from "../components/Search";
import { AnimeProps } from "../types/anime";
import Anime from "../components/Anime";
import classes from "./Home.module.css";

function Home (){
    const [animes, setAnimes] = useState<AnimeProps[]>([]);
    const [dedicated_hours, setDedicatedHours] = useState(2);

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
    
        setAnimes(animes_items);
    
      } catch (error: Error | any) {
        console.error("Ocorreu um erro:", error.message);
      }
    }

    const updateDedicatedHours = (e) => {
      console.log(e)
      setDedicatedHours(e.target.value)
    }
    

    return (
      <div>
        <Search loadAnime={loadAnime} />
        <input type="number" placeholder="digite as horas disponiveis" onChange={updateDedicatedHours}/>
        <div className={classes.animes_container}>
          {animes && animes.map((anime) => (
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
      </div>
    );
    
}

export default Home;

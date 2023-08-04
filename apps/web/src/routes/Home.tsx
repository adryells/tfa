import { useState } from "react";
import Search from "../components/Search";
import { AnimeProps } from "../types/anime";
import Anime from "../components/Anime";
import classes from "./Home.module.css";

function Home (){
    const [animes, setAnimes] = useState<AnimeProps | null>(null);

    const loadAnime = async(search: string) => {
        const res = await fetch("http://127.0.0.1:8000/graphql", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "variables": {"search": search},
                "query": `query ($search: String){
                    Animes{
                      animes(search: $search){
                        totalCount
                        items{
                          id
                          synopsis
                          numEpisodes
                          name
                          averageEpDuration
                          totalHours
                          totalDays
                        }
                      }
                    }
                  }`
            })
        })

        const response_json = await res.json()
        const animes_items = response_json["data"]["Animes"]["animes"]["items"]
        setAnimes(animes_items)
    }

    return (
      <div>
        <Search loadAnime={loadAnime} />
        <div className={classes.animes_container}>
          {animes && animes.map((anime) => (
            <Anime
              key={anime.id}
              name={anime.name}
              synopsis={anime.synopsis}
              num_episodes={anime.numEpisodes} // Change to "numEpisodes" from "num_episodes"
              average_ep_duration={anime.averageEpDuration} // Change to "averageEpDuration" from "average_ep_duration"
              total_days={anime.totalDays} // Change to "totalDays" from "total_days"
              total_hours={anime.totalHours} // Change to "totalHours" from "total_hours"
              id={anime.id}
            />
          ))}
        </div>
      </div>
    );
    
}

export default Home;

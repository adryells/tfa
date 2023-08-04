import { useState } from "react";
import Search from "../components/Search";
import { AnimeProps } from "../types/anime";

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
            <Search loadAnime={loadAnime}/>
            {animes && animes.length > 0 && <p>{animes[0].name}</p>}
        </div>
    )
}

export default Home;

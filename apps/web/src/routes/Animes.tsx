import { useEffect, useState } from "react";
import AppConfig from "../config/AppConfig";
import styles from "./Animes.module.css";
import { AnimeProps } from "../types/anime";

const config = AppConfig

function Animes(){
    const [animes, setAnimes] = useState<AnimeProps[] | null>([]);
    const [currentPage, setCurrentPage] = useState<number>(1);
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
    const [selectedAnime, setSelectedAnime] = useState<AnimeProps | null>(null);
    const [num_episodes, setNumEpisodes] = useState<number | null>(null);
    const [name, setName] = useState<string | null>("");
    const [average_ep_duration, setAverageEpDuration] = useState<number | null>(null);
    const [active, setActive] = useState<boolean | null>(null);
    const [request_change_id, setRequestChangeId] = useState<number | null>(null);
    const [synopsis, setSynopsis] = useState<string | null>("");
    const [source_data_id, setSourceDataId] = useState<number | null>(null);

    const currentPerPage = 10;
  

    const loadAnimes = async (search: string | null, page: number, per_page: number) => {
        try {
          const res = await fetch(`${config.API_URL}/graphql`, {
            method: "POST",
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              "variables": {
                "search": search,
                "page": page,
                "perpage": per_page
            },
              "query": `query($search: String, $page: Int, $perpage: Int) {
                Animes {
                  animes(search: $search, page: $page, perPage: $perpage) {
                    totalCount
                    items {
                      id
                      synopsis
                      numEpisodes
                      name
                      averageEpDuration
                      totalHours
                      active
                      totalDays
                    }
                  }
                }
              }
              `
            })
          });
      
          if (!res.ok) {
            throw new Error("Erro na chamada da API");
          }
      
          const response_json = await res.json();
          const anime_items = response_json["data"]["Animes"]["animes"]["items"];
          
          setAnimes(anime_items)
      
        } catch (error: Error | any) {
          console.error("Ocorreu um erro:", error.message);
        }
      }

      useEffect(() => {
        loadAnimes(null, currentPage, currentPerPage);
    }, [currentPage]);

    const loadPage = (page: number) => {
        setCurrentPage(page);
        loadAnimes(null, currentPage, currentPerPage);
    };

    const handleUpdateAnime = async (
        request_change_id: number | null,
        anime_id: number | null, 
        name: string | null,
        active: boolean | null,
        num_episodes: number | null,
        synopsis: string | null,
        average_ep_duration: number | null,
        source_data_id: number | null
        ) => {
      try {
        const res = await fetch(`${config.API_URL}/graphql`, {
          method: "POST",
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            "variables": {
              "request_change_id": request_change_id,
              "animeid": anime_id,
              "active": active,
              "source_data_id": source_data_id,
              "num_episodes": num_episodes,
              "synopsis": synopsis,
              "name": name,
              "average_ep_duration": average_ep_duration
            },
            "query": `mutation update_anime(
                $request_change_id: Int,
                $active: Boolean,
                $source_data_id: Int,
                $average_ep_duration: Int,
                $num_episodes: Int,
                $synopsis: String,
                $name: String,
                $animeid: Int!
              ){
                UpdateAnime(inputUpdateAnimeData:{
                  animeId: $animeid,
                  name: $name,
                  synopsis: $synopsis,
                  numEpisodes: $num_episodes,
                  averageEpDuration: $average_ep_duration,
                  sourceDataId: $source_data_id,
                  active: $active,
                  requestChangeId: $request_change_id
                }){
                  anime{
                    id
                  }
                }
              }`
          })
        });
  
        if (!res.ok) {
          throw new Error("Erro na chamada da API");
        }
  
      } catch (error: Error | any) {
        console.error("Ocorreu um erro:", error.message);
      }
    };

    
  const openModal = (anime: AnimeProps) => {
    setSelectedAnime(anime);
    setIsModalOpen(true);

    setNumEpisodes(anime.numEpisodes);
    setName(anime.name);
    setAverageEpDuration(anime.averageEpDuration);
    setActive(anime.active);

    setRequestChangeId(anime.request_change_id)
    setSynopsis(anime.synopsis)
    setSourceDataId(anime.source_data_id)
  };

  const closeModal = () => {
    setSelectedAnime(null);
    setIsModalOpen(false);

    setNumEpisodes(null);
    setName("");
    setAverageEpDuration(null);
    setActive(null);
    setRequestChangeId(null)
    setSynopsis(null)
    setSourceDataId(null)
  };


    return (
        <div className={styles.animes_container}>
            <div className={styles.animes_items}>
                {animes?.map((anime) => (
                    <div key={anime.id} className={styles.anime} onClick={() => {openModal(anime)}}>
                        <div>ID: {anime.id}</div>
                        <div>Numº episodes: {anime.numEpisodes}</div>
                        <div>Average episode duration: {anime.averageEpDuration}</div>
                        <div>Synopsis: {anime.synopsis}</div>
                        <div>Total Days: {anime.totalDays}</div>
                        <div>Total hours: {anime.totalHours}</div>
                        <div>Active: {anime.active ? "ACTIVE" : "INACTIVE"}</div>
                    </div>
                ))}
            </div>

            {isModalOpen && selectedAnime && (
                <div className={styles.modal}>
                <div className={styles.modal_content}>
                    <div>ID: {selectedAnime.id}</div>

                    <div>
              <label htmlFor="name">Username:</label>
              <input
                type="text"
                id="name"
                name="name"
                value={name ? name : ""}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div>
                <label htmlFor="synopsis">Synopsis:</label>
              <textarea
                id="synopsis"
                name="synopsis"
                value={synopsis ? synopsis : ""} // Use o valor do estado diretamente
                onChange={(e) => setSynopsis(e.target.value)}
                />

            </div>

            <div>
              <label htmlFor="source_data_id">Source Data:</label>
              <select
                id="source_data_id"
                name="source_data_id"
                value={source_data_id || 1}
                onChange={(e) => setSourceDataId(parseInt(e.target.value))}
              >
                <option value={1}>User Request</option>
                <option value={2}>My Anime List</option>
                <option value={3}>My Imagination</option>
              </select>
            </div>

            <div>
              <label htmlFor="active">Situation:</label>
              <select
                id="active"
                name="active"
                value={active !== null ? (active ? "ACTIVE" : "INACTIVE") : ""}
                onChange={(e) => setActive(e.target.value === "ACTIVE")}
              >
                <option value="ACTIVE">ACTIVE</option>
                <option value="INACTIVE">INACTIVE</option>
              </select>
            </div>

            <div>
              <label htmlFor="num_episodes">Num episodes:</label>
              <input
                type="number"
                id="num_episodes"
                name="num_episodes"
                value={num_episodes || 1}
                onChange={(e) => setNumEpisodes(parseInt(e.target.value))}
              />
            </div>

            <div>
              <label htmlFor="average_ep_duration">Average ep duration:</label>
              <input
                type="number"
                id="average_ep_duration"
                name="average_ep_duration"
                value={average_ep_duration || 1}
                onChange={(e) => setAverageEpDuration(parseInt(e.target.value))}
              />
            </div>

                    <button onClick={()=>{handleUpdateAnime(
                        request_change_id, 
                        selectedAnime.id, 
                        name,
                        active,
                        num_episodes,
                        synopsis,
                        average_ep_duration,
                        source_data_id
                        )}}>Confirm Changes</button>
                    <button onClick={closeModal}>Fechar</button>
                </div>
                </div>
      )}

            <div className={styles.pagination_bar}>
                <button onClick={() => loadPage(currentPage - 1)}>
                    &larr;
                </button>
                
                <button onClick={() => loadPage(currentPage + 1)}>
                    &rarr;
                </button>
            </div>
        </div>
    );
}

export default Animes;

import { ChangeEvent, useState } from "react";
import Search from "../components/Search";
import { AnimeProps } from "../types/anime";
import Anime from "../components/Anime";
import classes from "./Home.module.css";
import Input from "../components/Input";
import { TFAResultProps } from "../types/tfa";
import AppConfig from "../config/AppConfig";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPencilAlt } from "@fortawesome/free-solid-svg-icons";

const config = AppConfig;

function Home() {
  const [animes, setAnimes] = useState<AnimeProps[]>([]);
  const [new_anime, setNewAnime] = useState<TFAResultProps | null>(null);
  const [dedicated_hours, setDedicatedHours] = useState(1);
  const [just_arrived, setJustArrived] = useState(true);
  const [title, setTitle] = useState("Random anime");
  const [num_episodes, setNumEpisodes] = useState(1);
  const [average_ep_duration, setAverageEpDuration] = useState(1);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [selectedAnime, setSelectedAnime] = useState<AnimeProps | null>(null);
  const [request_change_num_episodes, setRequestChangetNumEpisodes] = useState<
    number | null
  >(null);
  const [name, setName] = useState<string | null>("");
  const [
    request_change_average_ep_duration,
    setRequestChangeAverageEpDuration,
  ] = useState<number | null>(null);
  const [synopsis, setSynopsis] = useState<string | null>("");
  const [reason, setReason] = useState<string>("");
  const [additional_info, setAdditionalInfo] = useState<string | null>("");

  const openModal = (anime: AnimeProps) => {
    setIsModalOpen(true);
    setSelectedAnime(anime);
  };

  const closeModal = () => {
    setSelectedAnime(null);
    setIsModalOpen(false);
    setName("");
    setAdditionalInfo("");
    setReason("");
    setSynopsis("");
    setRequestChangeAverageEpDuration(null);
    setRequestChangetNumEpisodes(null);
  };

  const loadAnime = async (search: string) => {
    try {
      const res = await fetch(`${config.API_URL}/graphql`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          variables: { search: search },
          query: `query ($search: String) {
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
                    active
                    relatedMedia {
                      url
                      sizeTypeId
                    }
                  }
                }
              }
            }`,
        }),
      });

      if (!res.ok) {
        throw new Error("Erro na chamada da API");
      }

      const response_json = await res.json();
      const animes_items = response_json["data"]["Animes"]["animes"]["items"];

      setNewAnime(null);
      setAnimes(animes_items);
      setJustArrived(false);
    } catch (error: Error | any) {
      console.error("Ocorreu um erro:", error.message);
    }
  };

  const registerAnime = async (
    numEpisodes: number,
    title: string,
    averageMinutesPerEp: number
  ) => {
    try {
      const res = await fetch(`${config.API_URL}/graphql`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          variables: {
            availableHours: dedicated_hours,
            numEpisodes: numEpisodes,
            title: title,
            averageMinutesPerEp: averageMinutesPerEp,
          },
          query: `mutation registerAnime (
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
            }`,
        }),
      });

      if (!res.ok) {
        throw new Error("Erro na chamada da API");
      }

      const response_json = await res.json();
      const result = response_json["data"]["CalculateTFA"]["result"];

      result.name = title;
      result.numEpisodes = num_episodes;
      result.averageEpDuration = average_ep_duration;

      setJustArrived(false);
      setAnimes([]);
      setNewAnime(result);
    } catch (error: Error | any) {
      console.error("Ocorreu um erro:", error.message);
    }
  };

  const handleRequestAnimeChange = async (
    animeId: number,
    reason: string,
    additionalInfo: string | null,
    name: string | null,
    synopsis: string | null,
    numEpisodes: number | null,
    averageEpDuration: number | null
  ) => {
    try {
      const res = await fetch(`${config.API_URL}/graphql`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          variables: {
            animeid: animeId,
            reason: reason,
            additional_info: additionalInfo,
            name: name,
            synopsis: synopsis,
            num_episodes: numEpisodes,
            average_ep_duration: averageEpDuration,
          },
          query: `mutation RequestAnimeChange (
            $animeid: Int!,
            $reason: String!,
            $additional_info: String,
            $name: String,
            $image_url: String,
            $synopsis: String,
            $num_episodes: Int,
            $average_ep_duration: Int
          ) {
            RequestAnimeChange(inputRequestAnimeChange:{
              animeId: $animeid,
              reason: $reason,
              additionalInfo: $additional_info,
              name: $name,
              imageUrl: $image_url,
              synopsis: $synopsis,
              numEpisodes: $num_episodes,
              averageEpDuration: $average_ep_duration
            }) {
              success
            }
          }`,
        }),
      });

      if (!res.ok) {
        throw new Error("Erro na chamada da API");
      }

      const responseJson = await res.json();
      const success = responseJson["data"]["RequestAnimeChange"]["success"];

      if (!success) {
        alert("Um erro desconhecido");
      }
    } catch (error: Error | any) {
      console.error("Ocorreu um erro:", error.message);
    }
  };

  const updateDedicatedHours = (e: ChangeEvent<HTMLInputElement>) => {
    const valueAsNumber = parseInt(e.target.value, 10);
    const validated_number = valueAsNumber > 0 ? valueAsNumber : 1;
    setDedicatedHours(validated_number);
  };

  const updateNumEpisodes = (e: ChangeEvent<HTMLInputElement>) => {
    const valueAsNumber = parseInt(e.target.value, 10);
    setNumEpisodes(valueAsNumber);
  };

  const updateAverageEpDuration = (e: ChangeEvent<HTMLInputElement>) => {
    const valueAsNumber = parseInt(e.target.value, 10);
    setAverageEpDuration(valueAsNumber);
  };

  const updateTitle = (e: ChangeEvent<HTMLInputElement>) => {
    setTitle(e.target.value);
  };

  return (
    <div>
      <section className={classes.result_container}>
        {just_arrived && (
          <div className={classes.intro}>
            <img src="/img/homegirl.png" />
            <h2>Como usar?</h2>
            <p>Bem vindo ao TFA!!! você tem 2 opções: </p>
            <p>
              A&#41; Nos campos na area á esquerda você pode buscar por um anime
              já registrado em nossa base de dados <br /> e logo abaixo informar
              suas horas disponiveis. <br />
            </p>
            <p>
              B&#41; Caso não encontre o anime que deseja você tem a opção de
              registra-lo na área superior direita.{" "}
            </p>
          </div>
        )}
      </section>

      <div className={classes.inputs_container}>
        <div className={classes.search_animes}>
          <Search loadAnime={loadAnime} />
          <Input updateDedicatedHours={updateDedicatedHours} />
        </div>

        <div className={classes.register_anime}>
          <h2>Nome do anime: </h2>
          <input
            type="text"
            placeholder="Nome do anime"
            onChange={updateTitle}
            required
          />

          <h2>Duração média do episódio: </h2>
          <input
            type="number"
            placeholder="Duração média do episódio"
            min={1}
            step={0.1}
            onChange={updateAverageEpDuration}
            required
          />

          <h2>Quantidade de episódios: </h2>
          <input
            type="number"
            placeholder="Quantidade de episódios"
            min={1}
            onChange={updateNumEpisodes}
            required
          />

          <button
            type="submit"
            onClick={() => {
              registerAnime(num_episodes, title, average_ep_duration);
            }}
          >
            Confirmar
          </button>
        </div>
      </div>

      <div className={classes.animes_container}>
        {animes &&
          animes.length > 0 &&
          animes.map((anime) => (
            <div key={anime.id} className={classes.anime}>
              <FontAwesomeIcon
                icon={faPencilAlt}
                className={classes.editIcon}
                onClick={() => openModal(anime)}
              />
              <Anime
                id={anime.id}
                name={anime.name}
                synopsis={anime.synopsis}
                numEpisodes={anime.numEpisodes}
                averageEpDuration={anime.averageEpDuration}
                totalDays={anime.totalDays}
                totalHours={anime.totalHours}
                dedicated_hours={dedicated_hours}
                active={anime.active}
                source_data_id={null}
                request_change_id={null}
              />
            </div>
          ))}
      </div>

      {new_anime && (
        <div className={classes.new_anime}>
          <div className={classes.new_anime_content}>
            <h2>Titulo: {new_anime.name}</h2>
            <p>Quantidade de episódios: {new_anime.numEpisodes}</p>
            <p>
              Duração média do episódio:{" "}
              {new_anime.averageEpDuration.toFixed(2)} minutos.
            </p>
            <p>
              São {new_anime.totalDays} dias para finalizar o anime dedicando{" "}
              {dedicated_hours}h por dia.
            </p>
            <p>
              São {new_anime.totalHours.toFixed(2)} horas para finalizar o
              anime.
            </p>
          </div>
          <img src="/img/resultgirl.png" />
        </div>
      )}

      {isModalOpen && selectedAnime && (
        <div className={classes.modal}>
          <div className={classes.modal_content}>
            <div>ID: {selectedAnime.id}</div>

            <div>
              <label htmlFor="name">Name:</label>
              <input
                type="text"
                id="name"
                name="name"
                value={selectedAnime.name || name || ""}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div>
              <label htmlFor="reason">Reason:</label>
              <textarea
                id="reason"
                name="reason"
                value={reason ? reason : ""}
                onChange={(e) => setReason(e.target.value)}
                required
              />
            </div>

            <div>
              <label htmlFor="name">Additional Info:</label>
              <input
                type="text"
                id="additional_info"
                name="additional_info"
                value={additional_info ? additional_info : ""}
                onChange={(e) => setAdditionalInfo(e.target.value)}
              />
            </div>

            <div>
              <label htmlFor="synopsis">Synopsis:</label>
              <textarea
                id="synopsis"
                name="synopsis"
                value={selectedAnime.synopsis || synopsis || ""}
                onChange={(e) => setSynopsis(e.target.value)}
              />
            </div>

            <div>
              <label htmlFor="num_episodes">Num episodes:</label>
              <input
                type="number"
                id="num_episodes"
                name="num_episodes"
                value={selectedAnime.numEpisodes || num_episodes}
                onChange={(e) =>
                  setRequestChangetNumEpisodes(parseInt(e.target.value))
                }
              />
            </div>

            <div>
              <label htmlFor="average_ep_duration">Average ep duration:</label>
              <input
                type="number"
                id="average_ep_duration"
                name="average_ep_duration"
                value={selectedAnime.averageEpDuration || average_ep_duration}
                onChange={(e) =>
                  setRequestChangeAverageEpDuration(parseInt(e.target.value))
                }
              />
            </div>

            <button
              onClick={() => {
                handleRequestAnimeChange(
                  selectedAnime.id,
                  reason,
                  additional_info,
                  name,
                  synopsis,
                  request_change_num_episodes,
                  request_change_average_ep_duration
                );
              }}
            >
              Confirm Changes
            </button>
            <button onClick={closeModal}>Fechar</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;

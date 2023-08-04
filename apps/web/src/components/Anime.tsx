import { AnimeProps } from "../types/anime";
import classes from "./Anime.module.css";

const Anime = ({
    name,
    synopsis,
    num_episodes,
    average_ep_duration,
    total_days,
    total_hours
}: AnimeProps) => {
    return (
        <div className={classes.anime}>
            <h3>{name}</h3>
            <p>{synopsis}</p>
            <p>Episódios: {num_episodes}</p>
            <p>Duração média do episódia: {average_ep_duration}</p>
            <p>São {total_days} dias para terminar de assistir.</p>
            <p>São {total_hours} horas para terminar de assistir.</p>
        </div>
    )
}

export default Anime;

import { AnimeProps } from "../types/anime";
import classes from "./Anime.module.css";

const Anime = ({
    name,
    synopsis,
    numEpisodes,
    averageEpDuration,
    totalDays,
    totalHours,
    id,
    dedicated_hours
  }: AnimeProps & { dedicated_hours: number }) => {
    return (
        <div className={classes.anime}>
            <h3>{name}</h3>
            <p>{synopsis}</p>
            <p>Episódios: {numEpisodes}</p>
            <p>Duração média do episódia: {averageEpDuration}</p>
            <p>São {totalDays * dedicated_hours} dias para terminar de assistir.</p>
            <p>São {totalHours} horas para terminar de assistir.</p>
        </div>
    )
}

export default Anime;

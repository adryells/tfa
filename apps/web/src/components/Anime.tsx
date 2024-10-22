import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { AnimeProps } from "../types/anime";
import classes from "./Anime.module.css";
import { faPencilAlt } from "@fortawesome/free-solid-svg-icons";

const Anime = ({
  name,
  synopsis,
  numEpisodes,
  averageEpDuration,
  totalDays,
  totalHours,
  dedicated_hours,
  active,
}: AnimeProps & { dedicated_hours: number }) => {
  const rounded_hours_tfa = totalHours.toFixed(2);
  const validated_dedicated_hours = dedicated_hours > 0 ? dedicated_hours : 1;
  const rounded_days_tfa = (totalDays / validated_dedicated_hours).toFixed(2);
  active;

  return (
    <div className={classes.anime}>
      <FontAwesomeIcon icon={faPencilAlt} className={classes.editIcon} />
      <h3>{name}</h3>
      <p>{synopsis}</p>
      <p>Episódios: {numEpisodes}</p>
      <p>Duração média do episódia: {averageEpDuration}</p>
      <p>São {rounded_days_tfa} dias para terminar de assistir.</p>
      <p>São {rounded_hours_tfa} horas para terminar de assistir.</p>
    </div>
  );
};

export default Anime;

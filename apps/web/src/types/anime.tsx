export type AnimeProps = {
  name: string;
  synopsis: string;
  numEpisodes: number;
  averageEpDuration: number;
  totalDays: number;
  totalHours: number;
  active: boolean | null;
  source_data_id: number | null;
  request_change_id: number | null;
  id: number;
};

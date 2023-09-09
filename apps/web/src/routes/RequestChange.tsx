import { useEffect, useState } from "react";
import { RequestChangeProps } from "../types/request_change";
import AppConfig from "../config/AppConfig";
import styles from "./RequestChange.module.css";

const config = AppConfig;

function RequestChanges() {
  const [request_changes, setRequestChanges] = useState<
    RequestChangeProps[] | null
  >([]);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const currentPerPage = 10;

  const loadRequestChanges = async (
    anime_id: number | null,
    page: number,
    per_page: number
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
            animeid: anime_id,
            page: page,
            perpage: per_page,
          },
          query: `query requestchanges ($page: Int, $perpage: Int, $animeid: Int){
                RequestChange{
                  requestChanges(page: $page, perPage: $perpage, animeId: $animeid){
                    totalCount
                    page
                    perPage
                    pages
                    items{
                      createdAt
                      id
                      changeData
                      reason
                      additionalInfo
                      active
                      accepted
                      animeId
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
      const request_change_items =
        response_json["data"]["RequestChange"]["requestChanges"]["items"];

      setRequestChanges(request_change_items);
    } catch (error: Error | any) {
      console.error("Ocorreu um erro:", error.message);
    }
  };

  useEffect(() => {
    loadRequestChanges(null, currentPage, currentPerPage);
  }, [currentPage]);

  const loadPage = (page: number) => {
    setCurrentPage(page);
    loadRequestChanges(null, currentPage, currentPerPage);
  };

  const handleUpdateRequestChange = async (
    request_change_id: number,
    accepted: boolean
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
            request_change_id: request_change_id,
            accepted: accepted,
          },
          query: `mutation update_request_change(
              $request_change_id: Int!,
              $accepted: Boolean!
            ){
              UpdateRequestChange(inputUpdateRequestChange:{
                requestChangeId: $request_change_id,
                accepted: $accepted
              }){
                requestChange{
                  id
                  accepted
                }
              }
            }`,
        }),
      });

      if (!res.ok) {
        throw new Error("Erro na chamada da API");
      }
    } catch (error: Error | any) {
      console.error("Ocorreu um erro:", error.message);
    }
  };

  return (
    <div className={styles.request_changes_container}>
      <div className={styles.request_changes_items}>
        {request_changes?.map((request_change) => (
          <div key={request_change.id} className={styles.request_change_item}>
            <div>ID: {request_change.id}</div>
            <div>AnimeID: {request_change.animeId}</div>
            <div>Ativo?: {request_change.active ? "ATIVO" : "INATIVO"}</div>
            <div>Aceito?: {request_change.accepted}</div>
            <div>Motivo: {request_change.reason}</div>
            <div>Inormações adicionais: {request_change.additionalInfo}</div>
            <div>Dados para alterar: {request_change.changeData}</div>
            <div>
              Data de criação:{" "}
              {new Date(request_change.createdAt).toLocaleDateString()}
            </div>
            <div>
              <button
                onClick={() =>
                  handleUpdateRequestChange(request_change.id, true)
                }
              >
                Accept request
              </button>
              <button
                onClick={() =>
                  handleUpdateRequestChange(request_change.id, false)
                }
              >
                Reject request
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className={styles.pagination_bar}>
        <button onClick={() => loadPage(currentPage - 1)}>&larr;</button>

        <button onClick={() => loadPage(currentPage + 1)}>&rarr;</button>
      </div>
    </div>
  );
}

export default RequestChanges;

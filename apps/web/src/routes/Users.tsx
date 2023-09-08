import { useEffect, useState } from "react";
import AppConfig from "../config/AppConfig";
import { UserProps } from "../types/user";
import styles from "./Users.module.css";

const config = AppConfig

function Users(){
    const [users, setUsers] = useState<UserProps[] | null>([]);
    const [currentPage, setCurrentPage] = useState<number>(1);
    const currentPerPage = 15;

    const loadUsers = async (search: string, page: number, per_page: number) => {
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
              "query": `query users($search: String, $page: Int, $perpage: Int){
                User{
                  users(search: $search, page: $page, perPage: $perpage){
                    totalCount
                    page
                    perPage
                    pages
                    items{
                      id
                      createdAt
                      username
                      email
                      active
                      roleId
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
          const user_items = response_json["data"]["User"]["users"]["items"];
          
          setUsers(user_items)
      
        } catch (error: Error | any) {
          console.error("Ocorreu um erro:", error.message);
        }
      }

      useEffect(() => {
        loadUsers("", currentPage, currentPerPage);
    }, [currentPage]);

    const loadPage = (page: number) => {
        setCurrentPage(page);
        loadUsers("", page, currentPerPage);
    };
    
    
      return (
        <div className={styles.users_container}>
            <div className={styles.user_items}>
                {users?.map((user) => (
                    <div key={user.id} className={styles.user_item}>
                        <div>ID: {user.id}</div>
                        <div>Situação: {user.active ? "ATIVO" : "INATIVO"}</div>
                        <div>Email: {user.email}</div>
                        <div>Username: {user.username}</div>
                        <div>Data de criação: {new Date(user.createdAt).toLocaleDateString()}</div>
                    </div>
                ))}
            </div>

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

export default Users;
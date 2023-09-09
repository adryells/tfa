import { useEffect, useState } from "react";
import AppConfig from "../config/AppConfig";
import { UserProps } from "../types/user";
import styles from "./Users.module.css";

const config = AppConfig;

function Users() {
  const [users, setUsers] = useState<UserProps[] | null>([]);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [selectedUser, setSelectedUser] = useState<UserProps | null>(null);
  const [username, setUsername] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [roleId, setRoleId] = useState<number | null>(null);
  const [active, setActive] = useState<boolean | null>(null);
  const [currentPassword, setCurrentPassword] = useState<string>("");
  const [newPassword, setNewPassword] = useState<string>("");

  const currentPerPage = 15;

  const loadUsers = async (search: string, page: number, per_page: number) => {
    try {
      const res = await fetch(`${config.API_URL}/graphql`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          variables: {
            search: search,
            page: page,
            perpage: per_page,
          },
          query: `query users($search: String, $page: Int, $perpage: Int){
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
          }`,
        }),
      });

      if (!res.ok) {
        throw new Error("Erro na chamada da API");
      }

      const response_json = await res.json();
      const user_items = response_json["data"]["User"]["users"]["items"];

      setUsers(user_items);
    } catch (error: Error | any) {
      console.error("Ocorreu um erro:", error.message);
    }
  };

  useEffect(() => {
    loadUsers("", currentPage, currentPerPage);
  }, [currentPage]);

  const loadPage = (page: number) => {
    setCurrentPage(page);
    loadUsers("", page, currentPerPage);
  };

  const openModal = (user: UserProps) => {
    setSelectedUser(user);
    setIsModalOpen(true);
    setUsername(user.username);
    setEmail(user.email);
    setRoleId(user.roleId);
    setActive(user.active);
  };

  const closeModal = () => {
    setSelectedUser(null);
    setIsModalOpen(false);
    setUsername("");
    setEmail("");
    setRoleId(null);
    setActive(null);
    setCurrentPassword("");
    setNewPassword("");
  };

  const handleUpdateUser = async () => {
    try {
      const res = await fetch(`${config.API_URL}/graphql`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          variables: {
            userid: selectedUser?.id,
            username: username,
            email: email,
            inputPassword: {
              currentPassword: currentPassword,
              newPassword: newPassword,
            },
            roleid: roleId,
            active: active,
          },
          query: `mutation updateuser (
            $userid: Int!,
            $username: String,
            $email: String,
            $inputPassword: InputPassword,
            $roleid: Int,
            $active: Boolean
          ) {
            UpdateUser(inputUpdateUserData:{
              userId: $userid
              username: $username,
              email: $email,
              inputPassword: $inputPassword,
              roleId: $roleid,
              active: $active
            }) {
              user {
                id
              }
            }
          }`,
        }),
      });

      if (!res.ok) {
        throw new Error("Erro na chamada da API");
      }

      closeModal();
    } catch (error: Error | any) {
      console.error("Ocorreu um erro:", error.message);
    }
  };

  return (
    <div className={styles.users_container}>
      <div className={styles.user_items}>
        {users?.map((user) => (
          <div
            key={user.id}
            className={styles.user_item}
            onClick={() => openModal(user)}
          >
            <div>ID: {user.id}</div>
            <div>Situation: {user.active ? "ACTIVE" : "INACTIVE"}</div>
            <div>E-mail: {user.email}</div>
            <div>Username: {user.username}</div>
            <div>
              Created at: {new Date(user.createdAt).toLocaleDateString()}
            </div>
          </div>
        ))}
      </div>

      <div className={styles.pagination_bar}>
        <button onClick={() => loadPage(currentPage - 1)}>&larr;</button>
        <button onClick={() => loadPage(currentPage + 1)}>&rarr;</button>
      </div>

      {isModalOpen && selectedUser && (
        <div className={styles.modal}>
          <div className={styles.modal_content}>
            <div>ID: {selectedUser.id}</div>

            <div>
              <label htmlFor="username">Username:</label>
              <input
                type="text"
                id="username"
                name="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>

            <div>
              <label htmlFor="email">Email:</label>
              <input
                type="text"
                id="email"
                name="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div>
              <label htmlFor="roleId">Role:</label>
              <select
                id="roleId"
                name="roleId"
                value={roleId || ""}
                onChange={(e) => setRoleId(parseInt(e.target.value))}
              >
                <option value={1}>Admin</option>
                <option value={2}>Common</option>
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
              <label htmlFor="currentPassword">Current Password:</label>
              <input
                type="password"
                id="currentPassword"
                name="currentPassword"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
              />
            </div>

            <div>
              <label htmlFor="newPassword">New Password:</label>
              <input
                type="password"
                id="newPassword"
                name="newPassword"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
            </div>

            <button onClick={handleUpdateUser}>Confirm Changes</button>
            <button onClick={closeModal}>Fechar</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Users;

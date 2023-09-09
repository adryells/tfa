import { ChangeEvent, useState } from "react";
import AppConfig from "../config/AppConfig";
import styles from "./Login.module.css";
import { useNavigate } from "react-router-dom";

const config = AppConfig;

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const connect = async (email: string, password: string) => {
    try {
      const res = await fetch(`${config.API_URL}/graphql`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          variables: {
            email: email,
            password: password,
          },
          query: `
                mutation login ($email: String!, $password: String!){
                    Login(inputLoginData: {email: $email, password: $password}){
                    authToken{
                        token
                        user{
                        id
                        username
                        email
                        active
                        roleId
                        }
                    }
                    }
                }
              `,
        }),
      });

      if (!res.ok) {
        throw new Error("Erro na chamada da API");
      }

      const response_json = await res.json();

      if (response_json.errors) {
        const error_msg = response_json.errors[0].message;
        alert(error_msg);
      } else {
        navigate("/admin", { state: { permited: true } });
      }
    } catch (error: Error | any) {
      console.error("Ocorreu um erro:", error.message);
    }
  };

  const updateEmail = (e: ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const updatePassword = (e: ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  return (
    <div id={styles.login}>
      <h3>Login</h3>
      <img src="/img/nojogirl.png" />
      <input
        type="email"
        name="email"
        placeholder="digite seu e-mail..."
        onChange={updateEmail}
      />
      <input
        type="password"
        name="password"
        placeholder="digite sua senha..."
        onChange={updatePassword}
      />
      <button
        type="submit"
        onClick={() => {
          connect(email, password);
        }}
      >
        Logar
      </button>
    </div>
  );
}

export default Login;

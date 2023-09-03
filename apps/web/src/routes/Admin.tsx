import { useLocation, useNavigate } from "react-router-dom";
import AppConfig from "../config/AppConfig";
import styles from "./Login.module.css";

const config = AppConfig;

function Admin() {
  const location = useLocation();
  const permited = location.state?.permited || false;

  if (!permited) {
    return null
  }

  console.log(config);

  return (
    <div id={styles.admin}>
      Pois é
    </div>
  );
}

export default Admin;

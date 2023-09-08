import { Link } from "react-router-dom";
import styles from "./SidebarAdmin.module.css";

function SidebarAdmin(){
    return (
        <div className={styles.sidebar}>
            <ul> 
                <li className={location.pathname === '/admin/users' ? styles.active_tab : ''}>
                    <Link to="/admin/users">Users</Link>
                </li>

                <li className={location.pathname === '/admin/requestchanges' ? styles.active_tab : ''}>
                    <Link to="/admin/requestchanges">Request Changes</Link>
                </li>
                
                <li className={location.pathname === '/admin/emails' ? styles.active_tab : ''}>
                    <Link to="/admin/emails">Emails</Link>
                </li>
            </ul>
        </div>
    );
}

export default SidebarAdmin;

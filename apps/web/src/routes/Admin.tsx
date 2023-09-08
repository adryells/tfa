import { useLocation } from "react-router-dom";
import styles from "./Admin.module.css";
import { useState } from "react";
import Users from "./Users";
import RequestChanges from "./RequestChange";

interface Page {
  name: string;
  component: JSX.Element;
}

function Admin() {
  const [currentPageElement, setCurrentPageElement] = useState<JSX.Element>(<Users />);
  const [currentPageElementName, setCurrentPageElementName] = useState("users");

  const location = useLocation();
  const permited = location.state?.permited || false;

  if (!permited) {
    return null;
  }

  const PAGES: { [key: string]: Page } = {
    users: {
      name: "Users",
      component: <Users />,
    },
    requestchanges: {
      name: "Request Changes",
      component: <RequestChanges />,
    }
  };

  const updateCurrentPage = (pageName: string) => {
    console.log(pageName)
    const page = PAGES[pageName];
    if (page) {
      setCurrentPageElementName(pageName);
      setCurrentPageElement(page.component);
    }
  };

  return (
    <div className={styles.admin}>
      <div className={styles.sidebar}>
        <ul>
          {Object.keys(PAGES).map((pageName) => (
            <li
              key={pageName}
              className={currentPageElementName === pageName ? styles.active_tab : ""}
              onClick={() => updateCurrentPage(pageName)}
            >
              {PAGES[pageName].name}
            </li>
          ))}
        </ul>
      </div>
      {currentPageElement}
    </div>
  );
}

export default Admin;

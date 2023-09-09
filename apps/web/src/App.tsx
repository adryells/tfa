import { Outlet } from "react-router-dom";
import classes from "./App.module.css";
import BackgroundMusic from "./components/BackgroundMusic";

function App() {
  return (
    <div className={classes.app}>
      <a href="/">
        <h1>TFA - Time to finish an anime</h1>
      </a>
      <BackgroundMusic />
      <Outlet />
    </div>
  );
}

export default App;

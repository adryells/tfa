import { Outlet } from "react-router-dom";
import classes from "./App.module.css";
import BackgroundMusic from "./components/BackgroundMusic";
import Contact from "./components/Contact";

function App() {
  console.log(import.meta.env);
  return (
    <div className={classes.app}>
      <a href="/">
        <h1>TFA - Time to finish an anime</h1>
      </a>
      <BackgroundMusic />
      <Outlet />
      <Contact />
    </div>
  );
}

export default App;

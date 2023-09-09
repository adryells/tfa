import classes from "./Input.module.css";

type InputProps = {
  updateDedicatedHours: (e: React.ChangeEvent<HTMLInputElement>) => void;
};

const Input = ({ updateDedicatedHours }: InputProps) => {
  return (
    <div className={classes.input}>
      <h2>Horas disponiveis: </h2>
      <div className={classes.input_container}>
        <input
          type="number"
          placeholder="digite as horas disponiveis"
          onChange={updateDedicatedHours}
          min={1}
          max={24}
        />
      </div>
    </div>
  );
};

export default Input;

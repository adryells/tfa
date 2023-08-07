import {BsSearch} from 'react-icons/bs';
import { useState } from 'react';
import classes from './search.module.css';

type SearchProps = {
    loadAnime: (search: string) => Promise<void>; 
}

const Search = ({loadAnime}: SearchProps) => {

    const [search, setSearch] = useState("");

    const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === "Enter" && search){
            loadAnime(search)
        }
    }

    return (
        <div className={classes.search}>
            <h2>Busque por um anime: </h2>
            <div className={classes.search_container}>
                <input 
                    type="text"
                    placeholder="Digite o nome do anime" 
                    onChange={e => setSearch(e.target.value)}
                    onKeyDown={handleKeyDown}
                />
                <button  onClick={() => {loadAnime(search)}}>
                    <BsSearch />
                </button>
            </div>
        </div>
    )
}

export default Search;

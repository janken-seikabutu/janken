import { Route, Routes } from "react-router-dom"
import Game from "./Game"
import Home from "./Home"
import LoginRegister from "./LoginRegister"
import Markov from "./Markov"

function App() {
  const item = localStorage.getItem("user_name")
  const gameCount = localStorage.getItem("game_count")
  const remainingCount = 50 - gameCount
  console.log("item", item);
  return (
    <>
      <Routes>
        {item === null ? (
          <>
            <Route path="/" element={<LoginRegister />} />
          </>
        )
        :
        (
          <>
            <Route path="/" element={<Home />} />
            <Route path="/game/1" element={<Game game_id={1}/>} />
            {remainingCount > 0 ?
            <>
            </>
            :
            <>
              <Route path="/game/2" element={<Markov />} />
            </>
            }
          </>
        )}
      </Routes>
    </>
  )
}

export default App

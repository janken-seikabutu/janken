import { Route, Routes } from "react-router-dom"
import Game from "./components/Game"

function App() {

  return (
    <>
      <Routes>
        <Route path="/game/1" element={<Game game_id={1}/>} />
        <Route path="/game/2" element={<Game game_id={2}/>} />
      </Routes>
    </>
  )
}

export default App

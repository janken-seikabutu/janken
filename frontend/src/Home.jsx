import { Link } from "react-router-dom";

const Home = () => {
  const gameCount = localStorage.getItem("game_count")
  const remainingCount = 50 - gameCount
  return (
    <>
      <div>相手を選択</div>
      <Link to="/game/1">ランダム</Link>
      {remainingCount > 0 ?
      <>
        <div>
          もう一つの相手は後{remainingCount}回ランダムのじゃんけんを遊んだら選択できます
        </div>
      </>
      :
      <>
        <Link to="/game/2">マルコフ</Link>
      </>
      }
    </>
  )
}

export default Home
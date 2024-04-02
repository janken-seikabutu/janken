import { useState } from "react"
import { Link } from "react-router-dom"

const Game = () => {
  const [userHandPath, setUserHandPath] =  useState("")
  const [aiHand, setAiHand] =  useState("")
  const [imagePath, setImagePath] = useState("")
  const hands = ["g","c","p"]
  const userName = localStorage.getItem("user_name")
  const previousId = localStorage.getItem("previous_id")
  const markovId = localStorage.getItem("markov_id")
  const jankenGame = async(hand) => {
    const aiRandomChoise = hands[Math.floor(Math.random() * hands.length)]
    setAiHand(aiRandomChoise)
    setImagePath("/images/" + aiRandomChoise + ".JPG")
    setUserHandPath("/images/" + hand + ".JPG")
    let gameResult = ""
    if (hand == aiHand){
      gameResult = "d"
    } 
    else if (hand == "g"){
      if (aiHand == "c"){
        gameResult = "w"
      }
      else {
        gameResult = "l"
      }
    }
    else if (hand == "c"){
      if (aiHand == "p"){
        gameResult = "w"
      }
      else {
        gameResult = "l"
      }
    }
    else {
      if (aiHand == "g") {
        gameResult = "w"
      }
      else {
        gameResult = "l"
      }
    }
    console.log(userName,hand,gameResult,previousId,markovId)
    const res = await fetch("https://gcp-dfj76wznba-an.a.run.app/game/1",{
      method: "POST",
      headers: {
				"Content-Type": "application/json",
			},
      body: JSON.stringify({
				name: userName,
        hand: hand,
        result: gameResult,
        previous_id: previousId,
        markov_id: markovId,
			}),
    });
    if (res.ok) {
      const data = await res.json()
      console.log(data)
      localStorage.setItem("markov_id", data["markov_id"]);
      localStorage.setItem("game_count", data["game_count"]);
      localStorage.setItem("previous_id", data["previous_id"]);
    }
  }
  return (
    <>
      <div>相手の手</div>
      {aiHand !== "" ?
      <>
        <img src={imagePath} className="w-64"></img>
      </>
      :
      <></>
      }
      <div>自分の手</div>
      {userHandPath !== "" ?
      <>
        <img src={userHandPath} className="w-64"></img>
      </>
      :
      <></>
      }
      <div>
        <button onClick={() => jankenGame("g")}>グー</button>
        <button onClick={() => jankenGame("c")}>チョキ</button>
        <button onClick={() => jankenGame("p")}>パー</button>
      </div>

      <Link to="/">ホームに戻る</Link>
    </>
  )
}

export default Game
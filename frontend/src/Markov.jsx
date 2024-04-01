import { useState } from "react"

const Markov = () => {
  const [userHandPath, setUserHandPath] =  useState("")
  const [imagePath, setImagePath] = useState("")
  const userName = localStorage.getItem("user_name")
  const previousId = localStorage.getItem("previous_id")
  const markovId = localStorage.getItem("markov_id")
  const jankenGame = async(hand) => {
    const res = await fetch("http://localhost:8081/game/2",{
      method: "POST",
      headers: {
				"Content-Type": "application/json",
			},
      body: JSON.stringify({
				name: userName,
        hand: hand,
        previous_id: previousId,
        markov_id: markovId,
			}),
    });
    if (res.ok) {
      const data = await res.json()
      console.log(data)
      localStorage.setItem("game_count", data["game_count"]);
      localStorage.setItem("previous_id", data["previous_id"]);
      setImagePath("../../public/" + data["hand_ai"] + ".jpg")
      setUserHandPath("../../public/" + hand + ".jpg")
    }
  }
  return (
    <>
      <div>相手の手</div>
      {imagePath !== "" ?
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
     
    </>
  )
}

export default Markov
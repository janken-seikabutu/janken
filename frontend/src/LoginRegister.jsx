import { useState } from "react";

const LoginRegister = () => {
  const [userName, setUserName] = useState("");
	const [password, setPassword] = useState("");
  const login = async () => {
    const res = await fetch("http://localhost:8081/user/login",{
      method: "POST",
      headers: {
				"Content-Type": "application/json",
			},
      body: JSON.stringify({
				name: userName,
				password: password,
			}),
    });
    if (res.ok) {
      const data = await res.json()
      console.log(data)
      localStorage.setItem("user_name", data["name"]);
      localStorage.setItem("markov_id", data["markov_id"]);
      localStorage.setItem("game_count", data["game_count"]);
      localStorage.setItem("previous_id", data["previous_id"]);
      document.location = "/";
    }
  }
 
  const register = async() => {
    const res = await fetch("http://localhost:8081/user/register",{
      method: "POST",
      headers: {
				"Content-Type": "application/json",
			},
      body: JSON.stringify({
				name: userName,
				password: password,
			}),
    });
    if (res.ok) {
      const data = await res.json()
      console.log(data)
      localStorage.setItem("user_name", data["name"]);
      localStorage.setItem("markov_id", data["markov_id"]);
      localStorage.setItem("game_count", data["game_count"]);
      localStorage.setItem("previous_id", data["previous_id"]);
      document.location = "/";
    }
  }

  return (
    <>
      <section class="">
          <div class=" items-center px-5 py-12 lg:px-20">
              <div class="flex flex-col w-full max-w-md p-10 mx-auto my-6 transition duration-500 ease-in-out transform bg-white rounded-lg md:mt-0">
                  <div class="mt-8">
                      <div class="mt-6">
                          <div class="space-y-6">
                              <div>
                                  <label for="userName" class="block text-sm font-medium text-neutral-600"> ユーザー名 </label>
                                  <div class="mt-1">
                                  </div>
                              </div>
                              <input id="userName" type="text" value={userName} onChange={(e) => setUserName(e.target.value)} className="block w-full px-5 py-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-50 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-300"/>
                              <div class="space-y-1">
                                  <label for="password" class="block text-sm font-medium text-neutral-600"> パスワード </label>
                                  <div class="mt-1">
                                  <input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="block w-full px-5 py-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-50 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-300"/>
                                  </div>
                              </div>
                              <div>
                                  <button type="submit" onClick={login} class="flex items-center justify-center w-full px-10 py-4 text-base font-medium text-center text-white transition duration-500 ease-in-out transform bg-blue-600 rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">ログイン</button>
                              </div>
                          </div>
                          <div class="relative my-10">
                              <button type="submit" onClick={register} class="flex items-center justify-center w-full px-10 py-4 text-base font-medium text-center text-white transition duration-500 ease-in-out transform bg-blue-600 rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">ユーザー登録</button>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
      </section>
    </>
  )
}

export default LoginRegister

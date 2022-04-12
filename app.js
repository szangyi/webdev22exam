console.log("hellokaa")



function sendTweet() {
    const form = event.target
        // Get the button, set the data-await, and disable it
    const button = _one("button[type='submit']", form)
    console.log(button)
    button.innerText = button.dataset.await
    button.disabled = true
}



// async function tweet() {
//     const form = event.target.form
//     const connection = await fetch("/tweet_add", {
//         method: "POST",
//         body: new FormData(form)
//     })
//     console.log(connection)
//     if (!connection.ok) {
//         alert("Could not tweeeeeet")
//         return
//     }

//     let tweet = await connection.json()
//     let section_tweet = `
//     <form onsubmit="return false" style="border:1px solid pink;">
//         <div id="tweet_id">${tweet.tweet_id}</div>
//         <div id="tweet_text">${tweet.tweet_text}</div>
//         <button id="button_like" onclick="like_tweet()">Like</button>
//         <button id="button_dislike" onclick="dislike_tweet()" style="display:none">Disike</button>
//         <button onclick="delete_tweet()">Delete</button>
//     </form>
//     `


//     document.querySelector("#tweets").insertAdjacentHTML("afterbegin", section_tweet)
//     console.log(tweet_id)
//}
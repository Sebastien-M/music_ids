let play_pause_button = document.querySelector(".play-pause-button");
let button_icon = document.querySelector(".audio-button-icon")

play_pause_button.addEventListener("click", ()=>{
    console.log(button_icon.innerHTML)
    if (button_icon.innerHTML === "pause_circle_filled") {
        button_icon.innerHTML = "play_circle_filled";
    } else {
        button_icon.innerHTML = "pause_circle_filled";
    }
})
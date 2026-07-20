// ===============================
// Theme Toggle
// ===============================

const themeBtn = document.querySelector(".theme-btn");

themeBtn.addEventListener("click", () => {

    document.body.classList.toggle("light");

    if(document.body.classList.contains("light")){

        themeBtn.innerHTML='<i class="fa-solid fa-sun"></i>';

    }else{

        themeBtn.innerHTML='<i class="fa-solid fa-moon"></i>';

    }

});


// ===============================
// Buttons
// ===============================

const startBtn=document.getElementById("start");
const stopBtn=document.getElementById("stop");
const speakBtn=document.getElementById("speak");
const clearBtn=document.getElementById("clear");

const gesture=document.querySelector(".gesture-box h1");
const translation=document.querySelector(".translation");


// Start Camera (Placeholder)

startBtn.onclick=()=>{

    alert("Camera will start in Phase 2.");

};


// Stop Camera

stopBtn.onclick=()=>{

    alert("Camera stopped.");

};


// Speak Translation

speakBtn.onclick=()=>{

    const speech=new SpeechSynthesisUtterance(
        translation.innerText
    );

    speech.rate=1;

    speech.pitch=1;

    window.speechSynthesis.speak(speech);

};


// Clear Output

clearBtn.onclick=()=>{

    gesture.innerText="----";

    translation.innerText="Waiting for gesture...";

};
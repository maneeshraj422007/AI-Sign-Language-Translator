const video = document.getElementById("video");

async function startCamera(){

    try{

        const stream = await navigator.mediaDevices.getUserMedia({

            video:true,
            audio:false

        });

        video.srcObject = stream;

    }

    catch(error){

        alert("Unable to access camera.");

        console.error(error);

    }

}
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

    startCamera();

};


// Stop Camera

stopBtn.onclick=()=>{

    const stream = video.srcObject;

    if(stream){

        stream.getTracks().forEach(track=>track.stop());

        video.srcObject = null;

    }

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
var video=document.getElementById('video');
var play_pause=document.getElementById('play-pause');
var video_player=document.getElementById('video-player');
var p=video_player.querySelector('p');
play_pause.src='images/play-circle-solid.png';
play_pause.style.top='40%';
play_pause.style.left='45%';

video.style.opacity=0.5;


play_pause.addEventListener('click',function(){
    if(video.paused==true){
        video.play();
// Update the button text to 'Pause'
 play_pause.src='images/pause-circle-solid.png';
 video.style.opacity=1;
 p.style.display='none';
 play_pause.style.opacity=0.1;
} else {
// Pause the video
video.pause();

// Update the button text to 'Play'
play_pause.src='images/play-circle-solid.png';
video.style.opacity=0.5;

p.style.display='block';

play_pause.style.opacity=1  ;

}
});



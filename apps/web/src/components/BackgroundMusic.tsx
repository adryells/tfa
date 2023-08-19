import { useEffect } from 'react';

const BackgroundMusic = () => {
  useEffect(() => {
    const volume = 0.2;

    const audio = new Audio('/audios/lofi1.mp3');
    audio.volume = volume;
    audio.play();

    const restartAudio = () => {
      audio.currentTime = 0; 
      audio.play();
    };

    audio.addEventListener('ended', restartAudio);

    return () => {
      audio.removeEventListener('ended', restartAudio);
      audio.pause();
    };
  }, []);

  return null;
};

export default BackgroundMusic;

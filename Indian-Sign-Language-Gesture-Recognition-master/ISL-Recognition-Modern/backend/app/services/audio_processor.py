"""
Audio processing service for speech recognition and text-to-speech.
Cross-platform implementation using pyttsx3 and SpeechRecognition.
"""
import speech_recognition as sr
import pyttsx3
import os
import logging
from typing import Optional, Tuple
from pathlib import Path
import threading

logger = logging.getLogger(__name__)


class AudioProcessor:
    """
    Cross-platform audio processing for ISL translation.
    Handles speech recognition and text-to-speech synthesis.
    """
    
    def __init__(self):
        """Initialize audio processor."""
        self.recognizer = sr.Recognizer()
        self.tts_engine = None
        self._init_tts()
    
    def _init_tts(self):
        """Initialize text-to-speech engine in a thread-safe manner."""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            self.tts_engine.setProperty('rate', 150)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Use first available voice
                self.tts_engine.setProperty('voice', voices[0].id)
            
            logger.info("TTS engine initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing TTS engine: {e}")
            self.tts_engine = None
    
    def transcribe_audio(
        self,
        audio_file_path: str,
        language: str = "en-IN"
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Transcribe audio file to text using Google Speech Recognition.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code (default: en-IN for Indian English)
            
        Returns:
            Tuple of (success, transcribed_text, error_message)
        """
        try:
            # Load audio file
            with sr.AudioFile(audio_file_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Record audio
                audio_data = self.recognizer.record(source)
            
            # Perform speech recognition
            try:
                text = self.recognizer.recognize_google(audio_data, language=language)
                logger.info(f"Transcribed text: {text}")
                return True, text, None
            except sr.UnknownValueError:
                error_msg = "Could not understand audio"
                logger.warning(error_msg)
                return False, None, error_msg
            except sr.RequestError as e:
                error_msg = f"Could not request results from speech recognition service: {e}"
                logger.error(error_msg)
                return False, None, error_msg
                
        except Exception as e:
            error_msg = f"Error processing audio file: {e}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def transcribe_microphone(
        self,
        duration: int = 5,
        language: str = "en-IN"
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Transcribe audio from microphone.
        
        Args:
            duration: Recording duration in seconds
            language: Language code
            
        Returns:
            Tuple of (success, transcribed_text, error_message)
        """
        try:
            with sr.Microphone() as source:
                logger.info("Listening...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for audio
                audio_data = self.recognizer.listen(source, timeout=duration)
            
            # Perform speech recognition
            try:
                text = self.recognizer.recognize_google(audio_data, language=language)
                logger.info(f"Transcribed text: {text}")
                return True, text, None
            except sr.UnknownValueError:
                error_msg = "Could not understand audio"
                logger.warning(error_msg)
                return False, None, error_msg
            except sr.RequestError as e:
                error_msg = f"Could not request results: {e}"
                logger.error(error_msg)
                return False, None, error_msg
                
        except Exception as e:
            error_msg = f"Error accessing microphone: {e}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def text_to_speech(
        self,
        text: str,
        save_to_file: Optional[str] = None
    ) -> bool:
        """
        Convert text to speech.
        
        Args:
            text: Text to convert to speech
            save_to_file: Optional path to save audio file
            
        Returns:
            Success status
        """
        if not self.tts_engine:
            logger.error("TTS engine not initialized")
            return False
        
        try:
            if save_to_file:
                # Save to file
                self.tts_engine.save_to_file(text, save_to_file)
                self.tts_engine.runAndWait()
                logger.info(f"Audio saved to {save_to_file}")
            else:
                # Play directly
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            
            return True
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            return False
    
    def get_supported_languages(self) -> list:
        """
        Get list of supported languages for speech recognition.
        
        Returns:
            List of language codes
        """
        # Common languages supported by Google Speech Recognition
        return [
            "en-US",  # English (US)
            "en-IN",  # English (India)
            "hi-IN",  # Hindi
            "en-GB",  # English (UK)
        ]
    
    def get_available_voices(self) -> list:
        """
        Get available TTS voices.
        
        Returns:
            List of voice information dictionaries
        """
        if not self.tts_engine:
            return []
        
        try:
            voices = self.tts_engine.getProperty('voices')
            voice_info = []
            
            for voice in voices:
                voice_info.append({
                    'id': voice.id,
                    'name': voice.name,
                    'languages': voice.languages,
                    'gender': getattr(voice, 'gender', 'unknown')
                })
            
            return voice_info
        except Exception as e:
            logger.error(f"Error getting voices: {e}")
            return []
    
    def set_voice(self, voice_id: str) -> bool:
        """
        Set TTS voice.
        
        Args:
            voice_id: Voice ID to use
            
        Returns:
            Success status
        """
        if not self.tts_engine:
            return False
        
        try:
            self.tts_engine.setProperty('voice', voice_id)
            return True
        except Exception as e:
            logger.error(f"Error setting voice: {e}")
            return False
    
    def cleanup(self):
        """Cleanup resources."""
        if self.tts_engine:
            try:
                self.tts_engine.stop()
            except:
                pass


# Singleton instance
_audio_processor = None
_lock = threading.Lock()


def get_audio_processor() -> AudioProcessor:
    """
    Get singleton audio processor instance.
    Thread-safe initialization.
    """
    global _audio_processor
    
    if _audio_processor is None:
        with _lock:
            if _audio_processor is None:
                _audio_processor = AudioProcessor()
    
    return _audio_processor

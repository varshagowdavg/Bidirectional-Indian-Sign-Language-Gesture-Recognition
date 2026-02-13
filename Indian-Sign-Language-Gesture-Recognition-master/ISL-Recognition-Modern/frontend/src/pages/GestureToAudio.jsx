import React, { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import { Camera, RefreshCw, Volume2, Image as ImageIcon, Upload } from 'lucide-react';

const GestureToAudio = () => {
    const [isCapturing, setIsCapturing] = useState(false);
    const [capturedImage, setCapturedImage] = useState(null);
    const [recognizedText, setRecognizedText] = useState('');
    const [confidence, setConfidence] = useState(0);
    const [isLoading, setIsLoading] = useState(false);
    const [imageError, setImageError] = useState(false);

    const webcamRef = useRef(null);
    const fileInputRef = useRef(null);

    const speakText = (text) => {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            window.speechSynthesis.speak(utterance);
        }
    };

    const analyzeImage = async (imageSrc) => {
        setIsLoading(true);
        setRecognizedText('');
        setImageError(false); // Reset image error state

        try {
            const response = await axios.post('/api/gesture/recognize', {
                image_data: imageSrc
            });

            const { recognized_character, confidence } = response.data;

            setRecognizedText(recognized_character);
            setConfidence(confidence);
            speakText(recognized_character);

        } catch (error) {
            console.error('Recognition error:', error);

            // Show specific error message
            if (error.response?.status === 400) {
                setRecognizedText('No hand detected');
                setConfidence(0);
            } else if (error.response?.data?.detail) {
                setRecognizedText(`Error: ${error.response.data.detail}`);
                setConfidence(0);
            } else {
                setRecognizedText('Error processing image');
                setConfidence(0);
            }
        } finally {
            setIsLoading(false);
        }
    };

    const captureAndAnalyze = useCallback(async () => {
        if (webcamRef.current) {
            const imageSrc = webcamRef.current.getScreenshot();
            if (imageSrc) {
                setCapturedImage(imageSrc);
                await analyzeImage(imageSrc);
            }
        }
    }, []);

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                const imageSrc = reader.result;
                setCapturedImage(imageSrc);
                setIsCapturing(false); // Ensure camera is off
                analyzeImage(imageSrc);
            };
            reader.readAsDataURL(file);
        }
    };

    const triggerFileUpload = () => {
        fileInputRef.current.click();
    };

    const resetCapture = () => {
        setCapturedImage(null);
        setRecognizedText('');
        setConfidence(0);
        setImageError(false);
    };

    const startCamera = () => {
        setIsCapturing(true);
        setCapturedImage(null);
    };

    const stopCamera = () => {
        setIsCapturing(false);
        setCapturedImage(null);
    };

    return (
        <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12 fade-in">
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                    Gesture to Audio
                </h1>
                <p className="text-xl text-gray-600">
                    Show a hand gesture, capture it, and let AI translate it to speech.
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Camera/Capture Section */}
                <div className="bg-white rounded-2xl shadow-xl p-6 slide-up" style={{ animationDelay: '0.1s' }}>
                    <div className="aspect-video bg-gray-900 rounded-lg overflow-hidden relative mb-6">
                        {!isCapturing && !capturedImage ? (
                            <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-500">
                                <Camera size={64} className="mb-4 opacity-50" />
                                <p>Camera is off</p>
                            </div>
                        ) : capturedImage ? (
                            <img src={capturedImage} alt="Captured" className="w-full h-full object-cover" />
                        ) : (
                            <Webcam
                                audio={false}
                                ref={webcamRef}
                                screenshotFormat="image/jpeg"
                                className="w-full h-full object-cover"
                                videoConstraints={{
                                    width: 1280,
                                    height: 720,
                                    facingMode: "user"
                                }}
                            />
                        )}

                        {/* Show uploaded image if not capturing but image exists */}
                        {!isCapturing && capturedImage && (
                            <img src={capturedImage} alt="Uploaded" className="absolute inset-0 w-full h-full object-cover" />
                        )}
                    </div>

                    <div className="flex justify-center gap-4">
                        {!isCapturing && !capturedImage ? (
                            <>
                                <button
                                    onClick={startCamera}
                                    className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors font-medium"
                                >
                                    <Camera size={20} />
                                    Start Camera
                                </button>
                                <button
                                    onClick={triggerFileUpload}
                                    className="flex items-center gap-2 px-6 py-3 bg-gray-800 text-white rounded-full hover:bg-gray-900 transition-colors font-medium"
                                >
                                    <Upload size={20} />
                                    Upload Image
                                </button>
                                <input
                                    type="file"
                                    ref={fileInputRef}
                                    onChange={handleFileUpload}
                                    className="hidden"
                                    accept="image/*"
                                />
                            </>
                        ) : isCapturing && !capturedImage ? (
                            <>
                                <button
                                    onClick={stopCamera}
                                    className="px-6 py-3 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300 transition-colors font-medium"
                                >
                                    Stop
                                </button>
                                <button
                                    onClick={captureAndAnalyze}
                                    disabled={isLoading}
                                    className="flex items-center gap-2 px-8 py-3 bg-red-600 text-white rounded-full hover:bg-red-700 transition-colors font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                                >
                                    {isLoading ? (
                                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                                    ) : (
                                        <div className="w-4 h-4 bg-white rounded-sm" />
                                    )}
                                    Capture Sign
                                </button>
                            </>
                        ) : (
                            <button
                                onClick={resetCapture}
                                className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors font-medium"
                            >
                                <RefreshCw size={20} />
                                Retake
                            </button>
                        )}
                    </div>
                </div>

                {/* Results Section */}
                <div className="bg-white rounded-2xl shadow-xl p-6 slide-up" style={{ animationDelay: '0.2s' }}>
                    <div className="flex items-center gap-3 mb-6">
                        <Volume2 className="text-blue-600" size={24} />
                        <h2 className="text-2xl font-bold text-gray-900">Recognition Result</h2>
                    </div>

                    <div className="h-[400px] flex flex-col items-center justify-center border-2 border-dashed border-gray-200 rounded-xl bg-gray-50 p-8">
                        {recognizedText ? (
                            <div className="text-center w-full">
                                <div className="mb-8">
                                    <p className="text-sm text-gray-500 mb-2 uppercase tracking-wide">Recognized Character</p>
                                    <div className="text-9xl font-bold text-blue-600 mb-4 animate-bounce-short">
                                        {recognizedText}
                                    </div>
                                    <div className="inline-flex items-center px-3 py-1 rounded-full bg-green-100 text-green-800 text-sm font-medium">
                                        {Math.round(confidence)}% Confidence
                                    </div>
                                </div>

                                {/* Reference Image Display */}
                                <div className="flex flex-col items-center">
                                    <p className="text-sm text-gray-500 mb-3 flex items-center gap-2">
                                        <ImageIcon size={16} />
                                        Reference Sign Image
                                    </p>
                                    {!imageError ? (
                                        <div className="w-32 h-32 bg-white rounded-lg shadow-md p-2 border border-gray-100">
                                            <img
                                                src={`http://localhost:8000/static/alphabets/${recognizedText.toLowerCase()}.png`}
                                                alt={`Sign for ${recognizedText}`}
                                                className="w-full h-full object-contain"
                                                onError={() => setImageError(true)}
                                            />
                                        </div>
                                    ) : (
                                        <div className="w-32 h-32 bg-gray-100 rounded-lg shadow-md p-2 border border-gray-200 flex items-center justify-center">
                                            <p className="text-xs text-gray-400 text-center">Image not available</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ) : (
                            <div className="text-center text-gray-400">
                                {isLoading ? (
                                    <div className="flex flex-col items-center">
                                        <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-4" />
                                        <p>Analyzing gesture...</p>
                                    </div>
                                ) : (
                                    <>
                                        <p className="mb-2">No gesture captured yet</p>
                                        <p className="text-sm">Capture a sign or upload an image to analyze</p>
                                    </>
                                )}
                            </div>
                        )}
                    </div>

                    <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                        <p className="text-sm text-blue-800 text-center">
                            Tip: Ensure your hand is clearly visible and well-lit for best results.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default GestureToAudio;

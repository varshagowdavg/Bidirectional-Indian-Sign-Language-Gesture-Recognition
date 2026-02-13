import React, { useState, useRef } from 'react';
import { Mic, Upload, Play, Square, Loader2, Image as ImageIcon } from 'lucide-react';
import axios from 'axios';

const AudioToGesture = () => {
    const [isRecording, setIsRecording] = useState(false);
    const [audioBlob, setAudioBlob] = useState(null);
    const [transcribedText, setTranscribedText] = useState('');
    const [gestureImageUrl, setGestureImageUrl] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const mediaRecorderRef = useRef(null);
    const chunksRef = useRef([]);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            chunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (e) => {
                if (e.data.size > 0) {
                    chunksRef.current.push(e.data);
                }
            };

            mediaRecorderRef.current.onstop = () => {
                const blob = new Blob(chunksRef.current, { type: 'audio/wav' });
                setAudioBlob(blob);
                handleUpload(blob);
            };

            mediaRecorderRef.current.start();
            setIsRecording(true);
            setError(null);
        } catch (err) {
            setError('Could not access microphone. Please check permissions.');
            console.error(err);
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
            mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
        }
    };

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            setAudioBlob(file);
            handleUpload(file);
        }
    };

    const handleUpload = async (blob) => {
        setLoading(true);
        setError(null);
        setGestureImageUrl(null);
        setTranscribedText('');

        const formData = new FormData();
        // Ensure filename has an extension
        const filename = blob.name || 'recording.wav';
        formData.append('file', blob, filename);

        try {
            const response = await axios.post('/api/audio/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setTranscribedText(response.data.transcribed_text);
            setGestureImageUrl(response.data.generated_image_url);
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || 'Error processing audio. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleTextSubmit = async (e) => {
        e.preventDefault();
        if (!transcribedText.trim()) return;

        setLoading(true);
        setError(null);
        setGestureImageUrl(null);

        try {
            const response = await axios.post('/api/audio/text-to-gesture', {
                text: transcribedText
            });

            setGestureImageUrl(response.data.generated_image_url);
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || 'Error converting text. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
            <div className="text-center space-y-4">
                <h1 className="text-3xl font-bold gradient-text">Audio to Gesture</h1>
                <p className="text-gray-600">
                    Record speech or upload audio to convert it into Indian Sign Language gestures.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Input Section */}
                <div className="space-y-6">
                    <div className="card space-y-6">
                        <h2 className="text-xl font-semibold flex items-center">
                            <Mic className="w-5 h-5 mr-2 text-blue-600" />
                            Input Source
                        </h2>

                        {/* Recording Controls */}
                        <div className="flex justify-center space-x-4">
                            {!isRecording ? (
                                <button
                                    onClick={startRecording}
                                    className="flex flex-col items-center justify-center w-32 h-32 rounded-full bg-red-50 hover:bg-red-100 border-2 border-red-200 transition-all duration-300 group"
                                >
                                    <div className="bg-red-500 text-white p-4 rounded-full shadow-lg group-hover:scale-110 transition-transform">
                                        <Mic className="w-8 h-8" />
                                    </div>
                                    <span className="mt-2 text-sm font-medium text-red-600">Record</span>
                                </button>
                            ) : (
                                <button
                                    onClick={stopRecording}
                                    className="flex flex-col items-center justify-center w-32 h-32 rounded-full bg-red-50 border-2 border-red-200 animate-pulse"
                                >
                                    <div className="bg-red-600 text-white p-4 rounded-full shadow-lg">
                                        <Square className="w-8 h-8" />
                                    </div>
                                    <span className="mt-2 text-sm font-medium text-red-600">Stop</span>
                                </button>
                            )}
                        </div>

                        <div className="relative">
                            <div className="absolute inset-0 flex items-center">
                                <div className="w-full border-t border-gray-200"></div>
                            </div>
                            <div className="relative flex justify-center text-sm">
                                <span className="px-2 bg-white text-gray-500">OR</span>
                            </div>
                        </div>

                        {/* File Upload */}
                        <div className="flex justify-center">
                            <label className="btn-secondary cursor-pointer flex items-center w-full justify-center">
                                <Upload className="w-5 h-5 mr-2" />
                                Upload Audio File
                                <input
                                    type="file"
                                    accept="audio/*"
                                    className="hidden"
                                    onChange={handleFileUpload}
                                />
                            </label>
                        </div>
                    </div>

                    {/* Text Input Fallback */}
                    <div className="card">
                        <form onSubmit={handleTextSubmit} className="space-y-4">
                            <label className="block text-sm font-medium text-gray-700">
                                Or type text directly
                            </label>
                            <div className="flex gap-2">
                                <input
                                    type="text"
                                    value={transcribedText}
                                    onChange={(e) => setTranscribedText(e.target.value)}
                                    placeholder="Type text to convert..."
                                    className="input-field"
                                />
                                <button
                                    type="submit"
                                    disabled={loading || !transcribedText.trim()}
                                    className="btn-primary px-6"
                                >
                                    {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Play className="w-5 h-5" />}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>

                {/* Output Section */}
                <div className="space-y-6">
                    <div className="card h-full min-h-[400px] flex flex-col">
                        <h2 className="text-xl font-semibold flex items-center mb-4">
                            <ImageIcon className="w-5 h-5 mr-2 text-blue-600" />
                            Generated Gesture
                        </h2>

                        <div className="flex-1 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200 flex items-center justify-center overflow-hidden relative">
                            {loading ? (
                                <div className="text-center space-y-3">
                                    <Loader2 className="w-10 h-10 text-blue-600 animate-spin mx-auto" />
                                    <p className="text-gray-500 font-medium">Processing...</p>
                                </div>
                            ) : error ? (
                                <div className="text-center p-6 text-red-500">
                                    <p>{error}</p>
                                </div>
                            ) : gestureImageUrl ? (
                                <div className="w-full h-full overflow-auto p-4">
                                    <img
                                        src={gestureImageUrl}
                                        alt="ISL Gesture"
                                        className="max-w-full h-auto mx-auto rounded-lg shadow-sm"
                                    />
                                    <div className="mt-4 text-center">
                                        <p className="text-sm text-gray-500 mb-1">Recognized Text:</p>
                                        <p className="text-lg font-bold text-gray-800">{transcribedText}</p>
                                    </div>
                                </div>
                            ) : (
                                <div className="text-center text-gray-400 p-6">
                                    <ImageIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
                                    <p>Output will appear here</p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AudioToGesture;

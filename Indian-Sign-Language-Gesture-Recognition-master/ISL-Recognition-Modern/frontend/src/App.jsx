import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import AudioToGesture from './pages/AudioToGesture';
import GestureToAudio from './pages/GestureToAudio';

function App() {
    return (
        <Router>
            <div className="min-h-screen">
                <Navbar />

                <main className="container mx-auto px-4 py-8">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/audio-to-gesture" element={<AudioToGesture />} />
                        <Route path="/gesture-to-audio" element={<GestureToAudio />} />
                        {/* Redirect any unknown routes to home */}
                        <Route path="*" element={<Navigate to="/" />} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
}

export default App;

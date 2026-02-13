import { Link } from 'react-router-dom';
import { Hand, Menu, X } from 'lucide-react';
import { useState } from 'react';

export default function Navbar() {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    return (
        <nav className="bg-white/80 backdrop-blur-md shadow-lg sticky top-0 z-50 border-b border-gray-100">
            <div className="container mx-auto px-4">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link to="/" className="flex items-center space-x-2 group">
                        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-2 rounded-lg transform group-hover:scale-110 transition-transform">
                            <Hand className="w-6 h-6 text-white" />
                        </div>
                        <span className="text-xl font-bold gradient-text hidden sm:block">
                            ISL Recognition
                        </span>
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center space-x-6">
                        <Link to="/audio-to-gesture" className="text-gray-700 hover:text-blue-600 font-medium transition-colors relative group">
                            Audio → Gesture
                            <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-blue-600 transition-all duration-300 group-hover:w-full"></span>
                        </Link>
                        <Link to="/gesture-to-audio" className="text-gray-700 hover:text-blue-600 font-medium transition-colors relative group">
                            Gesture → Audio
                            <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-blue-600 transition-all duration-300 group-hover:w-full"></span>
                        </Link>
                    </div>

                    {/* Mobile menu button */}
                    <button
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                    </button>
                </div>

                {/* Mobile Navigation */}
                {mobileMenuOpen && (
                    <div className="md:hidden py-4 border-t border-gray-200 animate-slide-up">
                        <div className="flex flex-col space-y-3">
                            <Link
                                to="/audio-to-gesture"
                                className="text-gray-700 font-medium py-2 px-4 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors"
                                onClick={() => setMobileMenuOpen(false)}
                            >
                                Audio → Gesture
                            </Link>
                            <Link
                                to="/gesture-to-audio"
                                className="text-gray-700 font-medium py-2 px-4 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors"
                                onClick={() => setMobileMenuOpen(false)}
                            >
                                Gesture → Audio
                            </Link>
                        </div>
                    </div>
                )}
            </div>
        </nav>
    );
}

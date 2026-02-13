import { Link } from 'react-router-dom';
import { Hand, Mic, Video, ArrowRight, CheckCircle } from 'lucide-react';

export default function Home() {
    const features = [
        {
            icon: <Mic className="w-8 h-8" />,
            title: "Audio to Gesture",
            description: "Convert spoken words to ISL gesture images instantly",
            link: "/audio-to-gesture",
            color: "from-blue-500 to-cyan-500"
        },
        {
            icon: <Video className="w-8 h-8" />,
            title: "Gesture to Audio",
            description: "Real-time hand gesture recognition with speech output",
            link: "/gesture-to-audio",
            color: "from-purple-500 to-pink-500"
        }
    ];

    const benefits = [
        "98.52% accuracy for one-hand gestures",
        "97% accuracy for two-hand gestures",
        "Real-time processing with MediaPipe",
        "Cross-platform support (Windows, Mac, Linux)",
        "Modern, responsive interface",
        "No registration required"
    ];

    return (
        <div className="space-y-16 pb-16">
            {/* Hero Section */}
            <section className="text-center space-y-6 pt-12 animate-fade-in">
                <div className="inline-block">
                    <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-4 rounded-2xl animate-float">
                        <Hand className="w-16 h-16 text-white" />
                    </div>
                </div>

                <h1 className="text-5xl md:text-6xl font-bold">
                    <span className="gradient-text">Indian Sign Language</span>
                    <br />
                    Recognition System
                </h1>

                <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                    Breaking communication barriers with modern AI-powered sign language translation.
                    Bidirectional conversion between audio and ISL gestures.
                </p>

                <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
                    <Link to="/audio-to-gesture" className="btn-primary text-lg px-8 py-4">
                        Start Translating
                        <ArrowRight className="w-5 h-5 ml-2 inline" />
                    </Link>
                </div>
            </section>

            {/* Features Grid */}
            <section className="space-y-8 animate-slide-up">
                <h2 className="text-3xl font-bold text-center">
                    Powerful Features
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
                    {features.map((feature, index) => (
                        <Link
                            key={index}
                            to={feature.link}
                            className="group card hover:scale-105 transform transition-all duration-300"
                        >
                            <div className={`bg-gradient-to-r ${feature.color} p-3 rounded-xl inline-block mb-4 group-hover:scale-110 transition-transform`}>
                                {feature.icon}
                            </div>
                            <h3 className="text-xl font-bold mb-2 group-hover:text-blue-600 transition-colors">
                                {feature.title}
                            </h3>
                            <p className="text-gray-600">
                                {feature.description}
                            </p>
                            <div className="mt-4 text-blue-600 font-semibold flex items-center">
                                Try it now
                                <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-2 transition-transform" />
                            </div>
                        </Link>
                    ))}
                </div>
            </section>

            {/* Benefits Section */}
            <section className="glass-card max-w-4xl mx-auto">
                <h2 className="text-3xl font-bold text-center mb-8">
                    Why Choose Our System?
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {benefits.map((benefit, index) => (
                        <div key={index} className="flex items-start space-x-3">
                            <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0 mt-1" />
                            <span className="text-gray-700">{benefit}</span>
                        </div>
                    ))}
                </div>
            </section>

            {/* Technology Stack */}
            <section className="text-center space-y-6">
                <h2 className="text-3xl font-bold">
                    Built with Modern Technology
                </h2>

                <div className="flex flex-wrap justify-center gap-4">
                    {['FastAPI', 'React', 'TensorFlow', 'MediaPipe', 'OpenCV', 'PostgreSQL'].map((tech, index) => (
                        <div
                            key={index}
                            className="bg-white/50 backdrop-blur-sm px-6 py-3 rounded-full border-2 border-gray-200 hover:border-blue-400 hover:shadow-lg transition-all duration-300"
                        >
                            <span className="font-semibold text-gray-700">{tech}</span>
                        </div>
                    ))}
                </div>
            </section>

            {/* CTA Section */}
            <section className="card bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-center max-w-3xl mx-auto">
                <h2 className="text-3xl font-bold mb-4">
                    Ready to Get Started?
                </h2>
                <p className="text-lg mb-6 opacity-90">
                    Join us in making communication accessible for everyone.
                    Start using the tool instantly.
                </p>
                <Link to="/gesture-to-audio" className="bg-white text-blue-600 px-8 py-4 rounded-lg font-bold hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200 inline-block">
                    Try Gesture Recognition
                </Link>
            </section>
        </div>
    );
}

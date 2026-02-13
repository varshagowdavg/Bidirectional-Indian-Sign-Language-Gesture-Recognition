import React from 'react';

const GestureKeyboard = () => {
    return (
        <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-6 text-gray-800">Gesture Keyboard</h1>
            <div className="bg-white rounded-lg shadow-lg p-6">
                <p className="text-gray-600 mb-4">
                    Type using sign language gestures.
                </p>
                <textarea
                    className="w-full h-32 p-4 border rounded-lg mb-4 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Text will appear here..."
                    readOnly
                ></textarea>
                <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300">
                    <span className="text-gray-400">Camera Feed Placeholder</span>
                </div>
            </div>
        </div>
    );
};

export default GestureKeyboard;

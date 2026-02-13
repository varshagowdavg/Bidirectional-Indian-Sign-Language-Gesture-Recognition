import React from 'react';

const Emergency = () => {
    return (
        <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-6 text-red-600">Emergency Assistance</h1>
            <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-red-500">
                <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <button className="bg-red-600 text-white p-4 rounded-lg hover:bg-red-700 transition-colors flex items-center justify-center gap-2">
                        <span className="text-2xl">🚑</span>
                        Call Ambulance
                    </button>
                    <button className="bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center gap-2">
                        <span className="text-2xl">👮</span>
                        Call Police
                    </button>
                    <button className="bg-orange-500 text-white p-4 rounded-lg hover:bg-orange-600 transition-colors flex items-center justify-center gap-2">
                        <span className="text-2xl">🚒</span>
                        Call Fire Dept
                    </button>
                    <button className="bg-gray-600 text-white p-4 rounded-lg hover:bg-gray-700 transition-colors flex items-center justify-center gap-2">
                        <span className="text-2xl">📞</span>
                        Emergency Contacts
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Emergency;

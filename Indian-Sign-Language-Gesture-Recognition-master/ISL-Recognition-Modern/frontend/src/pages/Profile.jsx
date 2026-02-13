import React from 'react';

const Profile = ({ user }) => {
    return (
        <div className="max-w-2xl mx-auto">
            <h1 className="text-3xl font-bold mb-6 text-gray-800">User Profile</h1>
            <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center gap-4 mb-6">
                    <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 text-2xl font-bold">
                        {user?.username?.[0]?.toUpperCase() || 'U'}
                    </div>
                    <div>
                        <h2 className="text-xl font-semibold">{user?.username || 'User'}</h2>
                        <p className="text-gray-500">{user?.email || 'email@example.com'}</p>
                    </div>
                </div>

                <div className="border-t pt-6">
                    <h3 className="text-lg font-semibold mb-4">Account Settings</h3>
                    <div className="space-y-4">
                        <button className="w-full text-left px-4 py-2 rounded hover:bg-gray-50 text-gray-700">
                            Edit Profile
                        </button>
                        <button className="w-full text-left px-4 py-2 rounded hover:bg-gray-50 text-gray-700">
                            Change Password
                        </button>
                        <button className="w-full text-left px-4 py-2 rounded hover:bg-gray-50 text-gray-700">
                            Notification Preferences
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Profile;

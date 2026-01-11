import React, { useState } from 'react';
import authService from '../services/authService';

const AuthTest = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const addResult = (message, type = 'info') => {
    setResults(prev => [...prev, { message, type, timestamp: new Date().toLocaleTimeString() }]);
  };

  const testRegistration = async () => {
    try {
      addResult('Testing registration...', 'info');
      const result = await authService.register({
        email: 'authtest@example.com',
        password: 'TestPass123',
        first_name: 'Auth',
        last_name: 'Test'
      });
      addResult(`Registration successful: ${JSON.stringify(result)}`, 'success');
    } catch (error) {
      addResult(`Registration failed: ${error.message}`, 'error');
      console.error('Registration error:', error);
    }
  };

  const testLogin = async () => {
    try {
      addResult('Testing login...', 'info');
      const result = await authService.login('authtest@example.com', 'TestPass123');
      addResult(`Login successful: ${JSON.stringify(result)}`, 'success');
    } catch (error) {
      addResult(`Login failed: ${error.message}`, 'error');
      console.error('Login error:', error);
    }
  };

  const testProfile = async () => {
    try {
      addResult('Testing profile...', 'info');
      const result = await authService.getCurrentUser();
      addResult(`Profile retrieved: ${JSON.stringify(result)}`, 'success');
    } catch (error) {
      addResult(`Profile failed: ${error.message}`, 'error');
      console.error('Profile error:', error);
    }
  };

  const runAllTests = async () => {
    setLoading(true);
    setResults([]);
    
    await testRegistration();
    await new Promise(resolve => setTimeout(resolve, 1000));
    await testLogin();
    await new Promise(resolve => setTimeout(resolve, 1000));
    await testProfile();
    
    setLoading(false);
  };

  const clearResults = () => {
    setResults([]);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Authentication Test Page</h1>
      
      <div className="mb-6 space-x-4">
        <button
          onClick={runAllTests}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
        >
          {loading ? 'Running Tests...' : 'Run All Tests'}
        </button>
        <button
          onClick={testRegistration}
          disabled={loading}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:bg-gray-400"
        >
          Test Registration
        </button>
        <button
          onClick={testLogin}
          disabled={loading}
          className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600 disabled:bg-gray-400"
        >
          Test Login
        </button>
        <button
          onClick={testProfile}
          disabled={loading}
          className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600 disabled:bg-gray-400"
        >
          Test Profile
        </button>
        <button
          onClick={clearResults}
          className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
        >
          Clear Results
        </button>
      </div>

      <div className="bg-gray-100 p-4 rounded-lg">
        <h2 className="text-xl font-semibold mb-4">Test Results:</h2>
        {results.length === 0 ? (
          <p className="text-gray-500">No tests run yet. Click a button above to start testing.</p>
        ) : (
          <div className="space-y-2">
            {results.map((result, index) => (
              <div
                key={index}
                className={`p-2 rounded ${
                  result.type === 'success'
                    ? 'bg-green-100 text-green-800'
                    : result.type === 'error'
                    ? 'bg-red-100 text-red-800'
                    : 'bg-blue-100 text-blue-800'
                }`}
              >
                <span className="text-xs text-gray-500">[{result.timestamp}]</span> {result.message}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
        <h3 className="font-semibold text-yellow-800">Debug Information:</h3>
        <p className="text-sm text-yellow-700">
          API Base URL: {process.env.REACT_APP_API_URL || 'http://localhost:5000/api'}
        </p>
        <p className="text-sm text-yellow-700">
          Current Token: {authService.getToken() ? 'Present' : 'None'}
        </p>
        <p className="text-sm text-yellow-700">
          Is Authenticated: {authService.isAuthenticated() ? 'Yes' : 'No'}
        </p>
      </div>
    </div>
  );
};

export default AuthTest;
// Simple test script to verify frontend authentication
const axios = require('axios');

const API_BASE = 'http://localhost:5000/api';

async function testFrontendAuth() {
  console.log('🔍 Testing frontend authentication flow...\n');

  try {
    // Test registration
    console.log('1. Testing registration...');
    const registerData = {
      email: 'frontend_test@example.com',
      password: 'TestPass123',
      first_name: 'Frontend',
      last_name: 'Test'
    };

    const registerResponse = await axios.post(`${API_BASE}/auth/register`, registerData, {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    console.log('✅ Registration successful');
    console.log('Response status:', registerResponse.status);
    console.log('Response data keys:', Object.keys(registerResponse.data));

    // Test login
    console.log('\n2. Testing login...');
    const loginData = {
      email: 'frontend_test@example.com',
      password: 'TestPass123'
    };

    const loginResponse = await axios.post(`${API_BASE}/auth/login`, loginData, {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    console.log('✅ Login successful');
    console.log('Response status:', loginResponse.status);
    console.log('Response data keys:', Object.keys(loginResponse.data));

    // Test profile access
    console.log('\n3. Testing profile access...');
    const token = loginResponse.data.tokens.access_token;
    
    const profileResponse = await axios.get(`${API_BASE}/auth/profile`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    console.log('✅ Profile access successful');
    console.log('Response status:', profileResponse.status);
    console.log('User email:', profileResponse.data.user.email);

    console.log('\n🎉 All frontend authentication tests passed!');
    console.log('\nThe backend is working correctly. If frontend login is still failing,');
    console.log('check the browser console for specific error messages.');

  } catch (error) {
    console.error('❌ Test failed:', error.message);
    if (error.response) {
      console.error('Status:', error.response.status);
      console.error('Data:', error.response.data);
    }
  }
}

testFrontendAuth();
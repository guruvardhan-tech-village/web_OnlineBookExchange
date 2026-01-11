// Debug script to test authentication from frontend
import authService from '../services/authService';

export const testAuthentication = async () => {
  console.log('🔍 Testing authentication from frontend...');
  
  try {
    // Test registration
    console.log('1. Testing registration...');
    const registerData = {
      email: 'debug_test@example.com',
      password: 'DebugPass123',
      first_name: 'Debug',
      last_name: 'Test'
    };

    const registerResult = await authService.register(registerData);
    console.log('✅ Registration successful:', registerResult);

    // Test login
    console.log('2. Testing login...');
    const loginResult = await authService.login('debug_test@example.com', 'DebugPass123');
    console.log('✅ Login successful:', loginResult);

    // Test profile
    console.log('3. Testing profile...');
    const profile = await authService.getCurrentUser();
    console.log('✅ Profile retrieved:', profile);

    console.log('🎉 All tests passed!');
    return true;

  } catch (error) {
    console.error('❌ Authentication test failed:', error);
    console.error('Error details:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status
    });
    return false;
  }
};

// Auto-run test when imported
if (window.location.search.includes('debug=auth')) {
  testAuthentication();
}
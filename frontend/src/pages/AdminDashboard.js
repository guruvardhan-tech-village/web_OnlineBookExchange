import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-toastify';
import adminService from '../services/adminService';
import LoadingSpinner from '../components/LoadingSpinner';

const AdminDashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await adminService.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch admin stats:', error);
      setError('Failed to load dashboard statistics');
      toast.error('Failed to load dashboard statistics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-xl mb-4">⚠️ Error</div>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={fetchStats}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const { overview, recent_activity, popular_categories, top_users } = stats || {};

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Welcome, {user?.first_name}! Monitor and manage the book exchange system.
          </p>
        </div>

        {/* Overview Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Users"
            value={overview?.total_users || 0}
            icon="👥"
            color="blue"
          />
          <StatCard
            title="Total Books"
            value={overview?.total_books || 0}
            icon="📚"
            color="green"
          />
          <StatCard
            title="Total Exchanges"
            value={overview?.total_exchanges || 0}
            icon="🔄"
            color="purple"
          />
          <StatCard
            title="Success Rate"
            value={`${overview?.exchange_success_rate || 0}%`}
            icon="✅"
            color="yellow"
          />
        </div>

        {/* Secondary Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatCard
            title="Active Books"
            value={overview?.active_books || 0}
            subtitle="Available for exchange"
            icon="📖"
            color="indigo"
          />
          <StatCard
            title="Pending Exchanges"
            value={overview?.pending_exchanges || 0}
            subtitle="Awaiting approval"
            icon="⏳"
            color="orange"
          />
          <StatCard
            title="Completed Exchanges"
            value={overview?.completed_exchanges || 0}
            subtitle="Successfully completed"
            icon="🎉"
            color="emerald"
          />
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Activity (Last 30 Days)</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">{recent_activity?.new_users_month || 0}</div>
              <div className="text-sm text-gray-600">New Users</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">{recent_activity?.new_books_month || 0}</div>
              <div className="text-sm text-gray-600">New Books</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600">{recent_activity?.new_exchanges_month || 0}</div>
              <div className="text-sm text-gray-600">New Exchanges</div>
            </div>
          </div>
        </div>

        {/* Charts and Analytics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Popular Categories */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Popular Categories</h2>
            <div className="space-y-4">
              {popular_categories?.map((category, index) => (
                <CategoryBar
                  key={category.category}
                  category={category.category}
                  count={category.count}
                  maxCount={popular_categories[0]?.count || 1}
                  rank={index + 1}
                />
              ))}
              {(!popular_categories || popular_categories.length === 0) && (
                <div className="text-center text-gray-500 py-8">
                  No category data available
                </div>
              )}
            </div>
          </div>

          {/* Top Users */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Top Contributors</h2>
            <div className="space-y-4">
              {top_users?.map((user, index) => (
                <UserCard
                  key={user.email}
                  name={user.name}
                  email={user.email}
                  bookCount={user.book_count}
                  rank={index + 1}
                />
              ))}
              {(!top_users || top_users.length === 0) && (
                <div className="text-center text-gray-500 py-8">
                  No user data available
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <ActionButton
              title="Manage Users"
              description="View and manage user accounts"
              icon="👥"
              onClick={() => {
                // TODO: Navigate to user management page
                toast.info('User management page coming soon');
              }}
            />
            <ActionButton
              title="Moderate Books"
              description="Review and moderate book listings"
              icon="📚"
              onClick={() => {
                // TODO: Navigate to book moderation page
                toast.info('Book moderation page coming soon');
              }}
            />
            <ActionButton
              title="System Settings"
              description="Configure system settings"
              icon="⚙️"
              onClick={() => {
                // TODO: Navigate to system settings page
                toast.info('System settings page coming soon');
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

// Reusable StatCard component
const StatCard = ({ title, value, subtitle, icon, color }) => {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600 border-blue-200',
    green: 'bg-green-50 text-green-600 border-green-200',
    purple: 'bg-purple-50 text-purple-600 border-purple-200',
    yellow: 'bg-yellow-50 text-yellow-600 border-yellow-200',
    indigo: 'bg-indigo-50 text-indigo-600 border-indigo-200',
    orange: 'bg-orange-50 text-orange-600 border-orange-200',
    emerald: 'bg-emerald-50 text-emerald-600 border-emerald-200'
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center">
        <div className={`flex-shrink-0 p-3 rounded-lg ${colorClasses[color] || colorClasses.blue}`}>
          <span className="text-2xl">{icon}</span>
        </div>
        <div className="ml-4 flex-1">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-semibold text-gray-900">{value}</p>
          {subtitle && (
            <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
          )}
        </div>
      </div>
    </div>
  );
};

// CategoryBar component for popular categories visualization
const CategoryBar = ({ category, count, maxCount, rank }) => {
  const percentage = (count / maxCount) * 100;
  
  return (
    <div className="flex items-center space-x-3">
      <div className="flex-shrink-0 w-6 text-center">
        <span className="text-sm font-medium text-gray-500">#{rank}</span>
      </div>
      <div className="flex-1">
        <div className="flex justify-between items-center mb-1">
          <span className="text-sm font-medium text-gray-900 capitalize">{category}</span>
          <span className="text-sm text-gray-600">{count} books</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${percentage}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

// UserCard component for top users
const UserCard = ({ name, email, bookCount, rank }) => {
  const getRankIcon = (rank) => {
    switch (rank) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return `#${rank}`;
    }
  };

  return (
    <div className="flex items-center space-x-3 p-3 rounded-lg bg-gray-50">
      <div className="flex-shrink-0 w-8 text-center">
        <span className="text-lg">{getRankIcon(rank)}</span>
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900 truncate">{name}</p>
        <p className="text-xs text-gray-500 truncate">{email}</p>
      </div>
      <div className="flex-shrink-0">
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
          {bookCount} books
        </span>
      </div>
    </div>
  );
};

// ActionButton component for quick actions
const ActionButton = ({ title, description, icon, onClick }) => {
  return (
    <button
      onClick={onClick}
      className="text-left p-4 rounded-lg border border-gray-200 hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 group"
    >
      <div className="flex items-center space-x-3">
        <div className="flex-shrink-0">
          <span className="text-2xl">{icon}</span>
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-gray-900 group-hover:text-blue-900">
            {title}
          </p>
          <p className="text-xs text-gray-500 group-hover:text-blue-700">
            {description}
          </p>
        </div>
      </div>
    </button>
  );
};

export default AdminDashboard;
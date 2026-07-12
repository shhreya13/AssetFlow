import { Link } from 'react-router-dom';
import { 
  Package, CheckCircle, AlertTriangle, Calendar, 
  TrendingUp, Clock, Plus, BookOpen, Wrench 
} from 'lucide-react';

export default function Dashboard() {
  // Mock data - replace with API later
  const stats = {
    totalAssets: 142,
    available: 58,
    allocated: 72,
    maintenance: 12,
    overdue: 8,
    activeBookings: 15,
  };

  const recentActivity = [
    { id: 1, action: 'Asset Allocated', asset: 'Laptop AF-0114', user: 'Priya', time: '5 min ago' },
    { id: 2, action: 'Maintenance Approved', asset: 'Projector AF-023', user: 'Raj', time: '15 min ago' },
    { id: 3, action: 'Booking Confirmed', asset: 'Conference Room B', user: 'Alex', time: '30 min ago' },
  ];

  const overdueItems = [
    { id: 1, asset: 'MacBook Pro', allocatedTo: 'Sneha', dueDate: '2024-01-20', daysOverdue: 5 },
    { id: 2, asset: 'Camera Sony', allocatedTo: 'Vikram', dueDate: '2024-01-18', daysOverdue: 7 },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-dark">Dashboard</h1>
          <p className="text-gray-500">Welcome back, John!</p>
        </div>
        <div className="flex gap-3">
          <Link to="/assets/register" className="bg-primary text-white px-4 py-2 rounded-xl flex items-center gap-2 hover:bg-secondary transition">
            <Plus className="w-4 h-4" /> Register Asset
          </Link>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-gray-500 text-sm">Total Assets</p>
              <h3 className="text-2xl font-bold text-dark mt-1">{stats.totalAssets}</h3>
            </div>
            <div className="bg-blue-50 p-3 rounded-xl">
              <Package className="w-6 h-6 text-primary" />
            </div>
          </div>
          <div className="mt-4 flex gap-2 text-xs">
            <span className="text-success">{stats.available} Available</span>
            <span className="text-primary">{stats.allocated} Allocated</span>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-gray-500 text-sm">Under Maintenance</p>
              <h3 className="text-2xl font-bold text-dark mt-1">{stats.maintenance}</h3>
            </div>
            <div className="bg-yellow-50 p-3 rounded-xl">
              <Wrench className="w-6 h-6 text-warning" />
            </div>
          </div>
          <div className="mt-4 text-xs text-gray-500">2 pending approval</div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-gray-500 text-sm">Active Bookings</p>
              <h3 className="text-2xl font-bold text-dark mt-1">{stats.activeBookings}</h3>
            </div>
            <div className="bg-purple-50 p-3 rounded-xl">
              <Calendar className="w-6 h-6 text-secondary" />
            </div>
          </div>
          <div className="mt-4 text-xs text-gray-500">5 end today</div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-sm border border-red-100">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-gray-500 text-sm">Overdue Returns</p>
              <h3 className="text-2xl font-bold text-accent mt-1">{stats.overdue}</h3>
            </div>
            <div className="bg-red-50 p-3 rounded-xl">
              <Clock className="w-6 h-6 text-accent" />
            </div>
          </div>
          <div className="mt-4 text-xs text-red-500">⚠️ Action required!</div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link to="/assets/register" className="bg-gradient-to-r from-primary to-secondary text-white p-4 rounded-xl flex items-center gap-3 hover:shadow-lg transition">
          <Package className="w-6 h-6" />
          <div>
            <h4 className="font-semibold">Register Asset</h4>
            <p className="text-sm opacity-90">Add new asset to inventory</p>
          </div>
        </Link>
        <Link to="/bookings" className="bg-gradient-to-r from-blue-500 to-blue-700 text-white p-4 rounded-xl flex items-center gap-3 hover:shadow-lg transition">
          <BookOpen className="w-6 h-6" />
          <div>
            <h4 className="font-semibold">Book Resource</h4>
            <p className="text-sm opacity-90">Book shared resources</p>
          </div>
        </Link>
        <Link to="/maintenance" className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white p-4 rounded-xl flex items-center gap-3 hover:shadow-lg transition">
          <Wrench className="w-6 h-6" />
          <div>
            <h4 className="font-semibold">Raise Maintenance</h4>
            <p className="text-sm opacity-90">Request repair</p>
          </div>
        </Link>
      </div>

      {/* Activity & Overdue */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h3 className="font-semibold text-dark mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-primary" />
            Recent Activity
          </h3>
          <div className="space-y-4">
            {recentActivity.map((item) => (
              <div key={item.id} className="flex items-center gap-3 p-3 hover:bg-gray-50 rounded-xl transition">
                <div className="w-2 h-2 bg-primary rounded-full"></div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-dark">{item.action}</p>
                  <p className="text-xs text-gray-500">{item.asset} by {item.user}</p>
                </div>
                <span className="text-xs text-gray-400">{item.time}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-sm border border-red-100">
          <h3 className="font-semibold text-dark mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-accent" />
            Overdue Returns
          </h3>
          {overdueItems.map((item) => (
            <div key={item.id} className="flex items-center gap-3 p-3 bg-red-50 rounded-xl mb-3">
              <div className="bg-red-100 p-2 rounded-lg">
                <Clock className="w-5 h-5 text-accent" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-dark">{item.asset}</p>
                <p className="text-xs text-gray-500">Allocated to {item.allocatedTo}</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-bold text-accent">{item.daysOverdue}d overdue</p>
                <p className="text-xs text-gray-400">Due: {item.dueDate}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
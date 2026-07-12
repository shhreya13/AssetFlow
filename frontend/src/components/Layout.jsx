import { Outlet, Link, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, Package, Users, Building2, 
  Calendar, Wrench, ClipboardList, BarChart3, 
  Bell, LogOut, Menu 
} from 'lucide-react';
import { useState } from 'react';

export default function Layout() {
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const menuItems = [
    { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/assets', icon: Package, label: 'Assets' },
    { path: '/departments', icon: Building2, label: 'Departments' },
    { path: '/employees', icon: Users, label: 'Employees' },
    { path: '/bookings', icon: Calendar, label: 'Bookings' },
    { path: '/maintenance', icon: Wrench, label: 'Maintenance' },
    { path: '/audit', icon: ClipboardList, label: 'Audit' },
    { path: '/reports', icon: BarChart3, label: 'Reports' },
    { path: '/notifications', icon: Bell, label: 'Notifications' },
  ];

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar - Fixed dark background */}
      <aside className={`bg-[#1A1A2E] text-white w-64 min-h-screen fixed left-0 top-0 transition-transform duration-300 ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'} lg:translate-x-0 z-50`}>
        <div className="p-6">
          {/* Logo */}
          <div className="flex items-center gap-3 mb-8">
            <div className="w-10 h-10 bg-[#6C63FF] rounded-xl flex items-center justify-center">
              <Package className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-xl font-bold text-white">AssetFlow</h1>
          </div>
          
          {/* Navigation */}
          <nav className="space-y-1">
            {menuItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className="flex items-center gap-3 px-4 py-3 rounded-xl text-white hover:bg-white/10 transition-colors"
              >
                <item.icon className="w-5 h-5 text-white" />
                <span className="text-white">{item.label}</span>
              </Link>
            ))}
            
            {/* Logout Button */}
            <button
              onClick={handleLogout}
              className="flex items-center gap-3 px-4 py-3 rounded-xl text-white hover:bg-white/10 transition-colors w-full mt-4"
            >
              <LogOut className="w-5 h-5 text-white" />
              <span className="text-white">Logout</span>
            </button>
          </nav>
        </div>
      </aside>

      {/* Mobile Menu Button */}
      <button
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 bg-[#1A1A2E] text-white p-2 rounded-xl shadow-lg"
      >
        <Menu className="w-6 h-6" />
      </button>

      {/* Main Content */}
      <main className="flex-1 lg:ml-64 p-6">
        <div className="max-w-7xl mx-auto">
          <Outlet />
        </div>
      </main>

      {/* Overlay for mobile */}
      {isMobileMenuOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-40"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
    </div>
  );
}
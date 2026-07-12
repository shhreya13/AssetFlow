import { NavLink } from "react-router-dom";
import {
  FaTachometerAlt,
  FaBoxOpen,
  FaCalendarAlt,
  FaTools,
  FaClipboardCheck,
  FaChartBar,
  FaBell,
} from "react-icons/fa";

const menuItems = [
  { name: "Dashboard", path: "/", icon: <FaTachometerAlt /> },
  { name: "Assets", path: "/assets", icon: <FaBoxOpen /> },
  { name: "Bookings", path: "/bookings", icon: <FaCalendarAlt /> },
  { name: "Maintenance", path: "/maintenance", icon: <FaTools /> },
  { name: "Audit", path: "/audit", icon: <FaClipboardCheck /> },
  { name: "Reports", path: "/reports", icon: <FaChartBar /> },
  { name: "Notifications", path: "/notifications", icon: <FaBell /> },
];

function Sidebar() {
  return (
    <aside className="w-64 h-screen bg-slate-900 text-white fixed left-0 top-0 shadow-lg">
      <div className="text-2xl font-bold text-center py-6 border-b border-slate-700">
        AssetFlow
      </div>

      <nav className="mt-6">
        {menuItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-6 py-3 transition ${
                isActive
                  ? "bg-blue-600"
                  : "hover:bg-slate-800"
              }`
            }
          >
            {item.icon}
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;
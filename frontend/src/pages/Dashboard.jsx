import DashboardLayout from "../layouts/DashboardLayout";
import StatCard from "../components/StatCard";

function Dashboard() {
  const stats = [
    { title: "Assets Available", value: 125, color: "#22c55e" },
    { title: "Assets Allocated", value: 84, color: "#3b82f6" },
    { title: "Maintenance", value: 12, color: "#f59e0b" },
    { title: "Bookings", value: 18, color: "#8b5cf6" },
  ];

  return (
    <DashboardLayout>
      <h2 className="text-3xl font-bold mb-6">Dashboard</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        {stats.map((item) => (
          <StatCard
            key={item.title}
            title={item.title}
            value={item.value}
            color={item.color}
          />
        ))}
      </div>

      <div className="bg-white mt-8 rounded-xl shadow-md p-6">
        <h3 className="text-xl font-semibold mb-4">Recent Assets</h3>

        <table className="w-full text-left">
          <thead>
            <tr className="border-b">
              <th className="py-3">Asset ID</th>
              <th>Name</th>
              <th>Category</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            <tr className="border-b">
              <td className="py-3">AF-0001</td>
              <td>Dell Latitude 5440</td>
              <td>Laptop</td>
              <td className="text-green-600 font-semibold">Available</td>
            </tr>

            <tr className="border-b">
              <td className="py-3">AF-0002</td>
              <td>Conference Room A</td>
              <td>Room</td>
              <td className="text-blue-600 font-semibold">Booked</td>
            </tr>

            <tr>
              <td className="py-3">AF-0003</td>
              <td>Canon Printer</td>
              <td>Printer</td>
              <td className="text-yellow-600 font-semibold">
                Maintenance
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </DashboardLayout>
  );
}

export default Dashboard;
function StatCard({ title, value, color }) {
  return (
    <div className="bg-white rounded-xl shadow-md p-5 border-l-4" style={{ borderColor: color }}>
      <h3 className="text-gray-500 text-sm">{title}</h3>
      <h2 className="text-3xl font-bold mt-2">{value}</h2>
    </div>
  );
}

export default StatCard;
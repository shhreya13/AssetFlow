import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, Plus, Filter, Eye, Edit, Trash2 } from 'lucide-react';

export default function Assets() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  const assets = [
    { id: 1, name: 'MacBook Pro 16"', tag: 'AF-0001', category: 'Electronics', status: 'Available', allocatedTo: null, condition: 'Good' },
    { id: 2, name: 'Dell XPS 15', tag: 'AF-0002', category: 'Electronics', status: 'Allocated', allocatedTo: 'Priya Sharma', condition: 'Excellent' },
    { id: 3, name: 'Projector Epson', tag: 'AF-0003', category: 'Electronics', status: 'Under Maintenance', allocatedTo: null, condition: 'Needs Repair' },
    { id: 4, name: 'Meeting Table', tag: 'AF-0004', category: 'Furniture', status: 'Available', allocatedTo: null, condition: 'Good' },
    { id: 5, name: 'Toyota Innova', tag: 'AF-0005', category: 'Vehicle', status: 'Allocated', allocatedTo: 'Raj Kumar', condition: 'Good' },
  ];

  const getStatusColor = (status) => {
    const colors = {
      Available: 'bg-green-100 text-green-700',
      Allocated: 'bg-blue-100 text-blue-700',
      'Under Maintenance': 'bg-yellow-100 text-yellow-700',
      Reserved: 'bg-purple-100 text-purple-700',
      Lost: 'bg-red-100 text-red-700',
      Retired: 'bg-gray-100 text-gray-700',
      Disposed: 'bg-red-100 text-red-700',
    };
    return colors[status] || 'bg-gray-100 text-gray-700';
  };

  const filteredAssets = assets.filter(asset => {
    const matchesSearch = asset.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          asset.tag.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || asset.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="space-y-6">
      {/* Header with Register Asset Button */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-[#1A1A2E]">Asset Directory</h1>
          <p className="text-gray-500">Manage and track all assets</p>
        </div>
        <Link 
          to="/assets/register" 
          className="bg-[#6C63FF] text-white px-4 py-2 rounded-xl flex items-center gap-2 hover:bg-[#4A3F8A] transition whitespace-nowrap"
        >
          <Plus className="w-4 h-4" /> Register Asset
        </Link>
      </div>

      {/* Search and Filter */}
      <div className="flex flex-col md:flex-row gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Search by name or asset tag..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#6C63FF]"
          />
        </div>
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#6C63FF] bg-white"
        >
          <option value="all">All Status</option>
          <option value="Available">Available</option>
          <option value="Allocated">Allocated</option>
          <option value="Under Maintenance">Under Maintenance</option>
          <option value="Reserved">Reserved</option>
          <option value="Lost">Lost</option>
          <option value="Retired">Retired</option>
        </select>
        <button className="px-4 py-3 border border-gray-200 rounded-xl hover:bg-gray-50 transition">
          <Filter className="w-5 h-5 text-gray-500" />
        </button>
      </div>

      {/* Assets Table */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-200">
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Asset Tag</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Name</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Category</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Status</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Allocated To</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Condition</th>
                <th className="text-right px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredAssets.map((asset) => (
                <tr key={asset.id} className="border-b border-gray-100 hover:bg-gray-50 transition">
                  <td className="px-6 py-4">
                    <span className="font-mono text-sm font-medium text-[#6C63FF]">{asset.tag}</span>
                  </td>
                  <td className="px-6 py-4 font-medium text-[#1A1A2E]">{asset.name}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{asset.category}</td>
                  <td className="px-6 py-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(asset.status)}`}>
                      {asset.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">{asset.allocatedTo || '—'}</td>
                  <td className="px-6 py-4 text-sm">
                    <span className="flex items-center gap-1">
                      <span className={`w-2 h-2 rounded-full ${asset.condition === 'Excellent' ? 'bg-green-500' : asset.condition === 'Good' ? 'bg-blue-400' : 'bg-yellow-400'}`}></span>
                      {asset.condition}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex justify-end gap-2">
                      <button className="p-1 hover:bg-gray-100 rounded-lg transition">
                        <Eye className="w-4 h-4 text-gray-500" />
                      </button>
                      <button className="p-1 hover:bg-gray-100 rounded-lg transition">
                        <Edit className="w-4 h-4 text-gray-500" />
                      </button>
                      <button className="p-1 hover:bg-red-50 rounded-lg transition">
                        <Trash2 className="w-4 h-4 text-red-500" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
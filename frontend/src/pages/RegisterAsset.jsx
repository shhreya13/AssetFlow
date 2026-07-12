import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload } from 'lucide-react';

export default function RegisterAsset() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    serialNumber: '',
    acquisitionDate: '',
    acquisitionCost: '',
    condition: 'Good',
    location: '',
    description: '',
    isBookable: false,
  });

  const categories = ['Electronics', 'Furniture', 'Vehicle', 'Equipment', 'Other'];

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Asset registered successfully! Asset Tag: AF-' + String(Math.floor(Math.random() * 10000)).padStart(4, '0'));
    navigate('/assets');
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-[#1A1A2E]">Register New Asset</h1>
        <p className="text-gray-500">Add a new asset to the inventory</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700">Asset Name *</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#6C63FF]"
              placeholder="e.g., MacBook Pro 16"
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700">Category *</label>
            <select
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#6C63FF] bg-white"
              required
            >
              <option value="">Select Category</option>
              {categories.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700">Serial Number</label>
            <input
              type="text"
              value={formData.serialNumber}
              onChange={(e) => setFormData({ ...formData, serialNumber: e.target.value })}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#6C63FF]"
              placeholder="Enter serial number"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700">Acquisition Date</label>
            <input
              type="date"
              value={formData.acquisitionDate}
              onChange={(e) => setFormData({ ...formData, acquisitionDate: e.target.value })}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#6C63FF]"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700">Acquisition Cost ($)</label>
            <input
              type="number"
              value={formData.acquisitionCost}
              onChange={(e) => setFormData({ ...formData, acquisitionCost: e.target.value })}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#6C63FF]"
              placeholder="e.g., 1500"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700">Condition *</label>
            <select
              value={formData.condition}
              onChange={(e) => setFormData({ ...formData, condition: e.target.value })}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#6C63FF] bg-white"
              required
            >
              <option value="Excellent">Excellent</option>
              <option value="Good">Good</option>
              <option value="Fair">Fair</option>
              <option value="Poor">Poor</option>
              <option value="Needs Repair">Needs Repair</option>
            </select>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700">Location</label>
            <input
              type="text"
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#6C63FF]"
              placeholder="e.g., Warehouse A, Floor 2"
            />
          </div>

          <div className="space-y-2 md:col-span-2">
            <label className="text-sm font-medium text-gray-700">Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#6C63FF] resize-none"
              rows="3"
              placeholder="Additional details about the asset..."
            />
          </div>

          <div className="space-y-2 md:col-span-2">
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.isBookable}
                onChange={(e) => setFormData({ ...formData, isBookable: e.target.checked })}
                className="w-5 h-5 text-[#6C63FF] rounded border-gray-300 focus:ring-[#6C63FF]"
              />
              <span className="text-sm font-medium text-gray-700">This is a shared/bookable resource</span>
            </label>
          </div>
        </div>

        <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-[#6C63FF] transition">
          <Upload className="w-10 h-10 text-gray-400 mx-auto mb-3" />
          <p className="text-sm text-gray-600">Drag & drop asset photos, or <span className="text-[#6C63FF] font-medium">browse</span></p>
          <p className="text-xs text-gray-400 mt-1">PNG, JPG, PDF up to 10MB</p>
        </div>

        <div className="flex gap-3 pt-4 border-t border-gray-100">
          <button
            type="button"
            onClick={() => navigate('/assets')}
            className="px-6 py-3 border border-gray-200 rounded-xl hover:bg-gray-50 transition"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="flex-1 bg-[#6C63FF] text-white px-6 py-3 rounded-xl hover:bg-[#4A3F8A] transition"
          >
            Register Asset
          </button>
        </div>
      </form>
    </div>
  );
}
import { useState } from 'react';
import { Plus, Edit, Trash2, Users } from 'lucide-react';

export default function Departments() {
  const [departments] = useState([
    { id: 1, name: 'Engineering', head: 'Amit Patel', employeeCount: 45, status: 'Active' },
    { id: 2, name: 'Marketing', head: 'Sneha Reddy', employeeCount: 28, status: 'Active' },
    { id: 3, name: 'Human Resources', head: 'Priya Sharma', employeeCount: 12, status: 'Active' },
    { id: 4, name: 'Finance', head: 'Rahul Singh', employeeCount: 18, status: 'Active' },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-dark">Department Management</h1>
          <p className="text-gray-500">Manage departments and assign heads</p>
        </div>
        <button className="bg-primary text-white px-4 py-2 rounded-xl flex items-center gap-2 hover:bg-secondary transition">
          <Plus className="w-4 h-4" /> Add Department
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {departments.map((dept) => (
          <div key={dept.id} className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-semibold text-dark">{dept.name}</h3>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-sm text-gray-500">Head: {dept.head}</span>
                </div>
              </div>
              <span className="px-2 py-1 bg-success/10 text-success text-xs font-medium rounded-full">
                {dept.status}
              </span>
            </div>
            
            <div className="flex items-center gap-2 mt-4 text-sm">
              <Users className="w-4 h-4 text-gray-400" />
              <span className="text-gray-600">{dept.employeeCount} employees</span>
            </div>

            <div className="flex gap-2 mt-4 pt-4 border-t border-gray-100">
              <button className="flex-1 text-sm text-gray-500 hover:text-primary hover:bg-primary/5 px-3 py-1 rounded-lg transition">
                <Edit className="w-4 h-4 inline mr-1" /> Edit
              </button>
              <button className="flex-1 text-sm text-gray-500 hover:text-red-500 hover:bg-red-50 px-3 py-1 rounded-lg transition">
                <Trash2 className="w-4 h-4 inline mr-1" /> Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
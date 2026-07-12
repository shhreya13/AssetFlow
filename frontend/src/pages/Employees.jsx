import { useState } from 'react';
import { Search, Users, Mail, User, Shield, MoreVertical } from 'lucide-react';

export default function Employees() {
  const [searchTerm, setSearchTerm] = useState('');

  const employees = [
    { id: 1, name: 'Amit Patel', email: 'amit@company.com', department: 'Engineering', role: 'Department Head', status: 'Active' },
    { id: 2, name: 'Priya Sharma', email: 'priya@company.com', department: 'HR', role: 'Employee', status: 'Active' },
    { id: 3, name: 'Raj Kumar', email: 'raj@company.com', department: 'Marketing', role: 'Asset Manager', status: 'Active' },
    { id: 4, name: 'Sneha Reddy', email: 'sneha@company.com', department: 'Engineering', role: 'Employee', status: 'Active' },
    { id: 5, name: 'Vikram Singh', email: 'vikram@company.com', department: 'Finance', role: 'Employee', status: 'Inactive' },
  ];

  const filteredEmployees = employees.filter(emp =>
    emp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    emp.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    emp.department.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-dark">Employee Directory</h1>
          <p className="text-gray-500">Manage employees and roles</p>
        </div>
        <button className="bg-primary text-white px-4 py-2 rounded-xl flex items-center gap-2 hover:bg-secondary transition whitespace-nowrap">
          <Users className="w-4 h-4" /> Add Employee
        </button>
      </div>

      <div className="flex-1 relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
        <input
          type="text"
          placeholder="Search employees by name, email, or department..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-200">
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Name</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Email</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Department</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Role</th>
                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Status</th>
                <th className="text-right px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredEmployees.map((emp) => (
                <tr key={emp.id} className="border-b border-gray-100 hover:bg-gray-50 transition">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                        <User className="w-5 h-5 text-primary" />
                      </div>
                      <span className="font-medium text-dark">{emp.name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">{emp.email}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{emp.department}</td>
                  <td className="px-6 py-4">
                    <span className="flex items-center gap-1 text-sm">
                      <Shield className="w-4 h-4 text-gray-400" />
                      {emp.role}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${emp.status === 'Active' ? 'bg-success/10 text-success' : 'bg-gray-100 text-gray-500'}`}>
                      {emp.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="p-1 hover:bg-gray-100 rounded-lg transition">
                      <MoreVertical className="w-4 h-4 text-gray-500" />
                    </button>
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
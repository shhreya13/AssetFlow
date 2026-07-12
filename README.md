# AssetFlow

## Enterprise Asset & Resource Management System

AssetFlow is a centralized ERP platform designed to simplify how organizations register, allocate, monitor, and maintain physical assets and shared resources.

The system replaces manual spreadsheets and paper-based tracking with a secure, role-based web application that provides complete visibility into asset lifecycles, resource bookings, maintenance workflows, audits, and operational analytics.

---

## Problem Statement

Organizations often struggle to efficiently manage assets such as laptops, furniture, vehicles, equipment, and meeting rooms due to fragmented tracking systems.

AssetFlow solves this by providing:

- Centralized asset management
- Role-based workflows
- Resource booking with conflict prevention
- Asset allocation and transfer management
- Maintenance approval workflow
- Asset audit management
- Notifications and activity logs
- Operational dashboards and analytics

---

## Features

### Authentication
- Secure Login
- Employee Signup
- Forgot Password
- Role-Based Access Control (RBAC)

### Dashboard
- Assets Available
- Assets Allocated
- Active Bookings
- Maintenance Today
- Pending Transfers
- Upcoming & Overdue Returns

### Organization Setup
- Department Management
- Asset Categories
- Employee Directory
- Role Assignment

### Asset Management
- Register Assets
- Asset Directory
- QR/Asset Tag Search
- Asset Lifecycle Tracking
- Asset History

### Asset Allocation
- Allocate Assets
- Transfer Requests
- Return Workflow
- Conflict Detection
- Overdue Return Tracking

### Resource Booking
- Calendar View
- Slot Booking
- Overlap Validation
- Booking Status Tracking

### Maintenance
- Raise Maintenance Request
- Approval Workflow
- Technician Assignment
- Maintenance History

### Asset Audit
- Audit Cycle Management
- Auditor Assignment
- Asset Verification
- Discrepancy Reports

### Reports & Analytics
- Asset Utilization
- Maintenance Reports
- Department Allocation Summary
- Resource Booking Heatmap
- Export Reports

### Notifications & Activity Logs
- Asset Notifications
- Booking Notifications
- Maintenance Notifications
- Audit Notifications
- Complete Activity History

---

## User Roles

### Admin
- Manage Departments
- Manage Asset Categories
- Employee Directory
- Assign Roles
- View Analytics

### Asset Manager
- Register Assets
- Allocate Assets
- Approve Transfers
- Approve Maintenance
- Manage Returns

### Department Head
- View Department Assets
- Approve Transfers
- Book Shared Resources

### Employee
- View Assigned Assets
- Book Resources
- Raise Maintenance Requests
- Request Transfers
- Initiate Asset Returns

---

## Asset Lifecycle

Available

↓

Allocated

↓

Reserved

↓

Under Maintenance

↓

Available

or

Lost / Retired / Disposed

---

## Technology Stack

### Frontend
- React
- Tailwind CSS

### Backend
- FastAPI
- SQLAlchemy

### Database
- SQLite

### Version Control
- Git
- GitHub

---

## Project Structure

```
AssetFlow/
│
├── frontend/
│
├── backend/
│   ├── app/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── database/
│   ├── docs/
│   └── mock_data/
│
├── assets/
│
└── README.md
```

---

## Team

| Member | Responsibility |
|---------|---------------|
| Shreya | Project Setup, Git, Documentation, Mock Data |
| Navya | Backend Development |
| Sujithra | Frontend Development |
| Darshini | UI/UX, Testing & API Integration |

---

## Current Status

- ✅ Repository Created
- ✅ Project Structure Initialized
- ✅ Mock Data Added
- ✅ API Documentation Created
- ✅ Database Schema Prepared
- 🚧 Backend Development In Progress
- 🚧 Frontend Development In Progress

---

## Future Enhancements

- QR Code Asset Scanning
- Smart Asset Recommendation
- Predictive Maintenance
- Email Notifications
- PDF Report Export
- Advanced Analytics Dashboard

---

## License

This project is developed as part of a hackathon and is intended for educational and demonstration purposes.

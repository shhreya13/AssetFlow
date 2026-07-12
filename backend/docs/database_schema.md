# AssetFlow Database Schema

## Overview

The database is designed to manage users, departments, assets, bookings, maintenance, audits, notifications, and activity logs.

---

# Users

| Field | Type |
|--------|------|
| id | Integer (PK) |
| name | String |
| email | String (Unique) |
| password | String (Hashed) |
| role | Enum (Admin, Asset Manager, Department Head, Employee) |
| department_id | FK -> Departments |
| status | Active / Inactive |

---

# Departments

| Field | Type |
|--------|------|
| id | Integer (PK) |
| name | String |
| head_id | FK -> Users |
| parent_department | FK -> Departments (Optional) |
| status | Active / Inactive |

---

# Asset Categories

| Field | Type |
|--------|------|
| id | Integer (PK) |
| name | String |
| description | String |

---

# Assets

| Field | Type |
|--------|------|
| id | Integer (PK) |
| asset_tag | String (Unique) |
| name | String |
| category_id | FK -> Asset Categories |
| serial_number | String |
| acquisition_date | Date |
| acquisition_cost | Decimal |
| condition | String |
| location | String |
| status | Available / Allocated / Reserved / Under Maintenance / Lost / Retired / Disposed |
| shared_bookable | Boolean |

---

# Asset Allocations

| Field | Type |
|--------|------|
| id | Integer (PK) |
| asset_id | FK -> Assets |
| employee_id | FK -> Users |
| allocated_date | Date |
| expected_return_date | Date |
| returned_date | Date |
| status | Active / Returned / Overdue |

---

# Transfer Requests

| Field | Type |
|--------|------|
| id | Integer (PK) |
| asset_id | FK -> Assets |
| requested_by | FK -> Users |
| approved_by | FK -> Users |
| status | Requested / Approved / Rejected |

---

# Resource Bookings

| Field | Type |
|--------|------|
| id | Integer (PK) |
| resource_id | FK -> Assets |
| booked_by | FK -> Users |
| start_time | DateTime |
| end_time | DateTime |
| status | Upcoming / Ongoing / Completed / Cancelled |

---

# Maintenance Requests

| Field | Type |
|--------|------|
| id | Integer (PK) |
| asset_id | FK -> Assets |
| reported_by | FK -> Users |
| issue | Text |
| priority | Low / Medium / High |
| status | Pending / Approved / Rejected / In Progress / Resolved |
| assigned_to | String |

---

# Audit Cycles

| Field | Type |
|--------|------|
| id | Integer (PK) |
| department_id | FK -> Departments |
| start_date | Date |
| end_date | Date |
| status | Open / Closed |

---

# Audit Records

| Field | Type |
|--------|------|
| id | Integer (PK) |
| audit_cycle_id | FK -> Audit Cycles |
| asset_id | FK -> Assets |
| verification_status | Verified / Missing / Damaged |

---

# Notifications

| Field | Type |
|--------|------|
| id | Integer (PK) |
| user_id | FK -> Users |
| message | String |
| is_read | Boolean |
| created_at | DateTime |

---

# Activity Logs

| Field | Type |
|--------|------|
| id | Integer (PK) |
| user_id | FK -> Users |
| action | String |
| timestamp | DateTime |

---

# Entity Relationships

- One Department has many Users.
- One Department has many Assets.
- One Asset Category has many Assets.
- One Asset can have many Allocation records over time.
- One Asset can have many Maintenance Requests.
- One Asset can have many Resource Bookings.
- One Audit Cycle contains many Audit Records.
- One User can receive many Notifications.
- One User can perform many Activity Log actions.
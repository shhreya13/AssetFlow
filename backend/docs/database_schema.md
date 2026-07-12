# AssetFlow Database Schema

## Users
- id
- name
- email
- password
- role (Admin, Asset Manager, Department Head, Employee)
- department_id
- status

---

## Departments
- id
- name
- head_id
- parent_department
- status

---

## Asset Categories
- id
- name
- description

---

## Assets
- id
- asset_tag
- name
- category_id
- serial_number
- acquisition_date
- acquisition_cost
- condition
- location
- status
- shared_bookable

---

## Asset Allocations
- id
- asset_id
- employee_id
- allocated_date
- expected_return
- returned_date
- status

---

## Resource Bookings
- id
- resource_id
- booked_by
- start_time
- end_time
- status

---

## Maintenance Requests
- id
- asset_id
- issue
- priority
- status
- assigned_to

---

## Audit Cycles
- id
- title
- department
- start_date
- end_date
- status

---

## Notifications
- id
- user_id
- message
- read
- created_at

---

## Activity Logs
- id
- user
- action
- timestamp

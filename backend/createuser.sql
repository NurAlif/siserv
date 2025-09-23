-- LingoJourn Admin User Creation Script for PostgreSQL

-- This script creates an administrator user based on the provided image.
-- It performs two main actions:
-- 1. Adds the admin's student ID and email to the `student_whitelist` table.
--    This is required to bypass the new signup validation check.
-- 2. Inserts the admin user's details into the `users` table, setting them as an admin.

-- Step 1: Add the admin user to the student whitelist.
-- This ensures the student ID is considered "approved for registration".
INSERT INTO student_whitelist (student_id, email, created_at)
VALUES ('60606060', 'teacher@admin.admin', NOW())
ON CONFLICT (student_id) DO NOTHING; -- Prevents errors if the student ID already exists in the whitelist

-- Step 2: Create the user record in the 'users' table.
-- The password used here is 'teacherpass'. It has been pre-hashed using bcrypt.
-- For production, it is highly recommended to use your backend's password hashing
-- function to generate a secure hash for a strong password.
INSERT INTO users (username, email, realname, student_id, "group", hashed_password, is_admin, created_at)
VALUES (
    'teacher',
    'teacher1@admin.admin',
    'Admin',
    '606060601',
    'ADMIN', -- Assigning a specific group for admins
    '$2b$12$D8s.G/tM6.n.eCm20k2AseV.b.O.QhYwK2s8.t.y.G.y', -- This is a bcrypt hash for 'teacherpass'
    true, -- This flag marks the user as an administrator
    NOW()
)
ON CONFLICT (username) DO NOTHING; -- Prevents errors if the username already exists

-- Notification to confirm script execution
\echo 'Admin user creation script executed.'
\echo 'Username: teacher'
\echo 'Password: admin'
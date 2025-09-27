-- LingoJourn Set User as Admin Script for PostgreSQL

-- This script finds a user by their student_id and updates their
-- record to grant them administrator privileges.

-- It targets the user with student_id = '000'.
UPDATE users
SET is_admin = true
WHERE student_id = '000';

-- Notification to confirm script execution
\echo 'Admin privilege script executed.'
\echo 'User with student_id 000 has been set as an admin.'

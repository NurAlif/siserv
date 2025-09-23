INSERT INTO student_whitelist (student_id, email, created_at) VALUES
('000', '000@admin.com', NOW()),
('60234567', 'student2@example.com', NOW()),
('60345678', 'another.student@example.com', NOW()),
('60456789', 'test.user@example.com', NOW()),
('60567890', 'jane.doe@example.com', NOW())
ON CONFLICT (student_id) DO NOTHING;

-- Notification to confirm script execution
\echo 'Student whitelist population script executed.'
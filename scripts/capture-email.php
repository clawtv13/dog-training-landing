<?php
// Email Capture Backend - CleverDogMethod
// Saves emails to JSON file and triggers PDF delivery

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$data_file = '/root/.openclaw/workspace/.state/cleverdogmethod-emails.json';
$data_dir = dirname($data_file);

// Create directory if doesn't exist
if (!is_dir($data_dir)) {
    mkdir($data_dir, 0755, true);
}

// Get POST data
$input = json_decode(file_get_contents('php://input'), true);

if (!isset($input['email']) || !filter_var($input['email'], FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid email']);
    exit;
}

$email = strtolower(trim($input['email']));
$source = $input['source'] ?? 'unknown';
$page = $input['page'] ?? 'unknown';
$resource = $input['resource'] ?? 'none';
$timestamp = date('Y-m-d H:i:s');

// Load existing emails
$emails = [];
if (file_exists($data_file)) {
    $emails = json_decode(file_get_contents($data_file), true) ?? [];
}

// Check for duplicate
$is_duplicate = false;
foreach ($emails as $existing) {
    if ($existing['email'] === $email) {
        $is_duplicate = true;
        break;
    }
}

// Add new email
$entry = [
    'email' => $email,
    'source' => $source,
    'page' => $page,
    'resource' => $resource,
    'timestamp' => $timestamp,
    'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown'
];

$emails[] = $entry;

// Save
file_put_contents($data_file, json_encode($emails, JSON_PRETTY_PRINT));

// Trigger PDF delivery (async)
if (!$is_duplicate && $resource !== 'none') {
    exec("python3 /root/.openclaw/workspace/scripts/send-pdf-email.py '$email' '$resource' > /dev/null 2>&1 &");
}

// Response
echo json_encode([
    'success' => true,
    'message' => 'Email captured',
    'is_new' => !$is_duplicate
]);
?>

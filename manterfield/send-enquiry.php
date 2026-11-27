<?php
/**
 * Manterfield Building & Roofing - website enquiry form.
 *
 * The Contact page posts the form here. This script checks the message and
 * emails it to the office. Nothing is stored on the website.
 *
 * Upload next to index.html in public_html (cPanel hosting runs PHP by default).
 * Change the three settings below if the email addresses ever change.
 */

// Where enquiries are delivered
const TO_ADDRESS = 'manterfield1@btinternet.com';
// The "from" address on the email. Use an address at your own domain, and create it
// in cPanel > Email Accounts (or Forwarders) so mail providers trust the message.
const FROM_ADDRESS = 'enquiries@manterfieldbuilders.co.uk';
const FROM_NAME = 'Manterfield Website';

// Spam protection
const MAX_PER_HOUR_PER_IP = 5;     // enquiries one visitor can send per hour
const MIN_SECONDS_ON_PAGE = 3;     // a real person takes longer than this to fill the form in

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

function reply(int $status, array $body): void
{
    http_response_code($status);
    echo json_encode($body);
    exit;
}

function clean(string $value, int $max): string
{
    // Strip control characters (blocks email header injection) and trim to length
    $value = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $value) ?? '';
    return mb_substr(trim($value), 0, $max);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    reply(405, ['ok' => false, 'error' => 'POST only']);
}

// Honeypot: real visitors never see or fill this field in
if (trim((string)($_POST['website'] ?? '')) !== '') {
    reply(200, ['ok' => true]); // pretend success so bots don't retry
}

$elapsed = (int)($_POST['elapsed'] ?? 0);
if ($elapsed > 0 && $elapsed < MIN_SECONDS_ON_PAGE * 1000) {
    reply(200, ['ok' => true]);
}

$name = clean((string)($_POST['name'] ?? ''), 100);
$email = clean((string)($_POST['email'] ?? ''), 150);
$phone = clean((string)($_POST['phone'] ?? ''), 40);
$service = clean((string)($_POST['service'] ?? ''), 60);
$subject = clean((string)($_POST['subject'] ?? ''), 120);
$message = trim(preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', (string)($_POST['message'] ?? '')) ?? '');
$message = mb_substr($message, 0, 5000);

if ($name === '' || $message === '') {
    reply(422, ['ok' => false, 'error' => 'Please fill in your name and message.']);
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    reply(422, ['ok' => false, 'error' => 'Please enter a valid email address so we can reply.']);
}
// Messages that are mostly links are almost always spam
if (preg_match_all('~https?://~i', $message) > 2) {
    reply(422, ['ok' => false, 'error' => 'Please remove the links from your message.']);
}

// Rate limit per visitor (kept in the server's temp folder, nothing personal is stored)
$ipHash = hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . date('Y-m-d-H'));
$stateFile = sys_get_temp_dir() . '/mfd-enquiry-' . $ipHash . '.count';
$count = is_file($stateFile) ? (int)file_get_contents($stateFile) : 0;
if ($count >= MAX_PER_HOUR_PER_IP) {
    reply(429, ['ok' => false, 'error' => 'Too many messages just now. Please call us on 01226 781344.']);
}

$title = $subject !== '' ? $subject : 'Website enquiry' . ($service !== '' ? ' - ' . $service : '');
$lines = [
    'A new enquiry was sent from the Manterfield website.',
    '',
    'Name:    ' . $name,
    'Email:   ' . $email,
    'Phone:   ' . ($phone !== '' ? $phone : '(not given)'),
    'Service: ' . ($service !== '' ? $service : '(not chosen)'),
    '',
    'Message:',
    $message,
    '',
    '-- Reply to this email to answer ' . $name . ' directly.',
];
$body = implode("\r\n", $lines);

$encodedFrom = '=?UTF-8?B?' . base64_encode(FROM_NAME) . '?= <' . FROM_ADDRESS . '>';
$headers = [
    'From: ' . $encodedFrom,
    'Reply-To: ' . $email,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: Manterfield website',
];
$encodedSubject = '=?UTF-8?B?' . base64_encode('[Website] ' . $title) . '?=';

$sent = @mail(TO_ADDRESS, $encodedSubject, $body, implode("\r\n", $headers), '-f' . FROM_ADDRESS);
if (!$sent) {
    reply(500, ['ok' => false, 'error' => 'Sorry, your message could not be sent. Please call us on 01226 781344.']);
}

@file_put_contents($stateFile, (string)($count + 1), LOCK_EX);
reply(200, ['ok' => true]);

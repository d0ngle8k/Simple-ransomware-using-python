<?php
// Step 1: Enable error reporting for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);


// Step 2: Set the header for JSON content type
header('Content-Type: application/json'); 


// Step 3: Include database connection
require_once '../db.php'; 


// Step 4: Check if machine_id is provided and fetch stop_signal from database
if (isset($_GET['machine_id'])) {
    $machine_id = $_GET['machine_id'];
    $stmt = $pdo->prepare("SELECT stop_signal FROM machine_keys WHERE machine_id = :machine_id");
    $stmt->bindParam(':machine_id', $machine_id);
    
    // Step 4.1: Execute the prepared statement and fetch result
    if ($stmt->execute()) {
        $result = $stmt->fetch(PDO::FETCH_ASSOC);
        echo json_encode(['stop_signal' => $result['stop_signal'] ?? 0]);
    } else {
        // Step 4.2: Include error information if execute fails
        echo json_encode(['error' => $stmt->errorInfo()]);
    }
} else {
    // Step 4.3: Handle case where machine_id is not provided
    echo json_encode(['error' => 'Machine ID not provided.']);
}
?>


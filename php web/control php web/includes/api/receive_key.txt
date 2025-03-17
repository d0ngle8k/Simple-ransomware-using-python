<?php
// Step 1: Include the database connection file
require_once '../db.php';


// Step 2: Set the header for JSON content type
header('Content-Type: application/json');


// Step 3: Ensure the request method is POST
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Step 3.1: Retrieve data from the POST request
    $json = file_get_contents('php://input');
    $data = json_decode($json, true);
    
    // Step 3.2: Extract machine_id and encryption_key from the POST data
    $machine_id = $data['machine_id'] ?? '';
    $encryption_key = $data['encryption_key'] ?? '';


    // Step 3.3: Prepare the SQL statement to insert the data into the database
    $stmt = $pdo->prepare("INSERT INTO machine_keys (machine_id, encryption_key) VALUES (:machine_id, :encryption_key)");
    
    // Step 3.4: Bind the parameters
    $stmt->bindParam(':machine_id', $machine_id);
    $stmt->bindParam(':encryption_key', $encryption_key);


    // Step 3.5: Execute the statement and respond with the appropriate message
    if ($stmt->execute()) {
        echo json_encode(['success' => true, 'message' => 'Data received successfully']);
    } else {
        echo json_encode(['success' => false, 'message' => 'An error occurred']);
    }
} else {
    // Step 3.6: Respond with an error message if the request method is not POST
    echo json_encode(['success' => false, 'message' => 'Invalid request method']);
}
?>


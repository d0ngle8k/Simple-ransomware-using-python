<?php
// Step 1: Include the database connection file
require_once '../db.php';


// Step 2: Initialize response array
$response = ['success' => false];


// Step 3: Check if machine_id is set in the POST request
if (isset($_POST['machine_id'])) {
    $machine_id = $_POST['machine_id'];


    // Step 3.1: Try to execute the SQL update statement
    try {
        // Step 3.2: Prepare the SQL statement to update stop_signal
        $stmt = $pdo->prepare("UPDATE machine_keys SET stop_signal = 1 WHERE machine_id = :machine_id");


        // Step 3.3: Bind the machine_id parameter
        $stmt->bindParam(':machine_id', $machine_id);


        // Step 3.4: Execute the statement
        if ($stmt->execute()) {
            // Step 3.5: Check if any rows were updated
            if ($stmt->rowCount() > 0) {
                $response['success'] = true;
            } else {
                $response['error'] = 'No rows updated. Check if machine_id exists.';
            }
        } else {
            $response['error'] = 'Database update failed.';
        }
    } catch (PDOException $e) {
        // Step 3.6: Handle any PDO exceptions
        $response['error'] = 'PDOException: ' . $e->getMessage();
    }
} else {
    // Step 4: Handle missing machine_id in the POST request
    $response['error'] = 'Machine ID not provided.';
}


// Step 5: Return the response as JSON
echo json_encode($response);
?>


<?php
// Step 1: Start session and check if already logged in
session_start();


if (isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === true) {
    header("location: dashboard.php");
    exit;
}


// Step 2: Include database connection
require_once "../includes/db.php";


$username = $password = "";
$err = "";


// Step 3: Process login form submission
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim(filter_input(INPUT_POST, "username", FILTER_SANITIZE_STRING));
    $sql = "SELECT user_id, username, password FROM users WHERE username = :username";


    if ($stmt = $pdo->prepare($sql)) {
        $stmt->bindParam(":username", $username, PDO::PARAM_STR);


        if ($stmt->execute()) {
            if ($stmt->rowCount() == 1) {
                if ($row = $stmt->fetch()) {
                    $hashed_password = $row["password"];


                    if (password_verify(filter_input(INPUT_POST, "password", FILTER_SANITIZE_STRING), $hashed_password)) {
                        $_SESSION["loggedin"] = true;
                        $_SESSION["user_id"] = $row["user_id"];
                        $_SESSION["username"] = $row["username"];
                        header("location: dashboard.php");
                        exit;
                    } else {
                        $err = "Invalid password.";
                    }
                }
            } else {
                $err = "Invalid username.";
            }
        } else {
            $err = "Something went wrong. Please try again later.";
        }
        unset($stmt);
    }
    unset($pdo);
}
?>


<!-- Step 4: HTML Sections -->
<!DOCTYPE html>
<html lang="en">
<head>
    
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enter the Matrix</title>
    <link rel="stylesheet" href="../assets/css/login.css">  <!-- Link to the CSS file for styling -->
</head>
<body>
    <div class="hacker-login">
        <h2>Login</h2>
        <form action="<?= htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
            <div class="hacker-input">
                <label>Username</label>
                <input type="text" name="username" value="<?= $username; ?>" required>
            </div>
            <div class="hacker-input">
                <label>Password</label>
                <input type="password" name="password" required>
            </div>
            <div class="hacker-button">
                <input type="submit" value="Login">
            </div>
            <?php if (!empty($err)) {
                echo '<div class="error">' . htmlspecialchars($err) . '</div>';
            } ?>
        </form>
    </div>


    <script src="../assets/js/login.js"></script>
</body>
</html>


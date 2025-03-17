<?php
// Step 1 : Logout Sessions
session_start();
$_SESSION = array();
session_destroy();
header("location: login.php");
exit;
?>

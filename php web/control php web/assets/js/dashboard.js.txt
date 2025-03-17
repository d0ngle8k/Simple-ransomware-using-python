// Step 1: Logging the machine ID to the console to verify which machine is targeted.
function sendKillSignal(machineId) {
    console.log("Sending kill signal to machine ID:", machineId);
    if (confirm("Are you sure you want to send a self-destruct signal to machine ID: " + machineId + "?")) {
        $.post('../includes/api/receive_kill_signal.php', { machine_id: machineId })
            .done(function(response) {
                var data = JSON.parse(response);
                
                if (data.success) {
                    alert('Self-destruct signal sent successfully to machine ID: ' + machineId);
                    location.reload();
                } else {
                    alert('Failed to send self-destruct signal.');
                }
            })
            .fail(function() {
                alert('Error sending self-destruct signal.');
            });
    }
}


  // Step 2:  Attach a click event handler to the element with the ID 'sidebarCollapse'.
$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
});


<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $mac = escapeshellarg($_POST['mac']);
    $dhcp_version = escapeshellarg($_POST['dhcp_version']);

    $command = escapeshellcmd("python3 network_config.py $mac $dhcp_version");
    $output = shell_exec($command);

    $result = json_decode($output, true);

    echo "<h2>Network Configuration Result:</h2>";

    if (isset($result["error"])) {
        echo "<p style='color: red;'><strong>Error:</strong> " . htmlspecialchars($result["error"]) . "</p>";
    } else {
        echo "<ul>";
        echo "<li><strong>MAC Address:</strong> " . htmlspecialchars($result["mac_address"]) . "</li>";
        echo "<li><strong>Assigned IP:</strong> " . htmlspecialchars($result["ip"]) . "</li>";
        echo "<li><strong>DHCP Version:</strong> " . htmlspecialchars($result["version"]) . "</li>";
        echo "<li><strong>Lease Time:</strong> " . htmlspecialchars($result["lease_time"]) . " seconds</li>";
        echo "<li><strong>Subnet:</strong> " . htmlspecialchars($result["subnet"]) . "</li>";
        echo "</ul>";
    }
}

?>

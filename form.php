<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Assignment 8</title>
</head>

<body>
	<h1>Network Simulator Tool</h1>
	<form action="process.php" method="post">
        <label>MAC Address:</label>
        <input type="text" name="mac" required><br>
        
        <label>DHCP Version:</label>
        <select name="dhcp_version">
            <option value="DHCPv4">DHCPv4</option>
            <option value="DHCPv6">DHCPv6</option>
        </select><br>

        <input type="submit" value="Request IP">
    </form>
</body>

</html>
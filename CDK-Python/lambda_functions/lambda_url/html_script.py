html_1 = """
<html>
<body>
    <form action="/submit" method="post">
        <label for="name">Instance Name:</label>
        <select id="name" name="name">
"""
html_2 = """
        </select>
        <input type="submit" value="Start EC2" onclick="startEC2(event)">
        <input type="submit" value="Stop EC2" onclick="stopEC2(event)">

    </form>
    
    <script>
    function startEC2(event) {
        event.preventDefault(); // Prevent form submission
        
        var name = document.getElementById("name").value;

        fetch('/start-ec2', {
            method: 'POST',
            body: JSON.stringify({ instance_name: name })
        })
        .then(response => {
            if (response.ok) {
                alert("EC2 instance start requested!");
            } else {
                alert("Failed to start EC2 instance!");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while starting the EC2 instance!");
        });
    }

    function stopEC2(event) {
        event.preventDefault(); // Prevent form submission
        
        var name = document.getElementById("name").value;
        
        fetch('/stop-ec2', {
            method: 'POST',
            body: JSON.stringify({ instance_name: name })
        })
        .then(response => {
            if (response.ok) {
                alert("EC2 instance stopped successfully!");
            } else {
                alert("Failed to stop EC2 instance!");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while stopping the EC2 instance!");
        });
    }
    </script>
</body>
</html>
"""
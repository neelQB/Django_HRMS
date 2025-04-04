
<script>
        function updateProgress(hoursWorked) {
            const totalHours = 8.5;
            const percentage = Math.min((hoursWorked / totalHours) * 100, 100);
            const circumference = 314;
            const offset = circumference - (percentage / 100) * circumference;
            document.querySelector(".progress-ring-progress").style.strokeDashoffset = offset;
            document.getElementById("progress-text").textContent = hoursWorked.toFixed(2) + " hrs";
        }

        // Example: Update dynamically (change the value to test)
        updateProgress(5.75); // Change this value to update the progress dynamically
    </script>
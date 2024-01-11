document.addEventListener('DOMContentLoaded', function() {
    const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    let dailyCalories = [];

    daysOfWeek.forEach(day => {
        const table = document.getElementById(`table-${day}`);
        if (table) {
            let totalCalories = 0;
            const calorieCells = table.querySelectorAll('td:nth-child(3)'); // Assuming calories are in the third column
            calorieCells.forEach(cell => {
                totalCalories += parseInt(cell.textContent) || 0;
            });
            dailyCalories.push(totalCalories);
        } else {
            dailyCalories.push(0); // If no data for a day, push 0
        }
    });

    const averageCalories = 2500;
    const ctx = document.getElementById('calorieChart').getContext('2d');
    const calorieChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: daysOfWeek,
            datasets: [{
                label: 'Daily Calories',
                data: dailyCalories,
                backgroundColor: 'skyblue'
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                annotation: {
                    annotations: {
                        line1: {
                            type: 'line',
                            yMin: averageCalories,
                            yMax: averageCalories,
                            borderColor: 'black',
                            borderWidth: 2,
                            label: {
                                content: 'Average Caloric Intake',
                                enabled: true,
                                position: 'start'
                            }
                        }
                    }
                }
            }
        }
    });
});

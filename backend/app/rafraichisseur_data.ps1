
$taskName = "Rafraichir la data ( client meteo france )"
$scriptPath = "C:\Users\Utilisateur\Documents\GitHub\b16\b16_mateo\main.py"
$pythonPath = "C:\Users\Utilisateur\Documents\GitHub\b16\b16_mateo\main.py"

# Vérifie si la tâche existe déjà
$taskExists = Get-ScheduledTask | Where-Object { $_.TaskName -eq $taskName }

if ($taskExists) {
    Write-Host "La tâche '$taskName' existe déjà."
} else {
    # Crée la tâche planifiée
    $action = New-ScheduledTaskAction -Execute $pythonPath -Argument "-u $scriptPath"
    $trigger = New-ScheduledTaskTrigger -Daily -At 12am
    $settings = New-ScheduledTaskSettingsSet
    $principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount -RunLevel Highest

    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal
    Write-Host "La tâche '$taskName' a été créée."
}
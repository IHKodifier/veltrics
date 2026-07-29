# gcp_cloud_control.ps1
# On-demand script to start or stop GCP Cloud SQL instances to minimize infrastructure costs.
# Usage:
#   .\scripts\gcp_cloud_control.ps1 -Action start -InstanceName veltrics-db-staging
#   .\scripts\gcp_cloud_control.ps1 -Action stop -InstanceName veltrics-db-staging

param (
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "stop", "status")]
    [string]$Action,

    [Parameter(Mandatory=$false)]
    [string]$InstanceName = "veltrics-db-staging"
)

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " GCP Cloud SQL Cost Control Utility " -ForegroundColor Cyan
Write-Host " Target Instance: $InstanceName " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

switch ($Action.ToLower()) {
    "start" {
        Write-Host "Starting GCP Cloud SQL instance '$InstanceName'..." -ForegroundColor Green
        gcloud sql instances patch $InstanceName --activation-policy=ALWAYS
        Write-Host "Cloud SQL instance '$InstanceName' is now RUNNING." -ForegroundColor Green
    }
    "stop" {
        Write-Host "Stopping GCP Cloud SQL instance '$InstanceName' to pause billing..." -ForegroundColor Yellow
        gcloud sql instances patch $InstanceName --activation-policy=NEVER
        Write-Host "Cloud SQL instance '$InstanceName' has been STOPPED. Billing paused." -ForegroundColor Yellow
    }
    "status" {
        Write-Host "Checking activation status for '$InstanceName'..." -ForegroundColor White
        gcloud sql instances describe $InstanceName --format="value(settings.activationPolicy,state)"
    }
}

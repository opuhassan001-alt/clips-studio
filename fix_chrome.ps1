# Kill all Chrome processes
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Remove corrupted GPUCache and ShaderCache
$gpuCache = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\GPUCache"
$shaderCache = "$env:LOCALAPPDATA\Google\Chrome\User Data\ShaderCache"

if (Test-Path $gpuCache) {
    Remove-Item "$gpuCache\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "GPU Cache cleared successfully."
}

if (Test-Path $shaderCache) {
    Remove-Item "$shaderCache\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Shader Cache cleared successfully."
}

Start-Sleep -Seconds 1
# Launch Chrome fresh with GPU rasterization flag safe
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" "https://business.facebook.com"
Write-Host "Chrome restarted successfully."

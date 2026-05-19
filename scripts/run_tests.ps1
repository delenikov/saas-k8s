param(
    [string]$BASE_URL = "http://127.0.0.1:8080",
    [string]$PLATFORM = "local"
)

New-Item -ItemType Directory -Force -Path results | Out-Null

# $sizes = @(64, 128, 256, 512, 1000)
# $usersList = @(10, 50, 100, 500)

$sizes = @(10)
$usersList = @(1, 10, 50, 100, 250, 500, 1000)

foreach ($SIZE in $sizes) {
    foreach ($USERS in $usersList) {

        $OUT = "results/${PLATFORM}_size${SIZE}_users${USERS}.json"

        Write-Host "========================================"
        Write-Host "Running:"
        Write-Host "Platform: $PLATFORM"
        Write-Host "Size: $SIZE"
        Write-Host "Users: $USERS"
        Write-Host "========================================"

        $env:BASE_URL = $BASE_URL
        $env:SIZE = $SIZE
        $env:USERS = $USERS
        $env:DURATION = "1m"

        k6 run `
            --summary-export $OUT `
            loadtest/test.js
    }
}
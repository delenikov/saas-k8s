param(
    [string]$BASE_URL = "http://127.0.0.1:8080",
    [string]$PLATFORM = "local"
)

New-Item -ItemType Directory -Force -Path results | Out-Null

$TEST_CASES = @(
    @{ Name="TC1"; Size=10; Users=1 },
    @{ Name="TC2"; Size=10; Users=5 },
    @{ Name="TC3"; Size=10; Users=10 },
    @{ Name="TC4"; Size=10; Users=25 },
    @{ Name="TC5"; Size=10; Users=50 },
    @{ Name="TC6"; Size=10; Users=100 },

    @{ Name="TC7"; Size=25; Users=1 },
    @{ Name="TC8"; Size=25; Users=5 },
    @{ Name="TC9"; Size=25; Users=10 },
    @{ Name="TC10"; Size=25; Users=25 },
    @{ Name="TC11"; Size=25; Users=50 },
    @{ Name="TC12"; Size=25; Users=100 },

    @{ Name="TC13"; Size=50; Users=1 },
    @{ Name="TC14"; Size=50; Users=5 },
    @{ Name="TC15"; Size=50; Users=10 },
    @{ Name="TC16"; Size=50; Users=25 },
    @{ Name="TC17"; Size=50; Users=50 },
    @{ Name="TC18"; Size=50; Users=100 },

    @{ Name="TC19"; Size=100; Users=1 },
    @{ Name="TC20"; Size=100; Users=5 },
    @{ Name="TC21"; Size=100; Users=10 },
    @{ Name="TC22"; Size=100; Users=25 },
    @{ Name="TC23"; Size=100; Users=50 },
    @{ Name="TC24"; Size=100; Users=100 },

    @{ Name="TC25"; Size=250; Users=1 },
    @{ Name="TC26"; Size=250; Users=5 },
    @{ Name="TC27"; Size=250; Users=10 },
    @{ Name="TC28"; Size=250; Users=25 },
    @{ Name="TC29"; Size=250; Users=50 },
    @{ Name="TC30"; Size=250; Users=100 },

    @{ Name="TC31"; Size=350; Users=1 },
    @{ Name="TC32"; Size=350; Users=5 },
    @{ Name="TC33"; Size=350; Users=10 },
    @{ Name="TC34"; Size=350; Users=25 },
    @{ Name="TC35"; Size=350; Users=50 },
    @{ Name="TC36"; Size=350; Users=100 },

    @{ Name="TC37"; Size=500; Users=1 },
    @{ Name="TC38"; Size=500; Users=5 },
    @{ Name="TC39"; Size=500; Users=10 },
    @{ Name="TC40"; Size=500; Users=25 },
    @{ Name="TC41"; Size=500; Users=50 },
    @{ Name="TC42"; Size=500; Users=100 }
)

foreach ($TEST in $TEST_CASES) {

    $NAME = $TEST.Name
    $SIZE = $TEST.Size
    $USERS = $TEST.Users

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

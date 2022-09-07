# A script to run various automation on rubato
function HelpText {
    $1 = $args[0]
    $tab="    "
    if ($PSBoundParameters.ContainsKey("1")) {
        Write-Output "Unknown argument: '$1'"
    } else {
        Write-Output "Usage: ./b [options]"
        Write-Output ""
        Write-Output "Options:"
        Write-Output "${tab}--help, -h: Show this help text"
        Write-Output "${tab}build, b: Build the project"
        Write-Output "${tab}${tab}force: Force a rebuild"
        Write-Output "${tab}demo, dem: Run the demos"
        Write-Output "${tab}delete, del: Delete the build directory"
        Write-Output "${tab}${tab}bin, b: Delete the binary files"
        Write-Output "${tab}${tab}c: Delete the c files"
        Write-Output "${tab}docs, doc: Start a live server of the documentation"
        Write-Output "${tab}${tab}clear, c: Clear the documentation build directory"
        Write-Output "${tab}${tab}save, s: Save the documentation build directory"
        Write-Output "${tab}lint, l: Run the linter"
        Write-Output "${tab}test, t: Run the testing flow"
        Write-Output "${tab}${tab}build, b: Build the project for testing"
        Write-Output "${tab}${tab}quick, q: Run the tests without force rebuilding"
        Write-Output "${tab}${tab}test, t: Run the tests without building"
        Write-Output "${tab}setup, s: Setup the project"
        Write-Output "${tab}precommit, pre: Run the precommit script"
        Write-Output "${tab}pypi: Build the project for pypi"
        Write-Output "${tab}publish-wheel, publish: Build and publish the wheel to pypi"
    }
}

function Delete {
    $1=$args[0]
    switch -Exact ($1) {
        "bin" {
            Write-Output "Deleting binary files..."
            cd rubato
            Get-ChildItem . -Include *.pyd -Recurse | Remove-Item
            Get-ChildItem . -Include *.so -Recurse | Remove-Item
            cd ..
        }
        "b" { Delete bin }
        "c" {
            Write-Output "Deleting c files..."
            cd rubato
            Get-ChildItem . -Include *.cpp -Exclude cdraw.cpp -Recurse | Remove-Item
            Get-ChildItem . -Include *.c -Recurse | Remove-Item
            cd ..
        }
        Default {
            Write-Output "Deleting build directory..."
            if (Test-Path -Path build) {
                Remove-Item build -Recurse
            }
            Delete bin
            Delete c
        }
    }
}

$ogdir=$pwd
$1=$args[0]
$2=$args[1]
cd $PSScriptRoot
switch -Exact ($1){
    "--help"{
        HelpText
    }
    "-h" {
        HelpText
    }
    "delete" {
        Delete $2
    }
    "del" {
        Delete $2
    }
    Default {
        HelpText $1
    }
}
cd $ogdir

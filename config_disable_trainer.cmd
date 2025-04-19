mkdir tmp
jq --indent 4 ".enable_trainer = false" conf/config.json > tmp\config.json
move /y tmp\config.json conf\config.json
pause

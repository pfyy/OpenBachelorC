mkdir tmp
jq --indent 4 ".enable_trainer = true" conf/config.json > tmp\config.json
move /y tmp\config.json conf\config.json
pause

mkdir tmp
jq --indent 4 ".use_su = false | .use_gadget = false" conf/config.json > tmp\config.json
move /y tmp\config.json conf\config.json
pause

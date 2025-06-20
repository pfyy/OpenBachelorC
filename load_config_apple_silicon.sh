mkdir -p tmp
jq --indent 4 ".use_su = false | .use_gadget = false" conf/config.json > tmp/config.json
mv tmp/config.json conf/config.json

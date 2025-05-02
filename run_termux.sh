frida -H 127.0.0.1:9443 -f com.hypergryph.arknights -l rel/native.js -P '{"proxy_url": "http://127.0.0.1:8443"}' -q --eternalize
frida -H 127.0.0.1:9443 -n 明日方舟 -l rel/java.js -P '{"proxy_url": "http://127.0.0.1:8443"}' -q --eternalize
frida -H 127.0.0.1:9443 -n 明日方舟 -l rel/extra.js -P '{"pause_deploy": true, "3x_speed": true, "vision": true, "vision_font_size": 22}' -q --eternalize

 #!/bin/sh
  
  cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
  chmod +x $BASE_DIR/target/etc/init.d/S41network-config
  cp $BASE_DIR/../custom-scripts/exemplo_html.py $BASE_DIR/target/usr/bin
  cp $BASE_DIR/../custom-scripts/S42server.sh $BASE_DIR/target/etc/init.d
  chmod +x $BASE_DIR/target/etc/init.d/S42server.sh

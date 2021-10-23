// boot network connection
n = NetAddr("127.0.0.1", 1234);
// set reply address
n.sendMsg("/replyTo", n.ip, 57120);
// function-name, path-to-csv, num-of-fields, percent-of-original, tag
n.sendMsg("/oversampling", "tuned_before_the_rain.dat", 6, 1, "'the'");
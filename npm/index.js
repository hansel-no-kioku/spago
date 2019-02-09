var binwrap = require("binwrap");
var path = require("path");

var packageInfo = require(path.join(__dirname, "package.json"));
var version = packageInfo.version;
var root = "https://github.com/spacchetti/spago/releases/download/"
         + version + ".0";

module.exports = binwrap({
  dirname: __dirname,
  binaries: [
    "spago"
  ],
  urls: {
    "darwin-x64": root + "/osx.tar.gz",
    "linux-x64": root + "/linux.tar.gz",
    "win32-x64": root + "/windows.tar.gz"
  }
});

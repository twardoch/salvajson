const esbuild = require("esbuild");

esbuild
  .build({
    entryPoints: ["./salvajson.src.js"], // Entry file
    outfile: "../src/salvajson/salvajson.js", // Updated output path
    bundle: true,
    platform: "node",
    format: "cjs",
    target: "es2020", // Changed from firefox134 to a more general ES version
    minify: true,
  })
  .then(() => {
    console.log("Bundling complete!");
  })
  .catch((err) => {
    console.error("Bundling failed:", err);
    process.exit(1);
  });

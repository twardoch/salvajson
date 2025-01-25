const esbuild = require('esbuild');

esbuild.build({
    entryPoints: ['./salvajson.src.js'], // Entry file
    outfile: '../salvajson/salvajson.js', // Output file in the Python package
    bundle: true,
    platform: 'node',
    format: 'cjs',
    target: 'firefox134',
    minify: true,
}).then(() => {
    console.log('Bundling complete!');
}).catch((err) => {
    console.error('Bundling failed:', err);
    process.exit(1);
});

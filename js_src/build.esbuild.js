const esbuild = require('esbuild');

esbuild.build({
    entryPoints: ['./salvajson.src.js'], // Entry file
    outfile: '../src/salvajson/salvajson.js', // Updated output path
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

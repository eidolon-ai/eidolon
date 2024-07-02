// webpack.config.cjs
const path = require('path')

module.exports = {
    entry: './src/index.ts',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist')
    },
    module: {
        rules: [
            {test: /\.json$/, type: 'json'},
            {
                test: /\.([cm]?ts|tsx)$/,
                loader: 'ts-loader',
                options: {
                    ignoreDiagnostics: [2538, 2532, 2322, 18048, 2769]
                }
            }
        ]
    },
    resolve: {
        extensions: ['.js', '.json', '.ts'],
        fallback: {
            "path": false,
            "util": false
        }
    },
    mode: 'development',
};

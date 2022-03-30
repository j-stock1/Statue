const path = require('path')
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
    entry: {
        //'app': '/sources/js/app.js',
        'script': '/sources/js/script.js'
    },
    output:{
        filename: '[name].js',
        path: path.join(__dirname,'static/js/')
    },
    optimization: {
    minimizer: [new TerserPlugin({
      extractComments: false,
    })],
  },
    mode: "production"
}
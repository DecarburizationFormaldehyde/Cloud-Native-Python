module.exports={
    mode: 'development',
    entry: "./static/main.js",
    output: {
        path: __dirname+"/static/build/",
        filename: "bundle.js"
    },
    devtool: 'eval-cheap-module-source-map',
    resolve: {
        extensions: ['.js', '.jsx']
    },
    module: {
        rules:[
            {
                test:/\.jsx?$/,
                exclude:/(node_modules)/,
                use:{
                    loader:'babel-loader',
                    options:{
                        presets:['@babel/preset-react']  // 更新为正确的预设名称
                    }
                }
            }
        ]
    }
}
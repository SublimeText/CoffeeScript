var parse = require('./parse-base64vlq-mappings/index.js');
var fs = require("fs");
// console.log(process.argv);
var mapFile = process.argv[2];
var row = process.argv[3];
var col = process.argv[4];
var map = fs.readFileSync(mapFile).toString();
// console.log(map);
var index = parse(JSON.parse(map).mappings);
var pos = undefined;
for(var i=0;i<index.length;i++){
    if (index[i].original.line > parseInt(row))
    {
        pos = index[i-1];
        break;
    }
    else{
        if (index[i].original.line == parseInt(row)){
            if (index[i].original.column >= parseInt(col)){
                pos = index[i];
            }
        }
        else{
            continue;
        }
    }
}
console.log(pos.generated.line,pos.generated.column)

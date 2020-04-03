
function getUsrCpuStat(){
	function takeNonWhitespace(arr){
		let final = []
		for(i in arr){
			if(arr[i]!= ''){
				final.push(arr[i])
			}
		}
		return final
	}
	let {spawnSync} = require("child_process")
	let gen_usage = spawnSync("mpstat").stdout.toString().trim().split("\n").slice(-2)
	
	let key = takeNonWhitespace(gen_usage.shift().trim().split(" "))
	let value = gen_usage.shift().trim()

	value = value.split("   ")

	let usage = {}
	for(i in key){
		if(i == 0){
			usage["Time"] = value[i]
			continue;
		}
		usage[key[i]] = value[i] + "%"
	}
	return usage
}

module.exports = getUsrCpuStat
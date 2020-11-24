

var jsonPath = document.getElementById("jsonPath")
var out = document.getElementById("output")
var env = document.getElementById("Env");


document.addEventListener('submit', async function ivy(e){
    e.preventDefault();

    return_val = await eel.chromeController(jsonPath.value.trim(), env.value)();
    

    if (Object.keys(return_val).length > 0) {
        var tbl = document.createElement("table")
        tbl.className = "u-full-width"
        var thead = document.createElement("thead")
        var tr = document.createElement("tr")
        var th1 = document.createElement("th")
        var th2 = document.createElement("th")
        var th3 = document.createElement("th")
        var tbody = document.createElement("tbody")
        th1.appendChild(document.createTextNode("Producer Name"))
        th2.appendChild(document.createTextNode("Consumer Name"))
        th3.appendChild(document.createTextNode("Action taken"))
        tr.appendChild(th1)
        tr.appendChild(th2)
        tr.appendChild(th3)
        thead.appendChild(tr)
        tbl.appendChild(thead)
        for (let [key, value] of Object.entries(return_val)){
            for (let [secondKey, val] of Object.entries(value)){ 
                val.forEach(element => {
                    var tg = document.createElement("tr")
                    var tp = document.createElement("td")
                    var tc = document.createElement("td")
                    var ts = document.createElement("td")
                    ts.appendChild(document.createTextNode(element))
                    tc.appendChild(document.createTextNode(secondKey))
                    tp.appendChild(document.createTextNode(key))
                    tg.appendChild(tp)
                    tg.appendChild(tc)
                    tg.appendChild(ts)
                    tbody.appendChild(tg) 
                });
            }
        }
        tbl.appendChild(tbody)
        out.appendChild(tbl)
    }
    
    
})
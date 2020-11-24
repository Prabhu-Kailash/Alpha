

var jsonPath = document.getElementById("jsonPath")
var out = document.getElementById("output")
var env = document.getElementById("Env");

document.addEventListener('contextmenu', event => event.preventDefault());


document.addEventListener('submit', async function rattle(e){
    e.preventDefault();

    return_val = await eel.magicWand(jsonPath.value.trim(), env.value)();
    

    if (Object.keys(return_val).length > 0) {
        
    }
    
    
})
var producer = document.getElementById("Producer");
var consumer = document.getElementById("Consumer");
var secondaryProducer = document.getElementById("SProducer");
var ssh = document.getElementById("UpdateSSH");
var dir = document.getElementById("UpdateDir");
var detailEmail = document.getElementById("DetailEmail");
var successEmail = document.getElementById("SuccessEmail");
var failureEmail = document.getElementById("FailEmail");
var routingChannel = document.getElementById("RCUpdate");
var detail_Email = document.getElementById("RDetailEmail");
var success_Email = document.getElementById("RSuccessEmail");
var failure_Email = document.getElementById("RFailEmail");
var authentication = document.getElementById("Auth");
var authCheck = document.getElementById("AuthCheck");
var pgp = document.getElementById("PGP");
var sign = document.getElementById("Signing");
var pgp_remove = document.getElementById("RPGP");
var sign_remove = document.getElementById("RSigning");
var sign_remove = document.getElementById("RSigning");
var producer_remove = document.getElementById("RProducer");
var consumer_remove = document.getElementById("RConsumer");
var env = document.getElementById("Env");
var fileRename = document.getElementById("UpdateFileRename");
var renameCheck = document.getElementById("FileRenameCheck");
var hold = document.getElementById("Hold");



document.addEventListener('submit', function anti_Dote(e){
    var rename;
    var auth;
    
    if(renameCheck.checked){
        rename = "Remove";
    } else {
        rename = fileRename.value;
    }

    if(authCheck.checked){
        auth = "Remove";
    } else {
        auth = authentication.value;
    }
    
    const antiDote = {
        
        "MainProducer" : producer.value.trim(),
        "SecondaryProducer" : secondaryProducer.value.trim(),
        "MainConsumer" : consumer.value.trim(),
        "HoldSetup" : "%s" % hold.checked,
        "UpdateSSH" : ssh.value.trim(),
        "UpdateDir" : dir.value.trim(),
        "UpdateFileRename" :  rename.trim(),
        "AddDetailEmail" : detailEmail.value.trim(),
        "AddSuccessEmail" : successEmail.value.trim(),
        "AddFailEmail" : failureEmail.value.trim(),
        "RemoveDetailEmail" : detail_Email.value.trim(),
        "RemoveSuccessEmail" : success_Email.value.trim(),
        "RemoveFailEmail" : failure_Email.value.trim(),
        "UpdateRC" : routingChannel.value.trim(),
        "UpdateSSHAuth" : auth.trim(),
        "UpdatePGPEncrypt" : pgp.value.trim(),
        "UpdatePGPSign" : sign.value.trim(),
        "RemovePGPEncrypt" : pgp_remove.value.trim(),
        "RemovePGPSign" : sign_remove.value.trim(),
        "RemoveConsumer" : consumer_remove.value.trim(),
        "RemoveProducer" : producer_remove.value.trim()
            
    };
    async function run(){
        message = document.createElement("p")
        return_val = await eel.validation(antiDote, env.value)();
        if (return_val != "Success. Output JSON file generated at ../Desktop/Builds/Reworks folder"){
            message.className = "alert";
            message.className = "alert-error";
            message.innerHTML = return_val;
            document.getElementById("alert").appendChild(message);
            setTimeout(function(){
                message.innerHTML = "";
                document.getElementById("alert").removeChild(message);
            }, 5000);
        } else {
            message.className = "alert";
            message.className = "alert-success";
            message.innerHTML = return_val;
            document.getElementById("alert").appendChild(message);
            setTimeout(function(){
                message.innerHTML = "";
                document.getElementById("alert").removeChild(message);
            }, 5000);
            document.getElementById("form").reset();
        }
    }
    run();
    e.preventDefault();
});
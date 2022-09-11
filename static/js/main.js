$(function(){

let bankData = NaN;
let bostonData = NaN;
let fraudData = NaN;
let toxicData = NaN;

let pathname = window.location.pathname; // Returns path only (/path/example.html)

if (pathname.includes("house")){
        
    $.ajax(
    {
        url:"/getHouse",
        type: "GET",
        success: function(data) {
            bostonData = data;
            let field = data["field"];
            let sample = data["sample"];
            for (let i in field){
                createHtml = '<div class="col-lg-2 mt-2">' +
                '                <label for="' + field[i] + '" ><b>' + field[i].toUpperCase() + '</b></label>' +
                '            </div>' +
                '            <div class="col-lg-2 mt-2">' +
                '                <input type="text" class="form-control" id="'+field[i].split(".")[0]+'" value="'+sample[i]+'"">' +
                '            </div>'
                $(".bostonField").append(createHtml);
            }
        },
        error:function(data){
            alert("fail");
        }
    });

}else if(pathname.includes("bank")){
    
    $.ajax(
        {
            url:"/getBank/",
            type: "GET",
            success: function(data) {
                bankData = data;
                let field = data["field"];
                let sample = data["sample"];
                let bankMapper = data["bankMap"];

                for (let i in field){
                    if(Object.keys(bankMapper).includes(field[i])){
                        let priKey = bankMapper[field[i]];
                        createHtml = '<div class="col-lg-2 mt-2">' +
                        '                <label for="' + field[i] + '" ><b>' + field[i].toUpperCase() + '</b></label>' +
                        '            </div>' +
                        '            <div class="col-lg-2 mt-2">' +
                        '               <select name='+field[i]+' id="'+field[i]+'" class="form-control">'+
                        '            </div>'
                        $(".classField").append(createHtml);
                   
                        for(let seckey in priKey){
                        
                            if(sample[i] == priKey[seckey]){
                                optStr = '<option value="'+priKey[seckey]+'" selected>'+seckey+'</option>'
                                $('select[name='+field[i]+']').append(optStr)
                            }else{
                                optStr = '<option value="'+priKey[seckey]+'">'+seckey+'</option>'
                                $('select[name='+field[i]+']').append(optStr)
                            }
                        }
                        

                    }else{
                        createHtml = '<div class="col-lg-2 mt-2">' +
                        '                <label for="' + field[i] + '" ><b>' + field[i].toUpperCase() + '</b></label>' +
                        '            </div>' +
                        '            <div class="col-lg-2 mt-2">' +
                        '                <input type="text" class="form-control" id="'+field[i].split(".")[0]+'" value="'+sample[i]+'"">' +
                        '            </div>'
                        $(".classField").append(createHtml);
                    }
                }
            
            },
            error:function(data){
                ("fail");
            }
        }
    )



}else if(pathname.includes("fraud")){
    $.ajax(
        {
            url:"/getFraud",
            type: "GET",
            success: function(data) {
                fraudData = data;
                let field = data["field"];
                let sample = data["sample"];
                for (let i in field){
                    createHtml = '<div class="col-lg-2 mt-2">' +
                    '                <label for="' + field[i] + '" ><b>' + field[i].toUpperCase() + '</b></label>' +
                    '            </div>' +
                    '            <div class="col-lg-2 mt-2">' +
                    '                <input type="text" class="form-control" id="'+field[i].split(".")[0]+'" value="'+sample[i]+'"">' +
                    '            </div>'
                    $(".fraudField").append(createHtml);
                }
                
            
            },
            error:function(data){
                alert("fail");
            }
        });
}else if(pathname.includes("toxic")){
    $.ajax(
        {
            url:"/getToxic",
            type: "GET",
            success: function(data) {
                toxicData = data;
                let field = data["field"];
                let sample = data["sample"];
                for (let i in field){
                    createHtml = '<div class="col-lg-2 mt-2">' +
                    '                <label for="' + field[i] + '" ><b>' + field[i].toUpperCase() + '</b></label>' +
                    '            </div>' +
                    '            <div class="col-lg-12 mt-2">' +
                    // '                <input type="text" class="form-control" id="'+field[i].split(".")[0]+'" placeholder="'+sample[i]+'" value="'+sample[i]+'"">' +
                    '                 <textarea rows="10" style="width:100%" class="form-control" id ='+field+' placeholder="Write something....">'+sample+'</textarea>' +
                    '            </div>'
                    $(".toxicField").append(createHtml);
                }
                
            
            },
            error:function(data){
                alert("fail");
            }
        });
}


$(".bankSubmit").click(function(){
    let bankMapper = bankData["bankMap"]
    let bankField = bankData["field"]
    let counter = true;
    for (i in bankField){
        if(Object.keys(bankMapper).includes(bankField[i])){
            bankData["sample"][i] = $('#'+bankData["field"][i].split(".")[0]+' :selected').val();
        }else{
            bankData["sample"][i] = $('#'+bankData["field"][i].split(".")[0]).val();
        }
        let tempVal = bankData["sample"][i];
        if(tempVal == null || tempVal ==""){
            counter = false;
            break;
        }
    }
    if(counter){
         $.ajax(
            {
                url:"bankOut/",
                type: "POST",
                data: JSON.stringify(bankData),
                contentType: 'application/json',
                success: function(data) {
                    // $('.classAlert .classMessage').remove();
                    // ansStr = '<span class="col-lg-4 classMessage" style="border: solid 4px black;"><b>'+data+'</b></span>';
                    // $('.classAlert').append(ansStr);
                    $('.classMessage').html(" "+data.toUpperCase());
                    alert("submission success");
                },
                error:function(data){
                    alert("Incorrect data input type");
                }
            }
        );   
    }else{
        alert("Please fill in all the empty field !")
    }

    
});


$(".bostonSubmit").click(function(){
    let counter = true;
    for (i in bostonData["field"]){
        bostonData["sample"][i] = $('#'+bostonData["field"][i].split(".")[0]).val();
        let tempVal = bostonData["sample"][i];
        if(tempVal == null || tempVal ==""){
            counter = false;
            break;
        }
    }
    if(counter){
        $.ajax(
            {
                url:"houseOut/",
                type: "POST",
                data: JSON.stringify(bostonData),
                contentType: 'application/json',
                success: function(data) {
                    // $('.bostonAlert .bostonMessage').remove();
                    // ansStr = '<span class="col-lg-4 bostonMessage" style="border: solid 4px black;"><b>'+data+'</b></span>';
                    // $('.bostonAlert').append(ansStr);
                    $('.bostonMessage').html(" "+data);
                    alert("submission success");
                },
                error:function(data){
                    alert("Incorrect data input type");
                }
            }
        );
    }else{
        alert("Please fill in all the empty field !")
    }

});

$(".fraudSubmit").click(function(){
    let counter = true;
    for (i in fraudData["field"]){
        fraudData["sample"][i] = $('#'+fraudData["field"][i].split(".")[0]).val();
        let tempVal = fraudData["sample"][i];
        if(tempVal == null || tempVal ==""){
            counter = false;
            break;
        }
    }
    if(counter){
        $.ajax(
            {
                url:"fraudOut/",
                type: "POST",
                data: JSON.stringify(fraudData),
                contentType: 'application/json',
                success: function(data) {
                    // $('.fraudAlert .fraudMessage').remove();
                    // ansStr = '<span class="col-lg-4 fraudMessage" style="border: solid 4px black;"><b>'+data+'</b></span>';
                    // $('.fraudAlert').append(ansStr);
                    $('.fraudMessage').html(" "+data.toUpperCase());
                    alert("submission success");
                },
                error:function(data){
                    alert("Incorrect data input type");
                }
            }
        );  
    }else{
        alert("Please fill in all the empty field !")
    }
    
});

$(".toxicSubmit").click(function(){
    let counter = true;
    for (i in toxicData["field"]){
        toxicData["sample"][i] = $('#'+toxicData["field"][i]).val();
        let tempVal = toxicData["sample"][i];
        if(tempVal == null || tempVal ==""){
            counter = false;
            break;
        }
    }
    if(counter){
        $.ajax(
            {
                url:"toxicOut/",
                type: "POST",
                data: JSON.stringify(toxicData),
                contentType: 'application/json',
                success: function(data) {
                    // $('.toxicAlert .toxicMessage').remove();
                    // ansStr = '<span class="col-lg-4 fraudMessage" style="border: solid 4px black;"><b>'+data+'</b></span>';
                    // $('.fraudAlert').append(ansStr);
                    $('.toxicMessage').html(" "+data.toUpperCase());
                    alert("submission success");
                },
                error:function(data){
                    alert("Input error");
                }
            }
        );        
    }else{
        alert("Please fill in all the empty field !")
    }
    
});


});
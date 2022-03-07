let Vsave = document.querySelector(".Vsave");
let Bsave = document.querySelector(".Bsave");
let one=document.querySelector(".one")
let two=document.querySelector(".two")

let three=document.querySelector(".three")


Vsave.addEventListener('click', function () {
    let vstartTime = document.querySelector(".form-control1");
    let vendTime = document.querySelector(".form-control2");
   
    console.log(vstartTime.value + "" + vendTime.value + "");

    let str=vstartTime.value+"*"+vendTime.value;
    $.ajax({
        type: 'POST',
        url: '/vacancy/',
        data: {
            send: str
        },
        // dataType: 'json',
        success: function (res) {
            // console.log(res);
            one.textContent=res.data;
        },
        error: function (err) {
            console.log(err);
        }
    })
})
Bsave.addEventListener('click', function (event) {
    event.preventDefault();


    let bstartTime = document.querySelector(".form-control3");
    let bendTime = document.querySelector(".form-control4");
    let cap = document.querySelector(".form-control5");


    console.log(bstartTime.value + "" + bendTime.value + "");

    let str=bstartTime.value+"*"+bendTime.value+"*"+cap.value;
    $.ajax({
        type: 'POST',
        url: '/book/',
        data: {
            send: str
        },
        // dataType: 'json',
        success: function (res) {
            one.textContent=res.data;
        },
        error: function (err) {
            console.log(err);
        }
    })

})

let btn=document.querySelector(".btn")
btn.addEventListener('click',function(){
    $.ajax({
        type: 'POST',
        url: '/clear/',
        // dataType: 'json',
        success: function (res) {
            alert("ALL MEETING DATA REMOVED")
        },
        error: function (err) {
            console.log(err);
        }
    })
})